// Strategy trades export (BE Swing / BE MACD / BE Intraday / BE Bias Day) for the strategy review.
// Reads do_backtests rows whose run starts with "BE " (TradingView imports + trades added by the strategy-alert function)
// and the alert stream do_strat_events, and writes exports/strategy-trades.json and exports/strategy-events.json.
import { mkdirSync, writeFileSync } from 'node:fs';
const URL_ = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_ANON_KEY;
if (!URL_ || !KEY) { console.error('Missing SUPABASE_URL or SUPABASE_ANON_KEY'); process.exit(1); }
const H = { apikey: KEY, Authorization: `Bearer ${KEY}` };
async function all(path) {
  const out = [];
  for (let from = 0; ; from += 1000) {
    const r = await fetch(`${URL_}/rest/v1/${path}`, { headers: { ...H, Range: `${from}-${from + 999}` } });
    if (!r.ok) throw new Error(`${path}: ${r.status} ${await r.text()}`);
    const j = await r.json(); out.push(...j); if (j.length < 1000) break;
  }
  return out;
}
const now = new Date().toISOString();
const trades = await all('do_backtests?select=*&run=like.BE%20*&order=day.asc,entry_time.asc');
let events = [], evErr = null;
try { events = await all(`do_strat_events?select=id,at,bar_time,strategy,variant,pair,tf,ev,dir,trade_id,what,entry,sl,tp,price,r,lots10k,done&at=gte.${new Date(Date.now() - 90 * 864e5).toISOString()}&order=id.asc`); }
catch (e) { evErr = String(e.message || e); }
mkdirSync('exports', { recursive: true });
writeFileSync('exports/strategy-trades.json', JSON.stringify({ format: 'daily-observer-strategy-trades', version: 1, generated_at: now,
  note: 'Closed strategy trades in Daily Observer → Trades (run = BE Swing 4H / BE MACD / BE Intraday / BE Bias Day). Source: TradingView CSV imports (backtest) and the strategy-alert function (live alerts, notes start with "Auto from TradingView alert"). r = result in R; day/entry_time = Bucharest.',
  count: trades.length, trades }, null, 1));
writeFileSync('exports/strategy-events.json', JSON.stringify({ format: 'daily-observer-strategy-events', version: 1, generated_at: now, days: 90, error: evErr, count: events.length, events }, null, 1));
console.log(`strategy trades: ${trades.length}; events (90 days): ${events.length}${evErr ? ' — events error: ' + evErr : ''}`);
