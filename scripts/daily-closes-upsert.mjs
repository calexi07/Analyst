// Writes missing daily closes into Daily Observer (Supabase do_daily: daily_change %, daily_pips), from imports/daily-closes-YYYY-MM-DD.json.
// Only these two columns are written; observations and trade fields on existing rows are left as they are.
import { readFileSync } from 'node:fs';
const URL_ = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_ANON_KEY, FILE = process.env.FILE;
if (!URL_ || !KEY || !FILE) { console.error('Missing SUPABASE_URL, SUPABASE_ANON_KEY or FILE'); process.exit(1); }
const j = JSON.parse(readFileSync(FILE, 'utf8'));
const rows = j.rows.map(r => ({ pair: r.pair, day: r.day, daily_change: r.daily_change, daily_pips: r.daily_pips }));
const res = await fetch(`${URL_}/rest/v1/do_daily?on_conflict=pair,day`, { method: 'POST',
  headers: { apikey: KEY, Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json', Prefer: 'resolution=merge-duplicates,return=representation' },
  body: JSON.stringify(rows) });
const txt = await res.text();
if (!res.ok) { console.error('Supabase error', res.status, txt); process.exit(1); }
const back = JSON.parse(txt);
console.log(`Written ${back.length} rows for ${[...new Set(rows.map(r => r.day))].join(', ')}`);
for (const r of back) console.log(r.pair, r.day, r.daily_change, r.daily_pips);
