// Builds pine/bias-engine.pine: a TradingView indicator that shows the weekly fundamental bias
// and the daily checks (history) of the Forex Fundamental Bias Engine on any of the 29 tracked pairs.
// Sources: Daily Observer (Supabase do_weekly + do_settings fcheck:*) for the history, overlaid with
// the repo's imports/*.json (always the newest). Pine cannot read the internet, so the data is
// embedded in the script; this generator rewrites it after every phase and check.
import { readFileSync, writeFileSync, mkdirSync, readdirSync, existsSync } from 'node:fs';

const URL_ = process.env.SUPABASE_URL, KEY = process.env.SUPABASE_ANON_KEY;
const MAX_WEEKS = 26, MAX_CHECKS = 120;
const PAIRS = ['EURUSD','GBPUSD','USDJPY','USDCHF','USDCAD','AUDUSD','NZDUSD','EURGBP','EURJPY','EURCHF','EURAUD','EURNZD','EURCAD',
  'GBPJPY','GBPCHF','GBPAUD','GBPNZD','GBPCAD','AUDJPY','AUDCHF','AUDNZD','AUDCAD','NZDJPY','NZDCHF','NZDCAD','CADJPY','CADCHF','CHFJPY','XAUUSD'];
const CCY = ['USD','EUR','GBP','JPY','CHF','CAD','AUD','NZD','XAU'];
const WD = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'], MON = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

const norm = p => String(p || '').toUpperCase().replace(/[^A-Z]/g, '');
const wkKey = (y, w) => `${y}-W${String(w).padStart(2, '0')}`;
function mondayOf(y, w){ const j4 = new Date(Date.UTC(y, 0, 4)); const m = new Date(j4); m.setUTCDate(4 - ((j4.getUTCDay() || 7) - 1) + (w - 1) * 7); return m; }
const biasCode = b => /bull/i.test(b || '') ? 'U' : /bear/i.test(b || '') ? 'D' : 'N';
const convCode = c => /high/i.test(c || '') ? 'h' : /med/i.test(c || '') ? 'm' : /low/i.test(c || '') ? 'l' : '-';
function statusCode(s){ s = String(s || '');
  if(s.startsWith('❌') || /INVALID/i.test(s)) return 'X';
  if(s.startsWith('⚠') || /PRESSURE/i.test(s)) return 'P';
  if(s.startsWith('👀') || /WATCH/i.test(s)) return 'W';
  if(s.startsWith('⚪') || /TWO-SIDED/i.test(s)) return 'T';
  if(s.startsWith('🟡') || /FRAGILE/i.test(s)) return 'F';
  if(/STRONGER/i.test(s)) return 'S';
  if(s.startsWith('✅') || /CONFIRMED/i.test(s)) return 'C';
  return '?'; }
