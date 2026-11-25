// Daily Observer — scan-event (Supabase Edge Function, single file, Verify JWT OFF)
// The "BE Tunnel MTF + SMC" indicator (v20+) sends one JSON message per pair at the scan hours (default 07, 10, 13, 15, 19 Bucharest).
// This function stores each pair (scan_rows) with a rule-based class:
//   watch   — clear day bias, the day has done less than half of its average move in the bias direction
//   late    — half to 90% of the average move done (with its continuation odds, pullback so far and pullback zone)
//   done    — 90%+ of the average move done, or the 75% line reached (same continuation line: a done day can still give a pullback and another leg)
//   unclear — no bias, a weak vote, no history, or the day already went further against the bias than its average with it
// The first message of a slot opens a run (scan_runs); after SCAN_WAIT_S seconds (default 60) Claude writes a short summary from the stored rows.
// The classes are computed here in code; Claude only comments on them. Thresholds below are untested starting values. Not a trade signal.
//
// Webhook URL in TradingView:  https://<project>.supabase.co/functions/v1/scan-event?key=<AA_KEY>
// Check the setup:              …/scan-event?key=<AA_KEY>&check=1
// Write the summary again:      …/scan-event?key=<AA_KEY>&redo=<slot ISO time>
// One-pair analysis (card tap):  …/scan-event?key=<AA_KEY>&pair=EURUSD&slot=<slot ISO time>[&force=1]  (stored in scan_rows.ai; a second tap reads it back for free)
// Secrets: AA_KEY (or STRAT_KEY), ANTHROPIC_API_KEY; optional AA_MODEL, SCAN_PAIR_MODEL (card analysis; default AA_MODEL), SCAN_WAIT_S, SCAN_LANG (default Romanian).
// Other alert() messages of the same indicator (liquidity, zone, tunnel alerts) reach this URL too when they share the alert: they are ignored.
import { createClient } from "npm:@supabase/supabase-js@2.45.4";

const env = (k: string) => Deno.env.get(k) ?? "";
const findKey = () => ["AA_KEY", "STRAT_KEY", "TV_SECRET", "WEBHOOK_KEY"].find((k) => env(k)) ?? "";
const db = createClient(env("SUPABASE_URL") || "http://localhost", env("SUPABASE_SERVICE_ROLE_KEY") || "x", { auth: { persistSession: false } });
const MODEL = env("AA_MODEL") || "claude-sonnet-5-5";
const CORS = { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "*" };
const json = (o: unknown, status = 200) => new Response(JSON.stringify(o, null, 1), { status, headers: { "Content-Type": "application/json", ...CORS } });

// starting thresholds (untested; to be checked against the stored history)
export const RULES = { minPct: 60, lateFrom: 0.5, doneFrom: 0.9, nearAtr1h: 0.5 };

export type Scan = {
  p: string; t: number; h: number; tf?: string; test?: boolean; c: number; pip?: number;
  dir: number; pct: number | null; up?: number; dn?: number; tot?: number; set?: string; v?: [string, number, number][];
  fund?: number; conv?: string; gap?: string; do?: number; dh?: number; dl?: number; atrd?: number | null; atr1h?: number | null;
  avg: number | null; avg75?: number | null; pb?: number | null; wdone: number | null; adone: number | null; n?: number; q?: number[];
  t1?: [number, number | null]; t4?: [number, number | null]; z?: [string, number, number, number, number | null][];
  lv?: Record<string, number | null>;
};

export function parse(text: string): Scan | null {
  try {
    const a = text.indexOf("{"), b = text.lastIndexOf("}");
    if (a < 0 || b < a) return null;
    const j = JSON.parse(text.slice(a, b + 1));
    if (!j || j.sc !== 1 || !j.p || !j.t) return null;
    j.p = String(j.p).toUpperCase().replace(/[^A-Z0-9]/g, "");
    j.t = +j.t;
    return j as Scan;
  } catch { return null; }
}

const r1 = (x: number) => Math.round(x * 10) / 10;

