// Weekly live-trade export for the Bias Engine trade review (Phase T).
// Reads the live trades (do_backtests rows with run = 'Live') logged in Daily Observer
// and writes exports/trades-YYYY-Www.json (the week), exports/trades-latest.json (same)
// and exports/trades-history.json (every live trade, for pattern detection).
import { mkdirSync, writeFileSync } from 'node:fs';

const URL_ = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_ANON_KEY;
if (!URL_ || !KEY) { console.error('Missing SUPABASE_URL or SUPABASE_ANON_KEY'); process.exit(1); }
const iso = d => d.toISOString().slice(0, 10);
function isoWeek(dt) { const d = new Date(Date.UTC(dt.getUTCFullYear(), dt.getUTCMonth(), dt.getUTCDate()));
  const day = d.getUTCDay() || 7; d.setUTCDate(d.getUTCDate() + 4 - day);
  const y = d.getUTCFullYear(), w = Math.ceil(((d - Date.UTC(y, 0, 1)) / 864e5 + 1) / 7); return { year: y, week: w }; }
function mondayOf(y, w) { const j4 = new Date(Date.UTC(y, 0, 4)); const m = new Date(j4); m.setUTCDate(4 - ((j4.getUTCDay() || 7) - 1) + (w - 1) * 7); return m; }

// Week: WEEK=2026-W46 if given (manual run); on Friday–Sunday the current week, otherwise the last completed week.
let y, w; const arg = (process.env.WEEK || '').match(/(\d{4})-?W(\d{1,2})/i);
if (arg) { y = +arg[1]; w = +arg[2]; }
else { const d = new Date(); const dow = d.getUTCDay(); if (dow >= 1 && dow <= 4) d.setUTCDate(d.getUTCDate() - 7); ({ year: y, week: w } = isoWeek(d)); }   // Fri/Sat/Sun → the current week; Mon–Thu → last week
const mon = mondayOf(y, w), sun = new Date(mon); sun.setUTCDate(mon.getUTCDate() + 6);
const from = iso(mon), to = iso(sun);

const res = await fetch(`${URL_}/rest/v1/do_backtests?select=*&run=eq.Live&order=day.asc,entry_time.asc&limit=10000`,
  { headers: { apikey: KEY, Authorization: `Bearer ${KEY}` } });
if (!res.ok) { console.error('Supabase error', res.status, await res.text()); process.exit(1); }
// extra fields saved by the app in do_settings under btx:<trade id> (liquidity sweep day and time)
const xr = await fetch(`${URL_}/rest/v1/do_settings?select=key,value&key=like.btx:*&limit=10000`, { headers: { apikey: KEY, Authorization: `Bearer ${KEY}` } });
const extra = new Map(xr.ok ? (await xr.json()).map(r => [r.key.slice(4), r.value || {}]) : []);
const all = (await res.json()).map(t => ({ ...t, sweep_day: extra.get(String(t.id))?.sweep_day ?? null, sweep_time: extra.get(String(t.id))?.sweep_time ?? null, mae_r: extra.get(String(t.id))?.mae_r ?? null, conf_pro: extra.get(String(t.id))?.conf_pro ?? [], conf_con: extra.get(String(t.id))?.conf_con ?? [], iso_week: (({ year, week }) => `${year}-W${String(week).padStart(2, '0')}`)(isoWeek(new Date(t.day + 'T12:00:00Z'))) }));
const week = all.filter(t => t.day >= from && t.day <= to);
const ww = String(w).padStart(2, '0');
const meta = { generated_at: new Date().toISOString(), source: 'GitHub Action trades-export (Supabase do_backtests, run = Live)',
  note: 'Live trades logged by the trader in Daily Observer. entry_time and sweep_time (when the liquidity was taken) are Bucharest time. r = result in R multiples; result O = still open (r empty); mae_r = max adverse excursion in R; conf_pro / conf_con = optional confluences for and against that the trader ticked (empty = not logged).' };
const out = { format: 'daily-observer-trades', version: 1, ...meta, week: { year: y, week: w, from, to }, count: week.length, trades: week };
mkdirSync('exports', { recursive: true });
writeFileSync(`exports/trades-${y}-W${ww}.json`, JSON.stringify(out, null, 1));
writeFileSync('exports/trades-latest.json', JSON.stringify(out, null, 1));
writeFileSync('exports/trades-history.json', JSON.stringify({ format: 'daily-observer-trades-history', version: 1, ...meta, count: all.length, trades: all }, null, 1));
console.log(`Week ${y}-W${ww}: ${week.length} live trades; history: ${all.length}`);
