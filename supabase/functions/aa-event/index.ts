// Daily Observer — aa-event (Supabase Edge Function, single file, Verify JWT OFF)
// The "BE Auto-Analyst" TradingView indicator posts one JSON message per closed 1H candle per pair.
// This function stores the candle (ev = 'bar') and every market event (structure breaks, liquidity taken, zones …) in aa_events,
// then moves the virtual trades of that pair (aa_paper) with the candle: pending → open → won / lost / expired.
//
// Webhook URL in TradingView:  https://<project>.supabase.co/functions/v1/aa-event?key=<AA_KEY>
// Check the setup:              …/aa-event?key=<AA_KEY>&check=1
// Secrets: AA_KEY (any long random text; STRAT_KEY is accepted too, so the same key as the strategies works).
//
// Message (sent by the indicator, alert() with "once per bar close"):
// {"aa":1,"p":"EURUSD","t":1764000000000,"o":1.1,"h":1.1,"l":1.1,"c":1.1,
//  "ev":[["4H","frac_choch",1,1.0950,1.0921,1.0934,"refined"], …],   // [tf, ev, dir, level, zlo, zhi, extra]
//  "st":{ … state snapshot: trend per timeframe, swing range, premium/discount … }}
import { createClient } from "npm:@supabase/supabase-js@2.45.4";

const env = (k: string) => Deno.env.get(k) ?? "";
const findKey = () => ["AA_KEY", "STRAT_KEY", "TV_SECRET", "WEBHOOK_KEY"].find((k) => env(k)) ?? "";
const db = createClient(env("SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const json = (o: unknown, status = 200) =>
  new Response(JSON.stringify(o, null, 1), { status, headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" } });

export type Bar = { t: number; o: number; h: number; l: number; c: number };
export type Msg = { p: string; t: number; o: number; h: number; l: number; c: number; ev?: unknown[][]; st?: Record<string, unknown> };

export function parse(text: string): Msg | null {
  try {
    const s = text.slice(text.indexOf("{"), text.lastIndexOf("}") + 1);
    const j = JSON.parse(s);
    if (!j || j.aa !== 1 || !j.p || !j.t) return null;
    return { p: String(j.p).toUpperCase().replace(/[^A-Z0-9]/g, ""), t: +j.t, o: +j.o, h: +j.h, l: +j.l, c: +j.c, ev: Array.isArray(j.ev) ? j.ev : [], st: j.st ?? {} };
  } catch { return null; }
}

export function rows(m: Msg, raw: string) {
  const bt = new Date(m.t).toISOString();
  const out: Record<string, unknown>[] = [{
    uid: `${m.p}|1H|bar|${m.t}`, bar_time: bt, pair: m.p, tf: "1H", ev: "bar", price: m.c,
    info: { o: m.o, h: m.h, l: m.l, c: m.c, st: m.st }, raw: raw.slice(0, 4000),
  }];
  (m.ev ?? []).forEach((e, n) => {
    const [tf, ev, dir, level, zlo, zhi, extra] = e as [string, string, number, number, number, number, string];
    if (!tf || !ev) return;
    const num = (x: unknown) => (x === null || x === undefined || x === "" || isNaN(+x!) ? null : +x!);
    out.push({ uid: `${m.p}|${tf}|${ev}|${m.t}|${n}`, bar_time: bt, pair: m.p, tf: String(tf), ev: String(ev), dir: num(dir),
      price: m.c, level: num(level), zlo: num(zlo), zhi: num(zhi), info: extra ? { x: extra } : null });
  });
  return out;
}

type Paper = { id: number; dir: number; entry: number; sl: number; tp: number; status: string; order_type: string | null; expires_at: string | null; opened_at: string | null };
// move one virtual trade with one closed candle; conservative: on the fill candle only the stop can be hit; if a candle reaches stop and target, the stop counts
export function step(p: Paper, b: Bar): Partial<Paper> & { r?: number; exit_price?: number; closed_at?: string; why?: string } | null {
  const t = new Date(b.t).toISOString();
  const risk = Math.abs(p.entry - p.sl);
  if (p.status === "pending") {
    if (p.expires_at && b.t > Date.parse(p.expires_at)) return { status: "expired", closed_at: t, why: "order not filled in time" };
    const filled = p.dir > 0 ? b.l <= p.entry : b.h >= p.entry;
    if (!filled) return null;
    const stopHit = p.dir > 0 ? b.l <= p.sl : b.h >= p.sl;
    if (stopHit) return { status: "lost", opened_at: t, closed_at: t, exit_price: p.sl, r: -1, why: "filled and stopped in the same candle" };
    return { status: "open", opened_at: t };
  }
  if (p.status === "open") {
    const stopHit = p.dir > 0 ? b.l <= p.sl : b.h >= p.sl;
    const tpHit = p.dir > 0 ? b.h >= p.tp : b.l <= p.tp;
    if (stopHit) return { status: "lost", closed_at: t, exit_price: p.sl, r: -1, why: tpHit ? "stop and target in the same candle: stop counted" : "stop hit" };
    if (tpHit) return { status: "won", closed_at: t, exit_price: p.tp, r: Math.round((Math.abs(p.tp - p.entry) / risk) * 100) / 100, why: "target hit" };
  }
  return null;
}

async function movePaper(m: Msg) {
  const { data } = await db.from("aa_paper").select("*").eq("pair", m.p).in("status", ["pending", "open"]);
  for (const p of (data ?? []) as (Paper & { created_at: string })[]) {
    if (m.t < Date.parse(p.created_at)) continue;   // only candles that opened after the order was placed
    if (p.opened_at && Date.parse(p.opened_at) >= m.t && p.status === "open") continue;   // never use the fill candle twice
    const u = step(p, { t: m.t, o: m.o, h: m.h, l: m.l, c: m.c });
    if (u) await db.from("aa_paper").update(u).eq("id", p.id);
  }
}

export async function handle(req: Request): Promise<Response> {
  const u = new URL(req.url);
  if (req.method === "OPTIONS") return new Response(null, { headers: { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "*" } });
  const keyName = findKey();
  if (!keyName || u.searchParams.get("key") !== env(keyName)) return json({ error: "wrong or missing key" }, 401);
  if (u.searchParams.get("check")) {
    const t = await Promise.all(["aa_events", "aa_notes", "aa_paper"].map(async (n) => {
      const { count, error } = await db.from(n).select("id", { count: "exact", head: true });
      return [n, error ? "ERROR: " + error.message : `ok (${count} rows)`];
    }));
    return json({ key_secret: keyName, ...Object.fromEntries(t) });
  }
  if (req.method !== "POST") return json({ error: "POST the TradingView alert message here" }, 405);
  const text = await req.text();
  runInBackground(process(text).catch((e) => console.error("aa-event:", (e as Error).message)));
  return json({ accepted: true });
}

export async function process(text: string) {
  const m = parse(text);
  if (!m) { await db.from("aa_events").insert({ pair: "?", tf: "?", ev: "unparsed", raw: text.slice(0, 4000) }); return { parsed: false }; }
  const r = rows(m, text);
  const { error } = await db.from("aa_events").upsert(r, { onConflict: "uid", ignoreDuplicates: true });
  if (error) throw new Error(error.message);
  await movePaper(m);
  return { stored: r.length };
}

function runInBackground(p: Promise<unknown>) {
  const rt = (globalThis as unknown as { EdgeRuntime?: { waitUntil: (p: Promise<unknown>) => void } }).EdgeRuntime;
  if (rt?.waitUntil) rt.waitUntil(p);
}

if (import.meta.main) Deno.serve(handle);