// share of past bias days whose bias-side extension reached x pips (from the 10…95% points the indicator sends, ATR units × today's daily ATR)
export function survival(d: Scan, x: number): number | null {
  const Q = [10, 20, 30, 40, 50, 60, 70, 80, 90, 95];
  if (!d.q || d.q.length !== Q.length || !d.atrd) return null;
  const pts: [number, number][] = [[0, 1], ...d.q.map((v, i) => [v * (d.atrd as number), 1 - Q[i] / 100] as [number, number])];
  if (x <= 0) return 1;
  if (x > pts[pts.length - 1][0]) return null;   // beyond the 95% point: fewer than 1 day in 20
  for (let i = 1; i < pts.length; i++) {
    const [x0, s0] = pts[i - 1], [x1, s1] = pts[i];
    if (x <= x1) return x1 === x0 ? s1 : s0 + (s1 - s0) * (x - x0) / (x1 - x0);
  }
  return null;
}

// late / done pairs: how often a day that had already gone this far went on to the next level, how far price has pulled back, and the pullback zone
export function continuation(d: Scan) {
  if (!d.dir || d.wdone == null || !d.avg) return null;
  const done = Math.max(d.wdone, 0), sNow = survival(d, done);
  const p90 = d.q && d.atrd && d.q.length === 10 ? r1(d.q[8] * d.atrd) : null;
  const legs: { to: string; more: number; chance: number | null }[] = [];
  for (const [to, lvl] of [["75% line", d.avg75 ?? null], ["90% day", p90]] as [string, number | null][]) {
    if (lvl == null || lvl <= done + 0.5) continue;
    const sT = survival(d, lvl);
    legs.push({ to, more: r1(lvl - done), chance: sNow && sT != null ? Math.round(100 * sT / sNow) : null });
  }
  legs.sort((a, b) => a.more - b.more);
  const pip = d.pip || 0;
  const retraced = pip && d.c != null ? r1(Math.max(0, d.dir < 0 ? (d.c - (d.dl as number)) / pip : ((d.dh as number) - d.c) / pip)) : null;
  // pullback side = against the bias: bias-side zones sit there (bearish zones above price, bullish below); a tunnel counts when price is beyond it with the bias
  const pz = (d.z ?? []).filter((z) => z[4] != null).sort((a, b) => (a[4] as number) - (b[4] as number))[0] ?? null;
  const tun = ([["1H tunnel", d.t1], ["4H tunnel", d.t4]] as [string, [number, number | null] | undefined][])
    .filter(([, t]) => t && t[0] === d.dir && t[1] != null).sort((a, b) => (a[1]![1] as number) - (b[1]![1] as number))[0] ?? null;
  return { legs, beyond95: sNow == null, retraced, zone: pz ? { tag: pz[0], dist: pz[4] } : null, tunnel: tun ? { tag: tun[0], dist: tun[1]![1] } : null };
}

export function contText(c: ReturnType<typeof continuation>, dir: number) {
  if (!c) return "";
  const parts: string[] = [];
  if (c.beyond95) parts.push("already beyond 95% of past days");
  for (const l of c.legs) parts.push(`${l.to} +${l.more}p${l.chance != null ? ` (went on in ${l.chance}% of past days that got this far)` : ""}`);
  if (!c.legs.length && !c.beyond95) parts.push("past the 90% day");
  if (c.retraced != null) parts.push(`pulled back ${c.retraced}p from the day ${dir < 0 ? "low" : "high"}`);
  if (c.zone) parts.push(`pullback zone ${c.zone.tag} ${c.zone.dist === 0 ? "price inside" : c.zone.dist + "p away"}`);
  if (c.tunnel) parts.push(`${c.tunnel.tag} ${c.tunnel.dist === 0 ? "price inside" : c.tunnel.dist + "p away"}`);
  return "continuation: " + parts.join(" · ");
}

