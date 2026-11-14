// Weekly price-action export for the Forex Fundamental Bias Engine (Phase 3).
// Builds the same JSON as the "Export price action" button in Daily Observer
// (format daily-observer-price-action v2) from the do_daily table, and saves it in exports/.
import { mkdirSync, writeFileSync } from 'node:fs';

const URL_ = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_ANON_KEY;
if (!URL_ || !KEY) { console.error('Missing SUPABASE_URL or SUPABASE_ANON_KEY'); process.exit(1); }

const PAIRS = ['EURUSD','GBPUSD','USDJPY','USDCHF','USDCAD','AUDUSD','NZDUSD',
  'EURGBP','EURJPY','EURCHF','EURCAD','EURAUD','EURNZD',
  'GBPJPY','GBPCHF','GBPCAD','GBPAUD','GBPNZD',
  'AUDJPY','AUDCHF','AUDCAD','AUDNZD','NZDJPY','NZDCHF','NZDCAD','CADJPY','CADCHF','CHFJPY','XAUUSD'];
const MON = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const WD = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
const iso = d => d.toISOString().slice(0, 10);
function isoWeek(dt) { const d = new Date(Date.UTC(dt.getUTCFullYear(), dt.getUTCMonth(), dt.getUTCDate()));
  const day = d.getUTCDay() || 7; d.setUTCDate(d.getUTCDate() + 4 - day);
  const y = d.getUTCFullYear(), w = Math.ceil(((d - Date.UTC(y, 0, 1)) / 864e5 + 1) / 7); return { year: y, week: w }; }
function mondayOf(y, w) { const j4 = new Date(Date.UTC(y, 0, 4)); const m = new Date(j4); m.setUTCDate(4 - ((j4.getUTCDay() || 7) - 1) + (w - 1) * 7); return m; }

// Week: WEEK=2026-W46 if given (manual run), otherwise the last completed Mon–Fri week (Friday from 21:00 UTC, after the close, counts as completed).
let y, w; const arg = (process.env.WEEK || '').match(/(\d{4})-?W(\d{1,2})/i);
if (arg) { y = +arg[1]; w = +arg[2]; }
else { const d = new Date(); const dow = d.getUTCDay(); if (!(dow === 6 || dow === 0 || (dow === 5 && d.getUTCHours() >= 21))) d.setUTCDate(d.getUTCDate() - 7); ({ year: y, week: w } = isoWeek(d)); }
const mon = mondayOf(y, w), days = [0,1,2,3,4].map(i => { const d = new Date(mon); d.setUTCDate(mon.getUTCDate() + i); return iso(d); });
const label = ds => { const d = new Date(ds + 'T00:00:00Z'); return `${WD[d.getUTCDay()]} ${String(d.getUTCDate()).padStart(2,'0')} ${MON[d.getUTCMonth()]}`; };

const q = `${URL_}/rest/v1/do_daily?select=pair,day,daily_change&day=gte.${days[0]}&day=lte.${days[4]}&limit=10000`;
const res = await fetch(q, { headers: { apikey: KEY, Authorization: `Bearer ${KEY}` } });
if (!res.ok) { console.error('Supabase error', res.status, await res.text()); process.exit(1); }
const rows = await res.json();
const by = new Map(rows.map(r => [`${r.pair}|${r.day}`, r.daily_change]));
const pairs = [...new Set([...PAIRS, ...rows.map(r => r.pair)])];

const closes = {}, missing = [], ccy = {};
for (const p of pairs) {
  const row = {}; let sum = 0, n = 0;
  for (const ds of days) { const v = by.get(`${p}|${ds}`); if (v != null) { row[label(ds)] = Number(v); sum += Number(v); n++; } }
  if (!n) { missing.push(p); continue; }
  row.week_total = +sum.toFixed(2); row.days_logged = `${n}/5`; closes[p] = row;
  for (const [c, s] of [[p.slice(0,3), 1], [p.slice(3), -1]]) { (ccy[c] ||= { sum: 0, pairs: [] }); ccy[c].sum += s * row.week_total; ccy[c].pairs.push(p); }
}
const strength = Object.fromEntries(Object.entries(ccy).map(([c, v]) => [c, { avg_move_pct: +(v.sum / v.pairs.length).toFixed(2), from_pairs: v.pairs }])
  .sort((a, b) => b[1].avg_move_pct - a[1].avg_move_pct));
const out = {
  format: 'daily-observer-price-action', version: 2, generated_at: new Date().toISOString(),
  week: { year: y, week: w, from: days[0], to: days[4] },
  note: 'Daily close % change per pair (close vs previous close), as logged by the trader. Pairs in "pairs_not_logged" have no data here — fetch their real prices.',
  daily_closes_pct: closes, realized_currency_strength: strength, pairs_not_logged: missing,
  source: 'GitHub Action weekly-export (Supabase do_daily)'
};
const ww = String(w).padStart(2, '0'), txt = JSON.stringify(out, null, 1);
mkdirSync('exports', { recursive: true });
writeFileSync(`exports/price-action-${y}-W${ww}.json`, txt);
writeFileSync('exports/latest.json', txt);
const full = Object.values(closes).filter(r => r.days_logged === '5/5').length;
console.log(`Week ${y}-W${ww}: ${Object.keys(closes).length} pairs with data (${full} complete 5/5), ${missing.length} missing: ${missing.join(', ') || 'none'}`);
