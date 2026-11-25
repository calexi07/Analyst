// Daily Observer — aa-analyst (Supabase Edge Function, single file, Verify JWT OFF)
// The three buttons of the Auto-Analyst page call this function:
//   mode=plan    (morning)  → reads the last days of market events (D / 4H / 1H), the state snapshot and the fundamentals,
//                             writes a plan with concrete, testable setups to watch
//   mode=confirm (intraday) → re-reads the plan and what happened since, says VALID / INVALID / WAIT;
//                             a valid setup becomes a virtual trade (aa_paper)
//   mode=close   (evening)  → reviews the day: what the plan got right or wrong, lessons, what to watch next
// Every answer is stored in aa_notes with the exact context it was given (nothing is rewritten after the fact).
//
// POST https://<project>.supabase.co/functions/v1/aa-analyst?key=<AA_KEY>   body: {"pair":"EURUSD","mode":"plan"}
// Secrets: AA_KEY (or STRAT_KEY), ANTHROPIC_API_KEY, optional AA_MODEL (default claude-sonnet-5-5).
import { createClient } from "npm:@supabase/supabase-js@2.45.4";

const env = (k: string) => Deno.env.get(k) ?? "";
const findKey = () => ["AA_KEY", "STRAT_KEY", "TV_SECRET", "WEBHOOK_KEY"].find((k) => env(k)) ?? "";
const MODEL = env("AA_MODEL") || "claude-sonnet-5-5";
const db = createClient(env("SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const CORS = { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "*", "Access-Control-Allow-Methods": "POST, GET, OPTIONS" };
const json = (o: unknown, status = 200) => new Response(JSON.stringify(o, null, 1), { status, headers: { "Content-Type": "application/json", ...CORS } });
const bucDay = (d = new Date()) => d.toLocaleDateString("sv-SE", { timeZone: "Europe/Bucharest" });
const buc = (iso: string) => new Date(iso).toLocaleString("sv-SE", { timeZone: "Europe/Bucharest" }).slice(0, 16);
function isoWeek(d: Date) {
  const t = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate()));
  const day = t.getUTCDay() || 7; t.setUTCDate(t.getUTCDate() + 4 - day);
  const y = t.getUTCFullYear(); const w = Math.ceil(((t.getTime() - Date.UTC(y, 0, 1)) / 864e5 + 1) / 7);
  return { year: y, week: w };
}

const SYSTEM = `You are a discretionary FX / gold trader and market analyst with more than 20 years of experience, working for one trader.
Your method is top-down and multi-timeframe: Daily → 4H → 1H. Entries are only on 4H or 1H.
You read: fractal structure (candle-based BOS / CHoCH), swing structure (close beyond a swing, like LuxAlgo), supply / demand zones created by
structure breaks (refined = origin candle, full = origin extreme to the broken level), liquidity taken (fractal highs/lows, PDH/PDL, PWH/PWL,
Asia / London / New York highs and lows), premium / discount inside the swing range, and the weekly FUNDAMENTAL bias from the trader's Bias Engine.
Typical ideas: trade with the Daily + 4H swing direction after a 1H pullback reaches a 4H zone in premium (shorts) / discount (longs) and 1H
confirms with a CHoCH; zones are stronger after liquidity was taken and when liquidity rests just behind them; the stop goes at the edge of the
zone (4H or 1H) or beyond the confirmed liquidity; counter-trend trades toward the Daily 0.5 only when the higher timeframe is extended.

STRICT RULES
- Use ONLY the data given below. Never invent prices, news or events. Every price you write must come from the events, the state snapshot or the bars.
- Be concrete and testable: a setup has a direction, the zone, the exact trigger (which timeframe, which event), entry, stop, target, and when it is invalid.
- Prefer no trade over a weak trade. Say clearly when the data is insufficient.
- Statistics the trader has measured on EURUSD 2005–2025 (keep them in mind, do not overstate edges): structure / zones alone gave roughly 0R per trade;
  stops at the edge of a Daily or 4H zone did better than tight 1H stops; zones with liquidity resting behind them held more often;
  the fundamental bias is the main candidate for an edge, so weigh it.
- Write in Romanian, short and clear (the trader reads on a phone). Prices with the pair's normal decimals.
- Finish with ONE JSON object inside <json> … </json> exactly as specified for the mode. No comments inside the JSON.`;

