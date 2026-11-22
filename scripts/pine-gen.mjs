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
const clean = (s, n) => String(s || '').replace(/\[\/?[a-z]+\]/gi, '').replace(/["\\|^~\n\r\t]/g, m => m === '"' ? "'" : ' ').replace(/\s+/g, ' ').trim().slice(0, n);

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
  const k = `${j.date}:${j.slot || 'check'}`, C = { date:j.date, slot:j.slot || 'check', title:clean(j.title, 60), pairs:{}, ccy:{} };
  for(const [c, v] of Object.entries(j.currencies || {})) C.ccy[c] = { st:clean(v.status, 40), note:clean(v.note, 170) };
  for(const p of j.pairs) C.pairs[norm(p.pair)] = { s:statusCode(p.status), g:p.today_gap ?? p.published_gap ?? null, hook:clean(p.hook, 170) };
  checks.set(k, C);
}

// 0) saved history (pine/history.json) so a Daily Observer outage never shrinks the indicator's data
if(existsSync('pine/history.json')){ try{ const h = JSON.parse(readFileSync('pine/history.json', 'utf8'));
  for(const W of h.weeks || []) weeks.set(wkKey(W.y, W.w), W);
  for(const C of h.checks || []) checks.set(`${C.date}:${C.slot}`, C); }catch(e){ console.error('history.json unreadable', e.message); } }
let supaOk = false;
// 1) history from Daily Observer (if the Supabase secrets are present) — only the fields the indicator needs, to keep traffic small
if(URL_ && KEY){
  const H = { apikey:KEY, Authorization:`Bearer ${KEY}` };
  const r1 = await fetch(`${URL_}/rest/v1/do_weekly?select=pair,year,week,bias,conviction,base_score:details->base_score,quote_score:details->quote_score&limit=20000`, { headers:H });
  if(r1.ok){ supaOk = true; for(const r of await r1.json()){
    const p = norm(r.pair); if(!PAIRS.includes(p)) continue;
    const d = r, W = getWeek(r.year, r.week);
    const bs = d.base_score != null ? Number(d.base_score) : null, qs = d.quote_score != null ? Number(d.quote_score) : null;
    W.pairs[p] = { b:biasCode(r.bias), c:convCode(r.conviction), bs, qs };
    if(bs != null) W.ccy[p.slice(0, 3)] ??= bs; if(qs != null) W.ccy[p.slice(3, 6)] ??= qs;
  } } else console.error('do_weekly', r1.status, await r1.text());
  // only checks newer than the saved history are fetched
  const known = [...checks.keys()].map(k => k.split(':')[0]).sort().at(-1) || '2000-01-01';
  const r2 = await fetch(`${URL_}/rest/v1/do_settings?select=key,value&key=gte.fcheck:${known}&key=like.fcheck:*&limit=500`, { headers:H });
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
// texts for the hover notes: newest checks first, within a budget so the script stays under TradingView's size limit
const TEXT_BUDGET = 50000; let used = 0;
for(const C of [...cl].reverse()){
  const ccyTxt = CCY.map(c => C.ccy[c] ? `${C.ccy[c].st || '-'}~${C.ccy[c].note || '-'}` : '-~-').join('|');
  const hookTxt = PAIRS.map(p => C.pairs[p]?.hook || '-').join('|');
  C.ccyTxt = used + ccyTxt.length <= TEXT_BUDGET ? ccyTxt : ''; used += C.ccyTxt.length;
  C.hookTxt = used + hookTxt.length <= TEXT_BUDGET ? hookTxt : ''; used += C.hookTxt.length;
}
for(const C of cl){
  const [y, m, d] = C.date.split('-').map(Number), hh = C.slot === 'morning' ? 6 : 19, mm = C.slot === 'morning' ? 30 : 55;
  const dt = new Date(Date.UTC(y, m - 1, d)), name = `${WD[dt.getUTCDay()]} ${d} ${MON[m - 1]} · ${C.slot}`;
  const rec = PAIRS.map(p => { const x = C.pairs[p]; return x ? `${x.s}${x.g ?? ''}` : '?'; }).join(',');
  L.push(`    array.push(cT, timestamp("Europe/Bucharest", ${y}, ${m}, ${d}, 0, 0))`);   // shown on the candle that opens at 00:00 Bucharest that day
  L.push(`    array.push(cN, "${name}")`);
  L.push(`    array.push(cD, "${rec}")`);
  L.push(`    array.push(cH, "${C.hookTxt}")`);
  L.push(`    array.push(cC, "${C.ccyTxt}")`);
}
const lastC = cl.at(-1);
const hooks = lastC ? PAIRS.map(p => lastC.pairs[p]?.hook || '-').join('|') : '';
const gen = new Date().toISOString().slice(0, 16).replace('T', ' ') + ' UTC';
const first = wl[0], last = wl.at(-1);

// Pine rejects one very long if block ("The if statement is too long"): one week or one check per block
function dataBlocks(lines){
  // Pine limits both one if block and the script's main body, so each week / check is a small function, called once on the first bar
  const fns = []; let cur = [], size = 0;
  const flush = () => { if(cur.length){ fns.push(cur); cur = []; size = 0; } };
  for(const ln of lines){
    if(cur.length && (/array\.push\((wT|cT),/.test(ln) || size + ln.length > 6000)) flush();
    cur.push(ln); size += ln.length;
  }
  flush();
  const out = [];
  fns.forEach((body, i) => out.push(`f_data${i}() =>`, ...body, '    0'));
  out.push('if barstate.isfirst');
  fns.forEach((_, i) => out.push(`    f_data${i}()`));
  return out.join('\n');
}
const ORDERS = String.raw`
// ───────── strategy orders (strategy build only): the same setup as a real order, 1% risk, for the Strategy Tester export ─────────
float stRisk = input.float(1.0, "Risk per trade (% of equity)", minval = 0.1, maxval = 5, step = 0.1, group = "Strategy")
// status of the latest daily check for this pair at this time
f_ckNow() =>
    string out = "none"
    if pIdx >= 0 and array.size(cT) > 0
        for j = 0 to array.size(cT) - 1
            if array.get(cT, j) <= time
                string r = f_item(array.get(cD, j), pIdx)
                out := r == "?" ? out : f_sname(str.substring(r, 0, 1))
    out
float seRiskP = math.abs(seSL - seEnt)
if seAct and seSt == 2 and seRiskP > 0 and strategy.position_size == 0
    float q = strategy.equity * stRisk / 100 / (seRiskP * syminfo.pointvalue)
    string cmt = pName + " | " + (seDir < 0 ? "short" : "long") + " | bias " + f_bname(b) + " " + f_cname(cv) + " gap " + f_sg(g) + " | check " + f_ckNow() + " | sweep " + seHr + " " + seSess + " | SL " + str.tostring(f_sePips(seRiskP)) + "p | POC after " + str.tostring(sePocH, "#.#") + "h"
    strategy.entry("Setup", seDir < 0 ? strategy.short : strategy.long, qty = q, limit = seEnt, comment = cmt)
    strategy.exit("Exit", "Setup", stop = seSL, limit = seTP, comment_loss = "SL −1R", comment_profit = "TP +" + str.tostring(seRR) + "R")
if seAct and seSt != 2 and strategy.position_size == 0
    strategy.cancel("Setup")
`;
const tpl = readFileSync('scripts/pine-template.pine', 'utf8')
  .replace('{{GENERATED}}', gen)
  .replace('{{COVERAGE}}', `${wkKey(first.y, first.w)} → ${wkKey(last.y, last.w)} (${wl.length} weeks), ${cl.length} daily checks`)
  .replace('{{PAIRS}}', PAIRS.map(p => `"${p}"`).join(', '))
  .replace('{{PAIR_OPTIONS}}', ['"Auto"', ...PAIRS.map(p => `"${p}"`)].join(', '))
  .replace('{{CCY}}', CCY.map(c => `"${c}"`).join(', '))
  .replace('{{DATA}}', dataBlocks(L))
  .replace('{{LAST_HOOKS}}', hooks)
  .replace('{{LAST_CHECK_INDEX}}', String(cl.length - 1))
  .replace('{{STAMP}}', gen);
mkdirSync('pine', { recursive:true });
writeFileSync('pine/bias-engine.pine', tpl);
// the same script as a TradingView strategy (Strategy Tester → List of trades → Export), so the setup rules can be measured
const strat = tpl
  .replace(/indicator\("Bias Engine · weekly bias & daily checks", shorttitle = "Bias Engine", overlay = true,/, 'strategy("Bias Engine · setup strategy (sweep → POC → 0.5)", shorttitle = "BE Setups", overlay = true, initial_capital = 10000, pyramiding = 0, process_orders_on_close = false, margin_long = 1, margin_short = 1, commission_type = strategy.commission.percent, commission_value = 0.005, slippage = 0,')
  .replace('// {{STRATEGY_ORDERS}}', ORDERS)
  .replace(/^alertcondition\(.*$/gm, '// (alertcondition is not available in strategies; use alert() events)');
writeFileSync('pine/bias-engine-strategy.pine', strat);
const ALERTS = existsSync('scripts/pine-alerts.pine') ? readFileSync('scripts/pine-alerts.pine', 'utf8').split('//@@TRACK\n') : null;
const withAlerts = src => ALERTS ? src.replace('// {{ALERT_FUNCS}}\n', ALERTS[0].replace('//@@FUNCS\n', '')).replace('// {{ALERT_TRACK}}\n', ALERTS[1]) : src;
// the swing test bench (Daily chart): same data, its own template
if(existsSync('scripts/pine-swing-template.pine')){
  const sw = withAlerts(readFileSync('scripts/pine-swing-template.pine', 'utf8'))
    .replace('{{GENERATED}}', gen)
    .replace('{{COVERAGE}}', `${wkKey(first.y, first.w)} → ${wkKey(last.y, last.w)} (${wl.length} weeks), ${cl.length} daily checks`)
    .replace('{{PAIRS}}', PAIRS.map(p => `"${p}"`).join(', '))
    .replace('{{PAIR_OPTIONS}}', ['"Auto"', ...PAIRS.map(p => `"${p}"`)].join(', '))
    .replace('{{CCY}}', CCY.map(c => `"${c}"`).join(', '))
    .replace('{{DATA}}', dataBlocks(L));
  writeFileSync('pine/bias-swing.pine', sw);
  // the same strategy with signal candles of 1H and 15m (defaults from the bias-week grid, 22 Nov)
  const variant = (src, title, short, note, sets) => {
    let o = src.replace('strategy("Bias Engine · swing test bench", shorttitle = "BE Swing"', `strategy("${title}", shorttitle = "${short}"`)
      .replace('// Forex Fundamental Bias Engine — swing strategy test bench (4H or Daily chart, holds 3–4 days).', `// Forex Fundamental Bias Engine — ${note}`);
    for (const [label, from, to] of sets) {
      const re = new RegExp(`input\\.(string|float|int|bool)\\(${from.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}, "${label.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}"`);
      if (!re.test(o)) throw new Error(`swing variant ${short}: input "${label}" with default ${from} not found`);
      o = o.replace(re, (m0, ty) => `input.${ty}(${to}, "${label}"`);
    }
    return o;
  };
  writeFileSync('pine/bias-swing-1h.pine', variant(sw, 'Bias Engine · swing 1H', 'BE Swing 1H',
    'swing strategy on 1H signal candles (1H chart, holds hours to 2 days). Defaults: bias-week grid, USD pairs W40–W47.', [
      ['Signal timeframe', '"4H"', '"1H"'], ['Hours to wait after an exit', '24', '12'], ['ATR multiple', '1.0', '1.0'],
      ['Take profit (R), 0 = none', '4.0', '6.0'], ['Trailing distance (ATR ×)', '0.75', '1.5'], ['Tighten the trailing to (ATR ×), 0 = off', '0.5', '0.0']]));
  writeFileSync('pine/bias-swing-15m.pine', variant(sw, 'Bias Engine · swing 15m', 'BE Swing 15m',
    'swing strategy on 15m signal candles (15m chart, intraday to 1 day). Defaults: bias-week grid on EURUSD only (other pairs untested).', [
      ['Signal timeframe', '"4H"', '"15m"'], ['Direction from', '"Both must agree"', '"Fundamental bias"'], ['Price confirmation', '"Close vs 20-day SMA"', '"None"'],
      ['Hours to wait after an exit', '24', '4'], ['ATR multiple', '1.0', '1.0'], ['Take profit (R), 0 = none', '4.0', '6.0'],
      ['Trailing stop', '"From the close (always on)"', '"Off"']]));
}
// the Bias Day intraday strategy (1H chart): same data, its own template
if(existsSync('scripts/pine-biasday-template.pine')){
  const bd = readFileSync('scripts/pine-biasday-template.pine', 'utf8')
    .replace('{{GENERATED}}', gen)
    .replace('{{COVERAGE}}', `${wkKey(first.y, first.w)} → ${wkKey(last.y, last.w)} (${wl.length} weeks), ${cl.length} daily checks`)
    .replace('{{PAIRS}}', PAIRS.map(p => `"${p}"`).join(', '))
    .replace('{{PAIR_OPTIONS}}', ['"Auto"', ...PAIRS.map(p => `"${p}"`)].join(', '))
    .replace('{{CCY}}', CCY.map(c => `"${c}"`).join(', '))
    .replace('{{DATA}}', dataBlocks(L));
  writeFileSync('pine/bias-biasday.pine', bd);
}
// the SMC 5m strategy (LuxAlgo CHoCH → OB): same data, its own template
if(existsSync('scripts/pine-smc5-template.pine')){
  const sm = readFileSync('scripts/pine-smc5-template.pine', 'utf8')
    .replace('{{GENERATED}}', gen)
    .replace('{{COVERAGE}}', `${wkKey(first.y, first.w)} → ${wkKey(last.y, last.w)} (${wl.length} weeks), ${cl.length} daily checks`)
    .replace('{{PAIRS}}', PAIRS.map(p => `"${p}"`).join(', '))
    .replace('{{PAIR_OPTIONS}}', ['"Auto"', ...PAIRS.map(p => `"${p}"`)].join(', '))
    .replace('{{CCY}}', CCY.map(c => `"${c}"`).join(', '))
    .replace('{{DATA}}', dataBlocks(L));
  writeFileSync('pine/bias-smc5.pine', sm);
}
// the supply / demand zones indicator: same data, its own template
if(existsSync('scripts/pine-zones-template.pine')){
  const zn = readFileSync('scripts/pine-zones-template.pine', 'utf8')
    .replace('{{GENERATED}}', gen)
    .replace('{{COVERAGE}}', `${wkKey(first.y, first.w)} → ${wkKey(last.y, last.w)} (${wl.length} weeks), ${cl.length} daily checks`)
    .replace('{{PAIRS}}', PAIRS.map(p => `"${p}"`).join(', '))
    .replace('{{PAIR_OPTIONS}}', ['"Auto"', ...PAIRS.map(p => `"${p}"`)].join(', '))
    .replace('{{CCY}}', CCY.map(c => `"${c}"`).join(', '))
    .replace('{{DATA}}', dataBlocks(L));
  writeFileSync('pine/bias-zones.pine', zn);
}
// the intraday ORB strategy (5m chart): same data, its own template
if(existsSync('scripts/pine-intraday-template.pine')){
  const it = withAlerts(readFileSync('scripts/pine-intraday-template.pine', 'utf8'))
    .replace('{{GENERATED}}', gen)
    .replace('{{COVERAGE}}', `${wkKey(first.y, first.w)} → ${wkKey(last.y, last.w)} (${wl.length} weeks), ${cl.length} daily checks`)
    .replace('{{PAIRS}}', PAIRS.map(p => `"${p}"`).join(', '))
    .replace('{{PAIR_OPTIONS}}', ['"Auto"', ...PAIRS.map(p => `"${p}"`)].join(', '))
    .replace('{{CCY}}', CCY.map(c => `"${c}"`).join(', '))
    .replace('{{DATA}}', dataBlocks(L));
  writeFileSync('pine/bias-intraday.pine', it);
}
// the sweep strategy (1H chart): same data, its own template
if(existsSync('scripts/pine-sweep-template.pine')){
  const sp = readFileSync('scripts/pine-sweep-template.pine', 'utf8')
    .replace('{{GENERATED}}', gen)
    .replace('{{COVERAGE}}', `${wkKey(first.y, first.w)} → ${wkKey(last.y, last.w)} (${wl.length} weeks), ${cl.length} daily checks`)
    .replace('{{PAIRS}}', PAIRS.map(p => `"${p}"`).join(', '))
    .replace('{{PAIR_OPTIONS}}', ['"Auto"', ...PAIRS.map(p => `"${p}"`)].join(', '))
    .replace('{{CCY}}', CCY.map(c => `"${c}"`).join(', '))
    .replace('{{DATA}}', dataBlocks(L));
  writeFileSync('pine/bias-sweep.pine', sp);
}
// the MACD strategy (1H chart): same data, its own template
if(existsSync('scripts/pine-macd-template.pine')){
  const mc = withAlerts(readFileSync('scripts/pine-macd-template.pine', 'utf8'))
    .replace('{{GENERATED}}', gen)
    .replace('{{COVERAGE}}', `${wkKey(first.y, first.w)} → ${wkKey(last.y, last.w)} (${wl.length} weeks), ${cl.length} daily checks`)
    .replace('{{PAIRS}}', PAIRS.map(p => `"${p}"`).join(', '))
    .replace('{{PAIR_OPTIONS}}', ['"Auto"', ...PAIRS.map(p => `"${p}"`)].join(', '))
    .replace('{{CCY}}', CCY.map(c => `"${c}"`).join(', '))
    .replace('{{DATA}}', dataBlocks(L));
  writeFileSync('pine/bias-macd.pine', mc);
}
// the Quasimodo strategy (15m chart): same data, its own template
if(existsSync('scripts/pine-qm-template.pine')){
  const qm = readFileSync('scripts/pine-qm-template.pine', 'utf8')
    .replace('{{GENERATED}}', gen)
    .replace('{{COVERAGE}}', `${wkKey(first.y, first.w)} → ${wkKey(last.y, last.w)} (${wl.length} weeks), ${cl.length} daily checks`)
    .replace('{{PAIRS}}', PAIRS.map(p => `"${p}"`).join(', '))
    .replace('{{PAIR_OPTIONS}}', ['"Auto"', ...PAIRS.map(p => `"${p}"`)].join(', '))
    .replace('{{CCY}}', CCY.map(c => `"${c}"`).join(', '))
    .replace('{{DATA}}', dataBlocks(L));
  writeFileSync('pine/bias-qm.pine', qm);
}
// the CISD indicator turned into a strategy (WillyAlgoTrader logic + engine bias)
if(existsSync('scripts/pine-cisd-template.pine')){
  const cs = readFileSync('scripts/pine-cisd-template.pine', 'utf8')
    .replace('{{GENERATED}}', gen)
    .replace('{{COVERAGE}}', `${wkKey(first.y, first.w)} → ${wkKey(last.y, last.w)} (${wl.length} weeks), ${cl.length} daily checks`)
    .replace('{{PAIRS}}', PAIRS.map(p => `"${p}"`).join(', '))
    .replace('{{PAIR_OPTIONS}}', ['"Auto"', ...PAIRS.map(p => `"${p}"`)].join(', '))
    .replace('{{CCY}}', CCY.map(c => `"${c}"`).join(', '))
    .replace('{{DATA}}', dataBlocks(L));
  writeFileSync('pine/bias-cisd.pine', cs);
}
// the structure strategy (1H chart): same data, its own template
if(existsSync('scripts/pine-structure-template.pine')){
  const st = readFileSync('scripts/pine-structure-template.pine', 'utf8')
    .replace('{{GENERATED}}', gen)
    .replace('{{COVERAGE}}', `${wkKey(first.y, first.w)} → ${wkKey(last.y, last.w)} (${wl.length} weeks), ${cl.length} daily checks`)
    .replace('{{PAIRS}}', PAIRS.map(p => `"${p}"`).join(', '))
    .replace('{{PAIR_OPTIONS}}', ['"Auto"', ...PAIRS.map(p => `"${p}"`)].join(', '))
    .replace('{{CCY}}', CCY.map(c => `"${c}"`).join(', '))
    .replace('{{DATA}}', dataBlocks(L));
  writeFileSync('pine/bias-structure.pine', st);
}
writeFileSync('pine/history.json', JSON.stringify({ saved_at:gen, daily_observer:supaOk ? 'ok' : 'unavailable (history kept from the last good run)',
  weeks:[...weeks.values()].filter(W => Object.keys(W.pairs).length).sort((a, b) => a.y - b.y || a.w - b.w),
  checks:[...checks.values()].sort((a, b) => (a.date + a.slot).localeCompare(b.date + b.slot)) }));
writeFileSync('pine/bias-engine.json', JSON.stringify({ generated_at:gen, weeks:wl.map(W => wkKey(W.y, W.w) + (W.phase ? ' ' + W.phase : '')), checks:cl.map(C => `${C.date} ${C.slot}`), chars:tpl.length }, null, 1));
console.log(`pine/bias-engine.pine: ${wl.length} weeks, ${cl.length} checks, ${tpl.length} chars`);