// rule-based class; every number in `why` comes from the message
export function classify(d: Scan) {
  const flags: string[] = [];
  const near = d.atr1h ? Math.max(RULES.nearAtr1h * d.atr1h, 1) : 3;
  const zs = (d.z ?? []).filter((z) => z[4] != null).sort((a, b) => (a[4] as number) - (b[4] as number));
  if (zs[0] && (zs[0][4] as number) <= near) flags.push(`${zs[0][0]} ${zs[0][4] === 0 ? "price inside" : zs[0][4] + "p away"}`);
  for (const [k, t] of [["1H tunnel", d.t1], ["4H tunnel", d.t4]] as const) if (t && t[1] != null && t[1] <= near) flags.push(`${k} ${t[1] === 0 ? "price inside" : t[1] + "p away"}`);
  const dirW = d.dir > 0 ? "bullish" : d.dir < 0 ? "bearish" : "neutral";
  const base = { flags, done_pct: null as number | null, room: null as number | null, cont: null as ReturnType<typeof continuation> };
  if (!d.dir) return { ...base, cls: "unclear", score: 0, why: "no day bias (vote tied)" };
  if (d.pct == null || d.pct < RULES.minPct) return { ...base, cls: "unclear", score: 0, why: `weak vote: ${dirW} ${d.pct ?? "?"}%` };
  if (!d.avg || d.wdone == null) return { ...base, cls: "unclear", score: 0, why: `${dirW} ${d.pct}%, no average move` };
  const done = Math.max(d.wdone, 0) / d.avg;
  const done_pct = Math.round(done * 100), room = r1(d.avg - Math.max(d.wdone, 0));
  const head = `${dirW} ${d.pct}% · done ${done_pct}% of ${d.avg}p`;
  if (d.adone != null && d.adone >= d.avg) return { ...base, done_pct, room, cls: "unclear", score: 0, why: `${head} · went ${d.adone}p against the bias (more than the average with it)` };
  const cont = continuation(d), ct = contText(cont, d.dir);
  const contScore = cont?.legs[0]?.chance ?? 0;
  if ((d.avg75 != null && d.wdone >= d.avg75) || done >= RULES.doneFrom) return { ...base, done_pct, room, cont, cls: "done", score: contScore, why: `${head}${d.avg75 != null && d.wdone >= d.avg75 ? " · 75% line reached" : ""}${ct ? " · " + ct : ""}` };
  const pbTxt = d.pb != null && d.adone != null ? ` · pullback ${Math.max(d.adone, 0)}p of usual ${d.pb}p` : "";
  if (done >= RULES.lateFrom) return { ...base, done_pct, room, cont, cls: "late", score: contScore, why: `${head} · ${room}p left to the average${ct ? " · " + ct : ""}` };
  return { ...base, done_pct, room, cls: "watch", score: r1((1 - done) * d.pct), why: `${head} · ${room}p left${pbTxt}` };
}

export function bucHour(ms: number) {
  return +new Intl.DateTimeFormat("en-GB", { timeZone: "Europe/Bucharest", hour: "2-digit", hourCycle: "h23" }).format(new Date(ms));
}

export function rowFrom(d: Scan, raw: string) {
  const k = classify(d);
  return {
    uid: `${d.p}|${d.t}${d.test ? "|test" : ""}`, slot: new Date(d.t).toISOString(), hour_local: d.h ?? bucHour(d.t), pair: d.p, test: !!d.test,
    cls: k.cls, rank_score: k.score, why: k.why + (k.flags.length ? " · near: " + k.flags.join(", ") : ""),
    data: { ...d, _raw_len: raw.length, _cls: k },
  };
}

// Sonnet 5.5 thinks by default (adaptive, high effort) and thinking counts toward max_tokens: a short note could end with no text.
// "between_tools" is the lowest thinking setting on Sonnet 5.5 (no up-front thinking); other models keep their default.
export const thinkingFor = (model: string) => (/sonnet-5-5/.test(model) ? { type: "between_tools" } : undefined);

// ---------- summary (Claude) ----------
const SYSTEM = `You are a senior FX analyst writing a short scan note for a discretionary intraday trader (5m execution, trades 07:00–20:00 Bucharest, prop-firm risk limits).
You receive a table built by code from his TradingView indicator: day bias vote, how much of the pair's average day move (bias side) is already done, the usual pullback, nearby zones and tunnels.
Rules: use only the numbers in the data, never invent prices or levels; do not change a pair's class; no entries, stops, targets or buy/sell instructions — say what is worth watching and why.
The classes and thresholds are untested starting rules; say "untested" once at the end.`;

