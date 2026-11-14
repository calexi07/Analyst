// Weekly volatility + reference Friday close for the Bias Engine chart kit (TradingView "Typical week" boxes).
// Runs in GitHub Actions (Saturday/Sunday). Source: Yahoo Finance chart API (FX = PAIR=X, gold = GC=F futures).
// Output: exports/fx-vol-latest.json and exports/fx-vol-YYYY-Www.json (week of the baseline Friday).
// sigma = standard deviation of the last 26 weekly log returns ending at the baseline Friday close.
const PAIRS = ["EURUSD","GBPUSD","USDJPY","USDCHF","USDCAD","AUDUSD","NZDUSD","EURGBP","EURJPY","EURCHF","EURAUD","EURNZD","EURCAD","GBPJPY","GBPCHF","GBPAUD","GBPNZD","GBPCAD","AUDJPY","AUDCHF","AUDNZD","AUDCAD","NZDJPY","NZDCHF","NZDCAD","CADJPY","CADCHF","CHFJPY","XAUUSD"];
const sym = p => p === 'XAUUSD' ? 'GC=F' : p + '=X';
const isoDay = t => new Date(t * 1000).toISOString().slice(0, 10);
const sleep = ms => new Promise(r => setTimeout(r, ms));
export async function chart(s, interval, range, base = 'https://query1.finance.yahoo.com'){
  for(let i = 0; i < 4; i++){
    const r = await fetch(`${base}/v8/finance/chart/${encodeURIComponent(s)}?interval=${interval}&range=${range}`, { headers:{ 'User-Agent':'Mozilla/5.0 (bias-engine fx-vol)' } }).catch(e => ({ ok:false, status:String(e) }));
    if(r.ok){ const j = await r.json(); const x = j?.chart?.result?.[0]; if(x?.timestamp) return x.timestamp.map((t, k) => [t, x.indicators.quote[0].close[k]]).filter(v => v[1] != null); }
    await sleep(1500 * (i + 1));
  }
  throw new Error(`Yahoo ${s} ${interval}: no data`);
}
// last completed Friday (UTC date) as of `asof` (YYYY-MM-DD, a Saturday/Sunday, or today)
export function baselineFriday(asof, afterClose = false){   // afterClose: run on a Friday after 21:30 UTC → that Friday is the baseline
  const d = new Date(asof + 'T12:00:00Z'); const back = (d.getUTCDay() + 2) % 7 || 7; // Sat→1, Sun→2, Mon→3 … Fri→7 (previous Friday)
  const f = new Date(d); f.setUTCDate(d.getUTCDate() - (d.getUTCDay() === 5 ? (afterClose ? 0 : 7) : back)); return f.toISOString().slice(0, 10);
}
export async function computePair(p, fri, base){
  const gold = p === 'XAUUSD', s = sym(p);
  const daily = await chart(s, '1d', '2y', base);
  let series;
  if(gold){
    // CME futures: Friday-dated bars are Friday settlements
    series = daily.filter(([t]) => new Date(t * 1000).getUTCDay() === 5 && isoDay(t) <= fri).slice(-27).map(([t, c]) => [isoDay(t), c]);
  } else {
    // Yahoo FX daily bars dated Monday ≈ the previous Friday's close; the baseline Friday itself comes from hourly bars
    const hourly = await chart(s, '1h', '1mo', base);
    const end = Date.parse(fri + 'T22:00:00Z') / 1000, start = Date.parse(fri + 'T00:00:00Z') / 1000;
    const last = hourly.filter(([t]) => t >= start && t < end).at(-1); if(!last) throw new Error(`${p}: no hourly bar on ${fri}`);
    const mon = daily.filter(([t]) => new Date(t * 1000).getUTCDay() === 1 && isoDay(t) < fri).slice(-26).map(([t, c]) => [isoDay(t), c]);
    series = [...mon, [fri, last[1]]];
  }
  const lr = []; for(let i = 1; i < series.length; i++) lr.push(Math.log(series[i][1] / series[i - 1][1]));
  const m = lr.reduce((a, b) => a + b, 0) / lr.length, sd = Math.sqrt(lr.reduce((a, b) => a + (b - m) ** 2, 0) / (lr.length - 1));
  const close = series.at(-1)[1];
  return { close: +close.toPrecision(7), sigma_pct: +(sd * 100).toFixed(3), n: lr.length, from: series[0][0], to: series.at(-1)[0] };
}
export function isoWeek(ds){ const d = new Date(ds + 'T12:00:00Z'); const day = d.getUTCDay() || 7; d.setUTCDate(d.getUTCDate() + 4 - day); const y = d.getUTCFullYear(); const w = Math.ceil(((d - Date.UTC(y, 0, 1)) / 864e5 + 1) / 7); return { year:y, week:w }; }
export async function run(asof, base){
  const now = new Date(), afterClose = now.toISOString().slice(0, 10) === asof && now.getUTCDay() === 5 && now.getUTCHours() * 60 + now.getUTCMinutes() >= 1290;
  const fri = baselineFriday(asof, afterClose), data = {}, errors = {};
  for(const p of PAIRS){ try{ data[p] = await computePair(p, fri, base); }catch(e){ errors[p] = String(e.message || e); } await sleep(250); }
  const k = isoWeek(fri);
  return { format:'bias-engine-fx-vol', version:1, generated_at:new Date().toISOString(), baseline_friday:fri, baseline_week:k,
    source:'Yahoo Finance chart API: FX = PAIR=X (daily bars dated Monday ≈ previous Friday close; baseline Friday close from hourly bars before 22:00 UTC); XAUUSD = COMEX GC=F futures Friday bars',
    window:'26 weekly log returns ending at the baseline Friday close', data, errors };
}
// GitHub Actions entry point
if(typeof process !== 'undefined' && process.argv?.[1]?.endsWith('fx-vol.mjs')){
  const fs = await import('node:fs');
  const asof = process.env.ASOF || new Date().toISOString().slice(0, 10);
  const out = await run(asof);
  const n = Object.keys(out.data).length;
  console.log(`baseline ${out.baseline_friday} (W${out.baseline_week.week}): ${n}/29 pairs`, out.errors);
  if(n < 25){ console.error('too many pairs missing — not writing'); process.exit(1); }
  fs.mkdirSync('exports', { recursive:true });
  const txt = JSON.stringify(out, null, 1);
  fs.writeFileSync('exports/fx-vol-latest.json', txt);
  fs.writeFileSync(`exports/fx-vol-${out.baseline_week.year}-W${String(out.baseline_week.week).padStart(2, '0')}.json`, txt);
}