const clean = (s, n) => String(s || '').replace(/\[\/?[a-z]+\]/gi, '').replace(/["\\|^\n\r\t]/g, m => m === '"' ? "'" : ' ').replace(/\s+/g, ' ').trim().slice(0, n);

const weeks = new Map();   // key → { y, w, phase, pairs: {PAIR: {b, c, bs, qs}}, ccy: {CCY: score} }
const checks = new Map();  // `${date}:${slot}` → { date, slot, title, pairs: {PAIR: {s, g, hook}} }
const getWeek = (y, w) => { const k = wkKey(y, w); if(!weeks.has(k)) weeks.set(k, { y, w, phase:'', pairs:{}, ccy:{} }); return weeks.get(k); };

function addFundamentals(j, phase){
  const W = getWeek(j.valid_week.year, j.valid_week.week);
  if(phase) W.phase = phase;
  for(const [c, v] of Object.entries(j.currencies || {})) if(v && v.score != null) W.ccy[c] = Number(v.score);
  for(const p of j.pairs || []) W.pairs[norm(p.pair)] = { b:biasCode(p.bias), c:convCode(p.conviction), bs:p.base_score, qs:p.quote_score };
}
function addCheck(j){
  if(!j || !j.date || !j.pairs) return;
  const k = `${j.date}:${j.slot || 'check'}`, C = { date:j.date, slot:j.slot || 'check', title:clean(j.title, 60), pairs:{} };
  for(const p of j.pairs) C.pairs[norm(p.pair)] = { s:statusCode(p.status), g:p.today_gap ?? p.published_gap ?? null, hook:clean(p.hook, 140) };
  checks.set(k, C);
}

// 1) history from Daily Observer (if the Supabase secrets are present)
if(URL_ && KEY){
  const H = { apikey:KEY, Authorization:`Bearer ${KEY}` };
  const r1 = await fetch(`${URL_}/rest/v1/do_weekly?select=pair,year,week,bias,conviction,details&limit=20000`, { headers:H });
  if(r1.ok){ for(const r of await r1.json()){
    const p = norm(r.pair); if(!PAIRS.includes(p)) continue;
    const d = (r.details && typeof r.details === 'object') ? r.details : {}, W = getWeek(r.year, r.week);
    const bs = d.base_score != null ? Number(d.base_score) : null, qs = d.quote_score != null ? Number(d.quote_score) : null;
    W.pairs[p] = { b:biasCode(r.bias), c:convCode(r.conviction), bs, qs };
    if(bs != null) W.ccy[p.slice(0, 3)] ??= bs; if(qs != null) W.ccy[p.slice(3, 6)] ??= qs;
  } } else console.error('do_weekly', r1.status, await r1.text());
  const r2 = await fetch(`${URL_}/rest/v1/do_settings?select=key,value&key=like.fcheck:*&limit=5000`, { headers:H });
  if(r2.ok){ for(const r of await r2.json()) addCheck(r.value); } else console.error('fcheck', r2.status, await r2.text());
} else console.log('No Supabase secrets: using repo imports only');

// 2) the repo's imports (newest; a FINAL file wins over PHASE 1 for the same week)
const files = existsSync('imports') ? readdirSync('imports').filter(f => f.endsWith('.json') && f !== 'index.json') : [];
const rank = f => /final/i.test(f) ? 2 : 1;
for(const f of files.sort((a, b) => rank(a) - rank(b) || a.localeCompare(b))){
  let j; try{ j = JSON.parse(readFileSync(`imports/${f}`, 'utf8')); }catch(e){ continue; }
  if(j.format === 'daily-observer-fundamentals') addFundamentals(j, /final/i.test(f) ? 'FINAL' : /phase1/i.test(f) ? 'PHASE 1' : '');
  else if(j.format === 'daily-observer-check') addCheck(j);
}

// 3) build the Pine data
const wl = [...weeks.values()].filter(W => Object.keys(W.pairs).length).sort((a, b) => a.y - b.y || a.w - b.w).slice(-MAX_WEEKS);
const cl = [...checks.values()].sort((a, b) => (a.date + (a.slot === 'morning' ? '1' : '2')).localeCompare(b.date + (b.slot === 'morning' ? '1' : '2'))).slice(-MAX_CHECKS);
if(!wl.length){ console.error('No weekly data found'); process.exit(1); }
for(const W of wl) for(const p of PAIRS){ const x = W.pairs[p]; if(x){ if(x.bs == null && W.ccy[p.slice(0,3)] != null) x.bs = W.ccy[p.slice(0,3)]; if(x.qs == null && W.ccy[p.slice(3,6)] != null) x.qs = W.ccy[p.slice(3,6)]; } }

const L = [];
for(const W of wl){
  const sun = mondayOf(W.y, W.w); sun.setUTCDate(sun.getUTCDate() - 1);
  const rec = PAIRS.map(p => { const x = W.pairs[p]; if(!x) return '?'; const g = x.bs != null && x.qs != null ? x.bs - x.qs : ''; return `${x.b}${x.c}${g}`; }).join(',');
  const sc = CCY.map(c => W.ccy[c] != null ? W.ccy[c] : '?').join(',');
  L.push(`    array.push(wT, timestamp("UTC", ${sun.getUTCFullYear()}, ${sun.getUTCMonth() + 1}, ${sun.getUTCDate()}, 21, 0))`);
  L.push(`    array.push(wN, "${wkKey(W.y, W.w)}${W.phase ? ' ' + W.phase : ''}")`);
  L.push(`    array.push(wD, "${rec}")`);
  L.push(`    array.push(wS, "${sc}")`);
}
for(const C of cl){
  const [y, m, d] = C.date.split('-').map(Number), hh = C.slot === 'morning' ? 6 : 19, mm = C.slot === 'morning' ? 30 : 55;
  const dt = new Date(Date.UTC(y, m - 1, d)), name = `${WD[dt.getUTCDay()]} ${d} ${MON[m - 1]} · ${C.slot}`;
  const rec = PAIRS.map(p => { const x = C.pairs[p]; return x ? `${x.s}${x.g ?? ''}` : '?'; }).join(',');
  L.push(`    array.push(cT, timestamp("Europe/Bucharest", ${y}, ${m}, ${d}, ${hh}, ${mm}))`);
  L.push(`    array.push(cN, "${name}")`);
  L.push(`    array.push(cD, "${rec}")`);
}
const lastC = cl.at(-1);
const hooks = lastC ? PAIRS.map(p => lastC.pairs[p]?.hook || '-').join('|') : '';
const gen = new Date().toISOString().slice(0, 16).replace('T', ' ') + ' UTC';
const first = wl[0], last = wl.at(-1);

const tpl = readFileSync('scripts/pine-template.pine', 'utf8')
  .replace('{{GENERATED}}', gen)
  .replace('{{COVERAGE}}', `${wkKey(first.y, first.w)} → ${wkKey(last.y, last.w)} (${wl.length} weeks), ${cl.length} daily checks`)
  .replace('{{PAIRS}}', PAIRS.map(p => `"${p}"`).join(', '))
  .replace('{{PAIR_OPTIONS}}', ['"Auto"', ...PAIRS.map(p => `"${p}"`)].join(', '))
  .replace('{{CCY}}', CCY.map(c => `"${c}"`).join(', '))
  .replace('{{DATA}}', L.join('\n'))
  .replace('{{LAST_HOOKS}}', hooks)
  .replace('{{LAST_CHECK_INDEX}}', String(cl.length - 1))
  .replace('{{STAMP}}', gen);
mkdirSync('pine', { recursive:true });
writeFileSync('pine/bias-engine.pine', tpl);
writeFileSync('pine/bias-engine.json', JSON.stringify({ generated_at:gen, weeks:wl.map(W => wkKey(W.y, W.w) + (W.phase ? ' ' + W.phase : '')), checks:cl.map(C => `${C.date} ${C.slot}`), chars:tpl.length }, null, 1));
console.log(`pine/bias-engine.pine: ${wl.length} weeks, ${cl.length} checks, ${tpl.length} chars`);