export function promptFor(rows: { pair: string; cls: string; why: string; data: Scan }[], when: string, lang: string) {
  const order = ["watch", "late", "done", "unclear"];
  const t = rows.slice().sort((a, b) => order.indexOf(a.cls) - order.indexOf(b.cls)).map((r) => ({
    pair: r.pair, cls: r.cls, why: r.why, fund: r.data.fund, conv: r.data.conv, votes: r.data.v, avg: r.data.avg, avg75: r.data.avg75, pb: r.data.pb,
    wdone: r.data.wdone, adone: r.data.adone, continuation: (r.data as Scan & { _cls?: { cont?: unknown } })._cls?.cont ?? null, zones: r.data.z, t1: r.data.t1, t4: r.data.t4, levels: r.data.lv,
  }));
  return `Scan at ${when} Bucharest, ${rows.length} pairs. Write in ${lang}, mobile-friendly, short:
1. "De urmărit" (watch): one line per pair — direction, % done and room left in pips, the nearest zone/tunnel if listed, what would make it interesting.
2. "Târziu" (late) and "Done": one line per pair about the continuation — how much more the day could go (to the 75% line / 90% day) and on what share of past days that got this far it did, how far price has already pulled back, and the pullback zone or tunnel it could come back to before another leg. If the continuation numbers are missing or the pair is beyond 95% of past days, say so in a few words.
3. "Neclar": just the pair names in one line.
Headers: De urmărit, Târziu, Done, Neclar; no intro. The continuation share is conditional history (days with the same technical bias), not a probability for today.

DATA (JSON):
${JSON.stringify(t)}`;
}

async function askClaude(user: string) {
  const key = env("ANTHROPIC_API_KEY");
  if (!key) throw new Error("ANTHROPIC_API_KEY secret is missing");
  const res = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json" },
    body: JSON.stringify({ model: MODEL, max_tokens: 4000, thinking: thinkingFor(MODEL), system: SYSTEM, messages: [{ role: "user", content: user }] }),
  });
  const j = await res.json();
  if (!res.ok) throw new Error(j?.error?.message || `Anthropic API ${res.status}`);
  return (j.content ?? []).filter((c: { type: string }) => c.type === "text").map((c: { text: string }) => c.text).join("\n").trim();
}

export async function summarize(slot: string) {
  const { data: rows, error } = await db.from("scan_rows").select("pair,cls,why,data,hour_local").eq("slot", slot).eq("test", false);
  if (error) throw new Error(error.message);
  if (!rows?.length) { await db.from("scan_runs").update({ status: "error", error: "no rows" }).eq("slot", slot); return; }
  try {
    const when = new Intl.DateTimeFormat("en-GB", { timeZone: "Europe/Bucharest", hour: "2-digit", minute: "2-digit", hourCycle: "h23" }).format(new Date(slot));
    const text = await askClaude(promptFor(rows as never, when, env("SCAN_LANG") || "Romanian"));
    if (!text) throw new Error("empty answer (the model used the tokens before writing)");
    await db.from("scan_runs").update({ status: "done", n: rows.length, summary: text, model: MODEL, error: null, done_at: new Date().toISOString() }).eq("slot", slot);
  } catch (e) {
    await db.from("scan_runs").update({ status: "error", n: rows.length, error: (e as Error).message }).eq("slot", slot);
  }
}


// ---------- one-pair analysis (tap on a Scanner card) ----------
const PAIR_SYSTEM = `Ești analistul de trade-uri al unui trader intraday (execuție pe 5m, tranzacționează 07:00–20:00 București, conturi prop cu limite de risc).
Primești datele indicatorului BE Tunnel SMC pentru o pereche, la ora unei scanări. Răspunzi în română, scurt, pentru telefon (max ~1 ecran și jumătate).
Reguli: folosești doar prețurile și cifrele din date, nu inventezi niveluri; dacă ceva lipsește, spui. Nu promiți rezultate și nu spui „sigur”.
Distanțele sunt predictibile, direcția nu. Fundamentalul (Fund) e singurul vot independent; T1H, T4H, Slope, SMA20 și DO măsoară toate trendul, deci un procent mare poate fi un singur argument numărat de mai multe ori.
„done” peste ~80% = ziua tipică e consumată; linia de 75% e atinsă ~1 zi din 4; „continuation” = cât de des au continuat zilele trecute care ajunseseră la fel de departe (istoric condiționat, votul tehnic de la 09:00, nu probabilitate pentru azi).
Zonele OB/FVG, sweep-urile și voturile tehnice folosite mecanic nu au avut edge în teste; folosește-le ca locuri de intrare și obstacole, nu ca argumente de direcție.
Datele sunt de la ora scanării; prețul s-a putut mișca de atunci — spune asta o dată, scurt.`;

