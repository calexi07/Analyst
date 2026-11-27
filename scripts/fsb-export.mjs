// Structure feed export for the multi-timeframe analysis (BE FSB Export → fsb_bars → data/fsb/).
// Writes one CSV per pair with the last ROWS closed 1H candles, in the same layout as the TradingView "Export chart data" file,
// plus the active Watchlist setups (do_settings wl:*) and a meta file. Seed files from manual TradingView exports
// (data/fsb/seed/<PAIR>.csv) fill the history until the webhook has collected enough; webhook rows win on the same candle.
import { mkdirSync, writeFileSync, readFileSync, existsSync } from 'node:fs';

const URL_ = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_ANON_KEY, ROWS = +(process.env.ROWS || 400);
export const PAIRS = ['EURUSD','GBPUSD','USDJPY','USDCHF','USDCAD','AUDUSD','NZDUSD','EURGBP','EURJPY','EURCHF','EURAUD','EURNZD','EURCAD',
  'GBPJPY','GBPCHF','GBPAUD','GBPNZD','GBPCAD','AUDJPY','AUDCHF','AUDNZD','AUDCAD','NZDJPY','NZDCHF','NZDCAD','CADJPY','CADCHF','CHFJPY','XAUUSD'];
export const COLS = ["D swing trend", "D swing CHoCH", "D swing BOS", "D swing pos %", "D internal trend", "D internal CHoCH", "D internal BOS", "D internal pos %", "D fractal trend", "D fractal CHoCH", "D fractal BOS", "D fractal pos %", "D zone dir (1 demand, -1 supply)", "D zone full high", "D zone full low", "D zone refined high", "D zone refined low", "4H swing trend", "4H swing CHoCH", "4H swing BOS", "4H swing pos %", "4H internal trend", "4H internal CHoCH", "4H internal BOS", "4H internal pos %", "4H fractal trend", "4H fractal CHoCH", "4H fractal BOS", "4H fractal pos %", "4H zone dir (1 demand, -1 supply)", "4H zone full high", "4H zone full low", "4H zone refined high", "4H zone refined low", "1H swing trend", "1H swing CHoCH", "1H swing BOS", "1H swing pos %", "1H internal trend", "1H internal CHoCH", "1H internal BOS", "1H internal pos %", "1H fractal trend", "1H fractal CHoCH", "1H fractal BOS", "1H fractal pos %", "1H zone dir (1 demand, -1 supply)", "1H zone full high", "1H zone full low", "1H zone refined high", "1H zone refined low"];
const H = { apikey: KEY, Authorization: `Bearer ${KEY}` };
const get = async q => { const r = await fetch(`${URL_}/rest/v1/${q}`, { headers: H }); if (!r.ok) throw new Error(`${r.status} ${await r.text()}`); return r.json(); };

