// Daily Observer — fsb-event (Supabase Edge Function, single file, Verify JWT OFF)
// The "BE FSB Export" TradingView indicator posts one JSON message per closed 1H candle per pair (alert() "once per bar close").
// This function stores it in fsb_bars and deletes that pair's rows older than 35 days.
//
// Webhook URL in TradingView:  https://<project>.supabase.co/functions/v1/fsb-event?key=<KEY>
// Check:                        …/fsb-event?key=<KEY>&check=1   (rows per pair and last candle)
// Secret: the same key as the other webhooks (AA_KEY, STRAT_KEY, TV_SECRET or WEBHOOK_KEY — the first one set is used).
//
// Message: {"fsb":1,"p":"EURUSD","t":1764000000000,"o":1.1,"h":1.1,"l":1.1,"c":1.1,"v":[ …51 values, null = empty… ]}
import { createClient } from "npm:@supabase/supabase-js@2.45.4";

const env = (k: string) => Deno.env.get(k) ?? "";
const findKey = () => ["AA_KEY", "STRAT_KEY", "TV_SECRET", "WEBHOOK_KEY"].find((k) => env(k)) ?? "";
const json = (o: unknown, status = 200) =>
  new Response(JSON.stringify(o, null, 1), { status, headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" } });
export const KEEP_DAYS = 35;
export const NCOLS = 51;

export type Row = { pair: string; bar_time: string; o: number; h: number; l: number; c: number; v: (number | null)[] };
export function parse(text: string): Row | null {
  try {
    const j = JSON.parse(text.slice(text.indexOf("{"), text.lastIndexOf("}") + 1));
    if (!j || j.fsb !== 1 || !j.p || !j.t || !Array.isArray(j.v) || j.v.length !== NCOLS) return null;
    const num = (x: unknown) => (x === null || x === undefined || x === "" || !isFinite(+x!) ? null : +x!);
    return { pair: String(j.p).toUpperCase().replace(/[^A-Z0-9]/g, ""), bar_time: new Date(+j.t).toISOString(),
      o: +j.o, h: +j.h, l: +j.l, c: +j.c, v: j.v.map(num) };
  } catch { return null; }
}

if (import.meta.main) Deno.serve(async (req) => {
  const url = new URL(req.url), k = findKey();
  if (!k || url.searchParams.get("key") !== env(k)) return json({ ok: false, error: "bad key" }, 401);
  const db = createClient(env("SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
  if (url.searchParams.get("check")) {
    const { data, error } = await db.from("fsb_bars").select("pair,bar_time").order("bar_time", { ascending: false }).limit(5000);
    if (error) return json({ ok: false, error: error.message }, 500);
    const per: Record<string, { n: number; last: string }> = {};
    for (const r of data ?? []) { const x = per[r.pair] ??= { n: 0, last: r.bar_time }; x.n++; }
    return json({ ok: true, pairs: Object.keys(per).length, per });
  }
  const raw = await req.text(), row = parse(raw);
  if (!row) return json({ ok: false, error: "not a BE FSB Export message", got: raw.slice(0, 200) }, 400);
  const { error } = await db.from("fsb_bars").upsert(row, { onConflict: "pair,bar_time" });
  if (error) return json({ ok: false, error: error.message }, 500);
  await db.from("fsb_bars").delete().eq("pair", row.pair).lt("bar_time", new Date(Date.now() - KEEP_DAYS * 864e5).toISOString());
  return json({ ok: true, pair: row.pair, bar_time: row.bar_time });
});