const PAIR_FORMAT = `Format (fără alte titluri):
**Pe scurt:** 2–3 fraze cu verdictul (de ex. „bias bearish, dar ziua e consumată 90%… are mai mult sens să aștepți pullback-ul spre X”).
**Unitate:** o frază (ex. pentru aur 1p = $0.01, deci $1 = 100p), doar dacă nu e o pereche forex obișnuită.
**Ce văd** — 4–6 puncte: prețul și DO, minimul/maximul zilei, biasul și voturile (cine e ▲, cine e ▼, Fund), Avg cu prețul liniei AVG și done %, linia de 75% și pullback-ul tipic, tunelurile (deasupra/sub, la câți pipși), zonele cu prețuri, nivelurile OPEN (PDH/PDL/PWH/PWL/BSL/SSL) cu prețuri.
**Pentru** (partea biasului) — 2–3 puncte.
**Prudență** — 2–4 puncte, cu distanțe în pipși.
**Ce aș face (opțiuni, decizia e a ta)** — 2–3 variante numerotate: unde ar avea sens intrarea (pullback la DO / zonă / tunel), SL logic (peste/sub zonă, sweep, DO) și TP realist față de AVG și niveluri, cu R aproximativ; plus ce faci dacă prețul nu revine. Dacă biasul e slab sau neclar, spune că varianta cea mai bună e să aștepți.`;

// prices from the distances the indicator sends, so the analysis can name levels
export function pairContext(d: Scan) {
  const pip = d.pip || 0, c = d.c, dir = d.dir;
  const px = (x: number | null | undefined, sign: number) => (x == null || !pip || c == null ? null : +(c + sign * x * pip).toFixed(6));
  const lvl = (dist: number | null | undefined, from: number | undefined, sign: number) => (dist == null || from == null || !pip ? null : +(from + sign * dist * pip).toFixed(6));
  const tun = (t?: [number, number | null]) => !t || t[1] == null ? null : { price_vs_tunnel: t[0] > 0 ? "above" : t[0] < 0 ? "below" : "inside", pips: t[1], edge: t[0] === 0 ? null : px(t[1], t[0] > 0 ? -1 : 1) };
  const lv = d.lv ?? {};
  return {
    pair: d.p, scan_close_time: d.t ? new Date(d.t).toISOString() : null, price: c, pip_size: pip, unit: "p = pips as the indicator shows them (forex: 0.0001 or 0.01 for JPY; gold/indices: one point = minimum tick)",
    day_bias: dir > 0 ? "bullish" : dir < 0 ? "bearish" : "neutral", vote_pct: d.pct, votes: (d.v ?? []).map(([n, v, w]) => `${n}${v > 0 ? "▲" : v < 0 ? "▼" : "–"}${w > 1 ? "×" + w : ""}`).join(" "), vote_set: d.set,
    fundamental: { vote: d.fund, conviction: d.conv, gap: d.gap },
    day_open: d.do, day_high: d.dh, day_low: d.dl, atr_daily_pips: d.atrd, atr_1h_pips: d.atr1h,
    avg_move: d.avg == null ? null : { pips: d.avg, line: lvl(d.avg, d.do, dir || 0), done_pips: d.wdone, done_pct: d.avg ? Math.round(100 * Math.max(d.wdone ?? 0, 0) / d.avg) : null, sample_days: d.n },
    avg_75: d.avg75 == null ? null : { pips: d.avg75, line: lvl(d.avg75, d.do, dir || 0) },
    usual_pullback: d.pb == null ? null : { pips: d.pb, line: lvl(d.pb, d.do, -(dir || 0)), against_so_far_pips: d.adone },
    continuation: continuation(d),
    tunnel_1h: tun(d.t1), tunnel_4h: tun(d.t4),
    zones_bias_side: (d.z ?? []).map(([tag, side, bot, top, dist]) => ({ tag, side: side > 0 ? "bullish" : "bearish", bot, top, pips_away: dist })),
    open_levels: { "1H BSL": px(lv.bsl, 1), "1H SSL": px(lv.ssl, -1), PDH: px(lv.pdh, 1), PDL: px(lv.pdl, -1), PWH: px(lv.pwh, 1), PWL: px(lv.pwl, -1) },
    open_levels_pips: lv,
  };
}