// ISO time in Europe/Bucharest with its offset, like TradingView's export (2026-11-27T08:00:00+02:00)
export function bucIso(ms) {
  const d = new Date(ms), f = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Bucharest', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit', hourCycle: 'h23' });
  const p = Object.fromEntries(f.formatToParts(d).map(x => [x.type, x.value]));
  const local = Date.UTC(+p.year, +p.month - 1, +p.day, +p.hour, +p.minute, +p.second), off = Math.round((local - ms) / 6e4);
  const sg = off >= 0 ? '+' : '-', a = Math.abs(off);
  return `${p.year}-${p.month}-${p.day}T${p.hour}:${p.minute}:${p.second}${sg}${String(Math.floor(a / 60)).padStart(2, '0')}:${String(a % 60).padStart(2, '0')}`;
}
const cell = x => (x === null || x === undefined || x === '' ? '' : String(x));
const q = s => (/[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s);
export function parseCsv(text) {
  const out = []; let row = [], f = '', i = 0, inq = false;
  for (; i < text.length; i++) { const ch = text[i];
    if (inq) { if (ch === '"') { if (text[i + 1] === '"') { f += '"'; i++; } else inq = false; } else f += ch; }
    else if (ch === '"') inq = true; else if (ch === ',') { row.push(f); f = ''; }
    else if (ch === '\n' || ch === '\r') { if (ch === '\r' && text[i + 1] === '\n') i++; row.push(f); f = ''; if (row.length > 1) out.push(row); row = []; }
    else f += ch; }
  if (f !== '' || row.length) { row.push(f); out.push(row); }
  return out;
}
// seed rows keyed by candle time (ms)
export function seedRows(text) {
  const [hd, ...rs] = parseCsv(text), ix = c => hd.indexOf(c), m = new Map();
  for (const r of rs) { const t = Date.parse(r[ix('time')]); if (!isFinite(t)) continue;
    m.set(t, { t, o: r[ix('open')], h: r[ix('high')], l: r[ix('low')], c: r[ix('close')], v: COLS.map(c => (ix(c) < 0 ? '' : r[ix(c)])) }); }
  return m;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  if (!URL_ || !KEY) { console.error('Missing SUPABASE_URL or SUPABASE_ANON_KEY'); process.exit(1); }
  mkdirSync('data/fsb', { recursive: true });
  const meta = { generated_at: new Date().toISOString(), rows_per_pair: ROWS, pairs: {} };
  for (const p of PAIRS) {
    const seedF = `data/fsb/seed/${p}.csv`, m = existsSync(seedF) ? seedRows(readFileSync(seedF, 'utf8')) : new Map();
    const nSeed = m.size;
    let live = [];
    try { live = await get(`fsb_bars?select=bar_time,o,h,l,c,v&pair=eq.${p}&order=bar_time.desc&limit=${ROWS}`); }
    catch (e) { meta.errors = [...(meta.errors || []), `${p}: ${String(e.message).slice(0, 160)}`]; }
    // consistency check: where a seed candle and a webhook candle overlap, the structure columns (all but pos %) should be equal
    let same = 0, diff = 0; const diffCols = new Set();
    for (const r of live) { const t = Date.parse(r.bar_time), sd = m.get(t);
      if (sd) { let ok = true; COLS.forEach((c, i) => { if (/pos %$/.test(c)) return; const a = sd.v[i] === '' || sd.v[i] == null ? null : +sd.v[i], b = r.v[i] == null ? null : +r.v[i];
          if (!(a === b || (a != null && b != null && Math.abs(a - b) < 1e-9))) { ok = false; diffCols.add(c); } }); ok ? same++ : diff++; }
      m.set(t, { t, o: r.o, h: r.h, l: r.l, c: r.c, v: r.v }); }
    const rows = [...m.values()].sort((a, b) => a.t - b.t).slice(-ROWS);
    meta.pairs[p] = { rows: rows.length, live: live.length, seed: nSeed, last: rows.length ? bucIso(rows.at(-1).t) : null,
      seed_vs_live: same + diff ? { same, diff, cols: [...diffCols].slice(0, 12) } : null };
    if (!rows.length) continue;
    const lines = [['time', 'open', 'high', 'low', 'close', ...COLS].map(q).join(','),
      ...rows.map(r => [bucIso(r.t), r.o, r.h, r.l, r.c, ...r.v].map(cell).join(','))];
    writeFileSync(`data/fsb/${p}.csv`, lines.join('\n') + '\n');
  }
  // active Watchlist setups (the plans you keep in Daily Observer)
  let st = [];
  try { st = await get(`do_settings?select=key,value&key=like.wl:*&limit=2000`); } catch (e) { meta.errors = [...(meta.errors || []), `watchlist: ${String(e.message).slice(0, 160)}`]; }
  const allWl = st.map(r => ({ key: r.key, ...r.value })).filter(x => x && x.pair);
  const wl = allWl.filter(x => (x.status || 'active') === 'active');
  const since = new Date(Date.now() - 90 * 864e5).toISOString();
  // setups = active plans (what the MTF runs check); all = every plan of the last 90 days, any status (for the trade review)
  writeFileSync('data/fsb/watchlist.json', JSON.stringify({ generated_at: meta.generated_at, setups: wl,
    all: allWl.filter(x => (x.created || x.for_day || '') >= since.slice(0, 10)) }, null, 1) + '\n');
  meta.watchlist_active = wl.length;
  writeFileSync('data/fsb/meta.json', JSON.stringify(meta, null, 1) + '\n');
  console.log(JSON.stringify(meta));
}
