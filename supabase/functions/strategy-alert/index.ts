// Daily Observer — strategy-alert (Supabase Edge Function, single file, Verify JWT OFF)
// TradingView strategy alerts (BE Swing / BE MACD / BE Intraday, "alert() function calls only") post here.
// It stores every alert in do_strat_events and sends a Web Push to every phone in do_push_subs
// (the same subscriptions the Daily Observer app uses).
//
// Webhook URL in TradingView:  https://<project>.supabase.co/functions/v1/strategy-alert?key=<STRAT_KEY>
// Test from a browser:          …/strategy-alert?key=<STRAT_KEY>&test=1   (sends a test notification, stores nothing)
// Check the setup:              …/strategy-alert?key=<STRAT_KEY>&check=1  (which secrets it found; never shows values)
//
// Secrets (Edge Functions → Secrets): STRAT_KEY (any long random text, the same one you put in the URL).
// The VAPID private key is the one tv-signal already uses: this function finds it by name (VAPID_PRIVATE_KEY, VAPID_PRIVATE, …).
import { createClient } from "npm:@supabase/supabase-js@2.45.4";
import webpush from "npm:web-push@3.6.7";

const env = (k: string) => Deno.env.get(k) ?? "";
const VAPID_PUBLIC = env("VAPID_PUBLIC_KEY") || env("VAPID_PUBLIC") ||
  "BAOgsdSJNvxen175cWjqvGRMSR9Hk-iBm7cyNcxtDF0ZgxW445gRNcaVvXKfQDqQfUD6kqK_k7MGaEUmJa2yWuw";