// streamed: the text is saved every few seconds, so the page shows it while Claude writes and nothing is lost if the function is stopped
async function askPair(ctx: unknown, save: (text: string) => Promise<void>, tag: string) {
  const key = env("ANTHROPIC_API_KEY");
  if (!key) throw new Error("ANTHROPIC_API_KEY secret is missing");
  const model = env("SCAN_PAIR_MODEL") || MODEL;
  const t0 = Date.now();
  const res = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json" },
    body: JSON.stringify({ model, max_tokens: 4000, stream: true, thinking: thinkingFor(model), system: PAIR_SYSTEM, messages: [{ role: "user", content: `${PAIR_FORMAT}\n\nDATE (JSON):\n${JSON.stringify(ctx)}` }] }),
  });
  console.log(`${tag}: API status ${res.status} after ${((Date.now() - t0) / 1000).toFixed(1)}s (model ${model})`);
  if (!res.ok || !res.body) { const j = await res.json().catch(() => ({})); throw new Error(j?.error?.message || `Anthropic API ${res.status}`); }
  const reader = res.body.getReader(), dec = new TextDecoder();
  let buf = "", text = "", first = 0, lastSave = 0, stop = "";
  for (;;) {
    const { value, done } = await reader.read();
    if (done) break;
    buf += dec.decode(value, { stream: true });
    let i;
    while ((i = buf.indexOf("\n")) >= 0) {
      const line = buf.slice(0, i).trim(); buf = buf.slice(i + 1);
      if (!line.startsWith("data:")) continue;
      let ev: { type?: string; delta?: { type?: string; text?: string; stop_reason?: string }; error?: { message?: string } };
      try { ev = JSON.parse(line.slice(5)); } catch { continue; }
      if (ev.type === "error") throw new Error(ev.error?.message || "stream error");
      if (ev.type === "content_block_delta" && ev.delta?.type === "text_delta") {
        if (!first) { first = Date.now(); console.log(`${tag}: first text after ${((first - t0) / 1000).toFixed(1)}s`); }
        text += ev.delta.text ?? "";
      }
      if (ev.type === "message_delta" && ev.delta?.stop_reason) stop = ev.delta.stop_reason;
    }
    if (text && Date.now() - lastSave > 3000) { lastSave = Date.now(); await save(text); }
  }
  console.log(`${tag}: done after ${((Date.now() - t0) / 1000).toFixed(1)}s, ${text.length} chars, stop ${stop || "?"}`);
  return { text: text.trim(), model };
}

