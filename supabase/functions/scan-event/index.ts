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
// Secrets: AA_KEY (or STRAT_KEY), ANTHROPIC_API_KEY; optional AA_MODEL, SCAN_WAIT_S, SCAN_LANG (default Romanian).
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

// ---------- summary (Claude) ----------
const SYSTEM = `You are a senior FX analyst writing a short scan note for a discretionary intraday trader (5m execution, trades 07:00–20:00 Bucharest, prop-firm risk limits).
You receive a table built by code from his TradingView indicator: day bias vote, how much of the pair's average day move (bias side) is already done, the usual pullback, nearby zones and tunnels.
Rules: use only the numbers in the data, never invent prices or levels; do not change a pair's class; no entries, stops, targets or buy/sell instructions — say what is worth watching and why.
The classes and thresholds are untested starting rules; say "untested" once at the end.`;

export function promptFor(rows: { pair: string; cls: string; why: string; data: Scan }[], hour: number, lang: string) {
  const order = ["watch", "late", "done", "unclear"];
  const t = rows.slice().sort((a, b) => order.indexOf(a.cls) - order.indexOf(b.cls)).map((r) => ({
    pair: r.pair, cls: r.cls, why: r.why, fund: r.data.fund, conv: r.data.conv, votes: r.data.v, avg: r.data.avg, avg75: r.data.avg75, pb: r.data.pb,
    wdone: r.data.wdone, adone: r.data.adone, continuation: (r.data as Scan & { _cls?: { cont?: unknown } })._cls?.cont ?? null, zones: r.data.z, t1: r.data.t1, t4: r.data.t4, levels: r.data.lv,
  }));
  return `Scan at ${String(hour).padStart(2, "0")}:00 Bucharest, ${rows.length} pairs. Write in ${lang}, mobile-friendly, short:
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
    body: JSON.stringify({ model: MODEL, max_tokens: 1500, system: SYSTEM, messages: [{ role: "user", content: user }] }),
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
    const text = await askClaude(promptFor(rows as never, rows[0].hour_local, env("SCAN_LANG") || "Romanian"));
    await db.from("scan_runs").update({ status: "done", n: rows.length, summary: text, model: MODEL, error: null, done_at: new Date().toISOString() }).eq("slot", slot);
  } catch (e) {
    await db.from("scan_runs").update({ status: "error", n: rows.length, error: (e as Error).message }).eq("slot", slot);
  }
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