const envNames = () => Object.keys(Deno.env.toObject());
const findPriv = () => {
  for (const k of ["VAPID_PRIVATE_KEY", "VAPID_PRIVATE", "WEB_PUSH_PRIVATE_KEY", "WEBPUSH_PRIVATE_KEY", "PUSH_PRIVATE_KEY"]) if (env(k)) return k;
  return envNames().find((k) => /VAPID/i.test(k) && /PRIV|SECRET/i.test(k)) ?? "";
};
const findKey = () => ["STRAT_KEY", "TV_SECRET", "TV_KEY", "WEBHOOK_KEY"].find((k) => env(k)) ?? "";
const SITE = env("SITE_URL") || "https://calexi07.github.io/Analyst/index.html";
const db = createClient(env("SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const json = (o: unknown, status = 200) =>
  new Response(JSON.stringify(o, null, 1), { status, headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" } });

// "#BE|st=SWING 4H|p=EURUSD|ev=order|…" → { st, p, ev, … }
export function parse(text: string) {
  const lines = text.replace(/\r/g, "").split("\n").map((s) => s.trim()).filter(Boolean);
  const tagLine = lines.find((l) => l.startsWith("#BE|")) ?? "";
  const tag: Record<string, string> = {};
  for (const kv of tagLine.split("|").slice(1)) { const i = kv.indexOf("="); if (i > 0) tag[kv.slice(0, i)] = kv.slice(i + 1); }
  const human = lines.filter((l) => !l.startsWith("#BE|"));
  const num = (k: string) => (tag[k] === undefined || tag[k] === "" || isNaN(+tag[k]) ? null : +tag[k]);
  return {
    ok: !!tagLine && !!tag.st && !!tag.p && !!tag.ev,
    strategy: (tag.st ?? "").split(" ")[0].toUpperCase(),   // SWING / MACD / INTRADAY
    variant: tag.st ?? "",
    pair: (tag.p ?? "").toUpperCase(), ev: tag.ev ?? "", dir: num("d"), trade_id: tag.id ?? "", what: tag.w ?? "",
    entry: num("e"), sl: num("sl"), tp: num("tp"), price: num("x"), r: num("r"), lots10k: num("l10"),
    push: tag.pu !== "0", tf: tag.tf ?? "", bar_time: num("t") ? new Date(num("t")!).toISOString() : null,
    title: human[0] ?? "", body: human.slice(1).join("\n"), raw: text.slice(0, 4000),
  };
}

async function pushAll(payload: Record<string, unknown>) {
  const priv = findPriv();
  if (!priv) return { sent: 0, error: "no VAPID private key secret found" };
  webpush.setVapidDetails(env("VAPID_SUBJECT") || "mailto:daily-observer@example.com", VAPID_PUBLIC, env(priv));
  const { data: subs, error } = await db.from("do_push_subs").select("endpoint, sub");
  if (error) return { sent: 0, error: error.message };
  let sent = 0; const gone: string[] = [];
  await Promise.all((subs ?? []).map(async (s: { endpoint: string; sub: webpush.PushSubscription }) => {
    try { await webpush.sendNotification(s.sub, JSON.stringify(payload), { TTL: 3600, urgency: "high" }); sent++; }
    catch (e) { const c = (e as { statusCode?: number }).statusCode; if (c === 404 || c === 410) gone.push(s.endpoint); }
  }));
  if (gone.length) await db.from("do_push_subs").delete().in("endpoint", gone);
  return { sent, removed: gone.length, phones: subs?.length ?? 0 };
}


// a closed trade → one row in Trades (do_backtests), run "BE Swing 4H" / "BE MACD" / "BE Intraday" (same names as the CSV import in the app)
const RUN: Record<string, string> = { SWING: "BE Swing", MACD: "BE MACD", INTRADAY: "BE Intraday" };
const runName = (variant: string) => { const [k, ...rest] = variant.split(" "); return (RUN[k.toUpperCase()] ?? "BE " + k) + (rest.length ? " " + rest.join(" ") : ""); };
const buc = (iso: string) => new Date(iso).toLocaleString("sv-SE", { timeZone: "Europe/Bucharest" });   // "2026-11-23 10:05:00"
async function logTrade(a: ReturnType<typeof parse>) {
  const { data: ev } = await db.from("do_strat_events").select("ev, entry, sl, r, bar_time, at")
    .eq("variant", a.variant).eq("pair", a.pair).eq("trade_id", a.trade_id).in("ev", ["filled", "open", "partial"])
    .order("id", { ascending: false }).limit(10);
  const fill = (ev ?? []).find((e: { ev: string }) => e.ev === "filled") ?? (ev ?? []).find((e: { ev: string }) => e.ev === "open");
  if (!fill) return "no fill event found";
  const fillT = fill.bar_time ?? fill.at;
  const part = (ev ?? []).find((e: { ev: string; at: string; r: number | null }) => e.ev === "partial" && e.at >= fill.at && e.r != null);
  const r = a.r == null ? null : part ? (a.r + part.r) / 2 : a.r;   // half closed earlier: each half counts 50 %
  const [day, hms] = buc(fillT).split(" ");
  const rec = {
    run: runName(a.variant), pair: a.pair, day, entry_time: hms.slice(0, 5), direction: (a.dir ?? 0) > 0 ? "Long" : "Short",
    result: r == null ? "BE" : r >= 0.1 ? "W" : r <= -0.1 ? "L" : "BE", r: r == null ? null : Math.round(r * 100) / 100,
    entry: fill.entry, sl: fill.sl, rules_ok: true, news: [], ctx_manual: false,
    notes: `Auto from TradingView alert · exit ${a.what} ${a.bar_time ? buc(a.bar_time).slice(0, 16) : ""} @ ${a.price ?? ""}${a.trade_id.includes(" ") ? " · " + ({ EU: "Europe ORB", NY: "New York ORB", PB: "EMA20 pullback" } as Record<string, string>)[a.trade_id.split(" ")[0]] : ""}`,
  };
  const { data: dup } = await db.from("do_backtests").select("id").eq("run", rec.run).eq("pair", rec.pair).eq("day", rec.day).eq("entry_time", rec.entry_time).eq("direction", rec.direction).limit(1);
  if (dup?.length) return "already in Trades";
  const { error } = await db.from("do_backtests").insert(rec);
  return error ? "Trades insert failed: " + error.message : "added to Trades";
}

export async function handle(req: Request): Promise<Response> {
  const u = new URL(req.url);
  if (req.method === "OPTIONS") return new Response(null, { headers: { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "*" } });
  const keyName = findKey();
  if (!keyName || u.searchParams.get("key") !== env(keyName)) return json({ error: "wrong or missing key" }, 401);

  if (u.searchParams.get("check")) {
    const { count, error } = await db.from("do_strat_events").select("id", { count: "exact", head: true });
    const subs = await db.from("do_push_subs").select("endpoint", { count: "exact", head: true });
    return json({ key_secret: keyName, vapid_private_secret: findPriv() || "NOT FOUND", vapid_like_secrets: envNames().filter((k) => /VAPID|PUSH/i.test(k)),
      table_do_strat_events: error ? "ERROR: " + error.message : `ok (${count} rows)`, phones_subscribed: subs.error ? "ERROR: " + subs.error.message : subs.count });
  }
  if (u.searchParams.get("test")) {
    const res = await pushAll({ title: "BE Strategies · test", body: "Strategy alerts reach this phone. 🎯", tag: "be-test", url: SITE + "?view=strategies", ts: Date.now() });
    return json({ test: true, ...res });
  }
  if (req.method !== "POST") return json({ error: "POST the TradingView alert message here" }, 405);

  const text = await req.text();
  const a = parse(text);
  if (!a.ok) {   // not one of ours: keep it so it can be seen in the app, but do not notify
    await db.from("do_strat_events").insert({ strategy: "UNKNOWN", pair: "", ev: "unparsed", title: text.slice(0, 120), body: "", raw: text.slice(0, 4000), push: false });
    return json({ stored: true, parsed: false });
  }
  // TradingView can retry a webhook: one row per strategy · pair · event · trade · bar
  const uid = [a.variant, a.pair, a.ev, a.trade_id, a.what, a.bar_time ?? text.length].join("|");
  const { ok: _ok, ...row } = a;
  const { error } = await db.from("do_strat_events").insert({ uid, ...row });
  if (error) {
    if (/duplicate|unique/i.test(error.message)) return json({ duplicate: true });
    return json({ error: error.message }, 500);
  }
  const trade = a.ev === "closed" ? await logTrade(a) : undefined;
  if (!a.push) return json({ stored: true, push: "off for this event", trade });
  const tv = `https://www.tradingview.com/chart/?symbol=${encodeURIComponent("FOREXCOM:" + a.pair)}`;
  const res = await pushAll({ title: a.title, body: a.body, tag: `be-${a.variant}-${a.pair}-${a.trade_id}`.replace(/\s+/g, ""), url: SITE + "?view=strategies", chart: tv, ts: Date.now() });
  return json({ stored: true, trade, ...res });
}

if (import.meta.main) Deno.serve(handle);