// runs in the background: the page polls scan_rows.ai (free) instead of holding the request open while Claude writes
export async function analysePair(pair: string, slot: string, force: boolean) {
  const { data: row, error } = await db.from("scan_rows").select("id,data,ai,ai_model,ai_at").eq("pair", pair).eq("slot", slot).eq("test", false).maybeSingle();
  if (error) throw new Error(error.message);
  if (!row) return { error: "no scan row for this pair and time" };
  if (row.ai && !force && !String(row.ai_model || "").startsWith("pending")) return { ai: row.ai, ai_model: row.ai_model, ai_at: row.ai_at, cached: true };
  const age = row.ai_at ? Math.round((Date.now() - Date.parse(row.ai_at)) / 1000) : 0;
  const busy = String(row.ai_model || "").startsWith("pending") && age < 160;   // older than the function's time limit = stuck, start again
  if (busy) return { pending: true, since: row.ai_at, age_s: age };
  const at = new Date().toISOString();
  await db.from("scan_rows").update({ ai_model: "pending", ai_at: at, ...(force ? { ai: null } : {}) }).eq("id", row.id);
  const job = (async () => {
    try {
      const save = async (t: string) => { await db.from("scan_rows").update({ ai: t }).eq("id", row.id); };
      const { text, model } = await askPair(pairContext(row.data as Scan), save, `${pair} ${slot}`);
      if (!text) throw new Error("empty answer (the model used the tokens before writing)");
      await db.from("scan_rows").update({ ai: text, ai_model: model, ai_at: new Date().toISOString() }).eq("id", row.id);
    } catch (e) {
      console.error(`${pair} ${slot}: ${(e as Error).message}`);
      await db.from("scan_rows").update({ ai_model: "error: " + (e as Error).message.slice(0, 180), ai_at: new Date().toISOString() }).eq("id", row.id);
    }
  })();
  const rt = (globalThis as unknown as { EdgeRuntime?: { waitUntil: (p: Promise<unknown>) => void } }).EdgeRuntime;
  if (rt?.waitUntil) rt.waitUntil(job); else await job;
  return { pending: true, since: at, age_s: 0 };
}

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

export async function process(text: string) {
  const d = parse(text);
  if (!d) return { ignored: true };   // other alerts of the same indicator
  const row = rowFrom(d, text);
  const { error } = await db.from("scan_rows").upsert(row, { onConflict: "uid" });
  if (error) throw new Error(error.message);
  // the first message of a slot opens the run and, after the wait, writes the summary (test messages: stored only)
  const { data: opened } = await db.from("scan_runs").upsert({ slot: row.slot, hour_local: row.hour_local, test: row.test, status: row.test ? "test" : "waiting" },
    { onConflict: "slot", ignoreDuplicates: true }).select("slot");
  if (opened?.length && !row.test) {
    await sleep(Math.min(120, Math.max(10, +(env("SCAN_WAIT_S") || 60))) * 1000);
    await summarize(row.slot);
  }
  return { stored: row.uid, cls: row.cls };
}

export async function handle(req: Request): Promise<Response> {
  const u = new URL(req.url);
  if (req.method === "OPTIONS") return new Response(null, { headers: CORS });
  const keyName = findKey();
  if (!keyName || u.searchParams.get("key") !== env(keyName)) return json({ error: "wrong or missing key" }, 401);
  if (u.searchParams.get("check")) {
    const t = await Promise.all(["scan_rows", "scan_runs"].map(async (n) => {
      const { count, error } = await db.from(n).select("*", { count: "exact", head: true });
      return [n, error ? "ERROR: " + error.message : `ok (${count} rows)`];
    }));
    return json({ key_secret: keyName, anthropic_key: env("ANTHROPIC_API_KEY") ? "set" : "MISSING", model: MODEL, ...Object.fromEntries(t) });
  }
  const ap = u.searchParams.get("pair");
  if (ap && u.searchParams.get("slot")) {
    try { return json(await analysePair(ap.toUpperCase(), new Date(u.searchParams.get("slot") as string).toISOString(), !!u.searchParams.get("force"))); }
    catch (e) { return json({ error: (e as Error).message }, 500); }
  }
  const redo = u.searchParams.get("redo");
  if (redo) {
    const slot = new Date(redo).toISOString();
    await db.from("scan_runs").upsert({ slot, status: "waiting" }, { onConflict: "slot" });
    await summarize(slot);
    const { data } = await db.from("scan_runs").select("*").eq("slot", slot).maybeSingle();
    return json(data);
  }
  if (req.method !== "POST") return json({ error: "POST the TradingView alert message here" }, 405);
  const text = await req.text();
  const p = process(text).catch((e) => console.error("scan-event:", (e as Error).message));
  const rt = (globalThis as unknown as { EdgeRuntime?: { waitUntil: (p: Promise<unknown>) => void } }).EdgeRuntime;
  if (rt?.waitUntil) rt.waitUntil(p); else await p;
  return json({ accepted: true });
}

if (import.meta.main) Deno.serve(handle);