const SPEC: Record<string, string> = {
  plan: `MODE: MORNING PLAN.
Write: 1) Context top-down (D, 4H, 1H: fractal + swing trend, where price is in the range, liquidity taken recently, active zones), 2) fundamental bias and how it fits,
3) up to 3 scenarios to watch today, each with zone, trigger, entry, SL, TP, invalidation, 4) what would make you NOT trade today.
JSON: {"bias":"long|short|neutral","confidence":"low|medium|high","summary":"one line",
"scenarios":[{"id":"A","name":"short name","dir":1 or -1,"tf_entry":"1H|4H","zone":[low,high],"trigger":"text","entry":number,"sl":number,"tp":number,"invalid_if":"text","valid_until":"HH:MM"}],
"watch":["short items to watch"],"no_trade_if":"text"}`,
  confirm: `MODE: CONFIRMATION. The trader pressed "confirm" because something from the morning plan seems to be happening.
Compare the plan with the events since the plan. Decide: VALID (take it now), INVALID (the idea is dead) or WAIT (not yet).
If VALID give the exact order. Do not re-plan from scratch; judge the plan's own conditions.
JSON: {"verdict":"VALID|INVALID|WAIT","scenario":"id from the plan or null","reason":"text",
"order":{"dir":1 or -1,"type":"market|limit","entry":number,"sl":number,"tp":number,"expires_hours":number} or null}`,
  close: `MODE: CLOSE THE DAY. Review honestly: what happened today (events), which scenario played out, was the plan right or wrong and why,
what the confirmation did, the virtual trades' results, mistakes (reading, timing, levels, bias), lessons that should change future plans
(only lessons supported by what happened; one day is not proof — say so), and what to watch tomorrow.
JSON: {"plan_score":0-10,"played":"which scenario or none","right":["…"],"wrong":["…"],"lessons":["…"],"watch_tomorrow":["…"]}`,
};

async function context(pair: string, mode: string, fund: Record<string, unknown> | null) {
  const now = new Date(); const day = bucDay(now);
  const since = new Date(now.getTime() - 8 * 864e5).toISOString();
  const { data: evs } = await db.from("aa_events").select("bar_time, tf, ev, dir, level, zlo, zhi, info").eq("pair", pair).neq("ev", "bar")
    .gte("bar_time", since).order("bar_time", { ascending: true }).limit(400);
  const { data: bars } = await db.from("aa_events").select("bar_time, info, price").eq("pair", pair).eq("ev", "bar")
    .gte("bar_time", new Date(now.getTime() - 5 * 864e5).toISOString()).order("bar_time", { ascending: true }).limit(200);
  const last = bars?.length ? bars[bars.length - 1] : null;
  const w = isoWeek(now);
  const { data: wk } = await db.from("do_weekly").select("bias, conviction, fundamentals, review, details").eq("pair", pair).eq("year", w.year).eq("week", w.week).maybeSingle();
  // the page sends the latest daily check for this pair (most checks live in the repo, not in Supabase)
  const check = fund?.check ?? null;
  const { data: notes } = await db.from("aa_notes").select("id, created_at, kind, text, data").eq("pair", pair).eq("day", day).order("id", { ascending: true });
  const { data: lessons } = await db.from("aa_notes").select("day, pair, data").eq("kind", "close").order("id", { ascending: false }).limit(12);
  const { data: paper } = await db.from("aa_paper").select("pair, day, setup, dir, entry, sl, tp, status, r, opened_at, closed_at").order("id", { ascending: false }).limit(200);
  const closed = (paper ?? []).filter((p: { r: number | null }) => p.r != null);
  const stats = { trades: closed.length, wins: closed.filter((p: { r: number }) => p.r > 0).length, R: Math.round(closed.reduce((s: number, p: { r: number }) => s + p.r, 0) * 100) / 100,
    this_pair: closed.filter((p: { pair: string }) => p.pair === pair).length };
  // compact bar path: 1H candles of the last days (time, o, h, l, c)
  const path = (bars ?? []).map((b: { bar_time: string; info: { o: number; h: number; l: number; c: number } }) => [buc(b.bar_time), b.info?.o, b.info?.h, b.info?.l, b.info?.c]);
  const events = (evs ?? []).map((e: { bar_time: string; tf: string; ev: string; dir: number; level: number; zlo: number; zhi: number; info: { x?: string } | null }) =>
    [buc(e.bar_time), e.tf, e.ev, e.dir, e.level, e.zlo, e.zhi, e.info?.x ?? ""]);
  return {
    pair, mode, now_bucharest: buc(now.toISOString()), day,
    price_now: last?.price ?? null, last_bar: last ? buc(last.bar_time) : null,
    state_snapshot: (last?.info as { st?: unknown } | null)?.st ?? null,
    events_columns: ["time (Bucharest)", "tf", "event", "dir", "level", "zone_low", "zone_high", "extra"], events,
    bars_1h_columns: ["time", "open", "high", "low", "close"], bars_1h: path,
    fundamentals_this_week: wk ?? fund?.weekly ?? null, latest_daily_check: check ?? null,
    today_notes: (notes ?? []).map((n: { kind: string; created_at: string; data: unknown; text: string }) => ({ kind: n.kind, at: buc(n.created_at), data: n.data, text: n.text?.slice(0, 3000) })),
    recent_lessons: (lessons ?? []).map((l: { day: string; pair: string; data: { lessons?: string[] } }) => ({ day: l.day, pair: l.pair, lessons: l.data?.lessons ?? [] })),
    paper_today: (paper ?? []).filter((p: { pair: string; day: string }) => p.pair === pair && p.day === day),
    paper_stats: stats,
  };
}

async function askClaude(ctx: Record<string, unknown>, mode: string) {
  const key = env("ANTHROPIC_API_KEY");
  if (!key) throw new Error("ANTHROPIC_API_KEY secret is missing");
  const user = `${SPEC[mode]}\n\nDATA (JSON):\n${JSON.stringify(ctx)}`;
  const res = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json" },
    body: JSON.stringify({ model: MODEL, max_tokens: 4000, system: SYSTEM, messages: [{ role: "user", content: user }] }),
  });
  const j = await res.json();
  if (!res.ok) throw new Error(j?.error?.message || `Anthropic API ${res.status}`);
  const text = (j.content ?? []).filter((c: { type: string }) => c.type === "text").map((c: { text: string }) => c.text).join("\n");
  return text;
}

export function split(text: string) {
  const m = text.match(/<json>([\s\S]*?)<\/json>/i);
  let data: Record<string, unknown> | null = null;
  if (m) { try { data = JSON.parse(m[1].trim()); } catch { data = { parse_error: true, raw: m[1].slice(0, 2000) }; } }
  const md = text.replace(/<json>[\s\S]*?<\/json>/i, "").trim();
  return { md, data };
}

// a VALID confirmation with a sane order becomes a virtual trade
export function orderFrom(data: Record<string, unknown> | null, priceNow: number | null) {
  const o = data?.order as { dir?: number; type?: string; entry?: number; sl?: number; tp?: number; expires_hours?: number } | null | undefined;
  if (!data || String(data.verdict).toUpperCase() !== "VALID" || !o) return null;
  const dir = o.dir === 1 ? 1 : o.dir === -1 ? -1 : 0;
  const market = String(o.type) === "market";
  const entry = market && priceNow != null ? priceNow : Number(o.entry);
  const sl = Number(o.sl), tp = Number(o.tp);
  if (!dir || !isFinite(entry) || !isFinite(sl) || !isFinite(tp)) return null;
  if ((entry - sl) * dir <= 0 || (tp - entry) * dir <= 0) return null;   // stop and target on the right sides
  return { dir, order_type: market ? "market" : "limit", entry, sl, tp, hours: Math.min(72, Math.max(1, Number(o.expires_hours) || 12)) };
}

export async function handle(req: Request): Promise<Response> {
  const u = new URL(req.url);
  if (req.method === "OPTIONS") return new Response(null, { headers: CORS });
  const keyName = findKey();
  if (!keyName || u.searchParams.get("key") !== env(keyName)) return json({ error: "wrong or missing key" }, 401);
  if (u.searchParams.get("check")) return json({ key_secret: keyName, anthropic_key: env("ANTHROPIC_API_KEY") ? "found" : "MISSING", model: MODEL });
  let body: { pair?: string; mode?: string; fund?: Record<string, unknown> } = {};
  try { body = await req.json(); } catch { /* empty */ }
  const pair = String(body.pair ?? u.searchParams.get("pair") ?? "").toUpperCase().replace(/[^A-Z0-9]/g, "");
  const mode = String(body.mode ?? u.searchParams.get("mode") ?? "");
  if (!pair || !SPEC[mode]) return json({ error: "need pair and mode (plan | confirm | close)" }, 400);
  try {
    const ctx = await context(pair, mode, body.fund ?? null);
    if (!(ctx.events as unknown[]).length && !(ctx.bars_1h as unknown[]).length) return json({ error: "no market events for this pair yet — is the BE Auto-Analyst alert running on its 1H chart?" }, 409);
    const text = await askClaude(ctx, mode);
    const { md, data } = split(text);
    const { data: note, error } = await db.from("aa_notes").insert({ pair, day: ctx.day, kind: mode, model: MODEL, text: md, data, context: ctx }).select("id").single();
    if (error) throw new Error(error.message);
    let paper = null;
    if (mode === "confirm") {
      const o = orderFrom(data, ctx.price_now as number | null);
      if (o) {
        const now = Date.now();
        const row = { pair, day: ctx.day, note_id: note.id, setup: String(data?.scenario ?? "confirmed setup"), dir: o.dir, order_type: o.order_type, entry: o.entry, sl: o.sl, tp: o.tp,
          status: o.order_type === "market" ? "open" : "pending", opened_at: o.order_type === "market" ? new Date(now).toISOString() : null,
          expires_at: new Date(now + o.hours * 36e5).toISOString(), why: String(data?.reason ?? "").slice(0, 500) };
        const ins = await db.from("aa_paper").insert(row).select().single();
        paper = ins.error ? { error: ins.error.message } : ins.data;
      }
    }
    return json({ ok: true, note_id: note.id, text: md, data, paper });
  } catch (e) {
    return json({ error: (e as Error).message }, 500);
  }
}

if (import.meta.main) Deno.serve(handle);
