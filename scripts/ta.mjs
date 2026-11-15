// Technical read for the 29 Bias Engine pairs, compared with the week's fundamental bias.
// Source: Yahoo Finance hourly bars (FX = PAIR=X, gold = GC=F futures), regrouped into New-York-close
// daily bars and 4-hour bars like most FX brokers. Method: a compact version of the Technical Overlay
// rules (fractal swings, structure with BOS/CHoCH, supply/demand zones, liquidity pools and sweeps,
// premium/discount). Price never changes a fundamental score; this is context, not a trade signal.
// Output: exports/ta-latest.json and exports/ta-YYYY-MM-DD.json
import { readFileSync, writeFileSync, mkdirSync, readdirSync, existsSync } from 'node:fs';

const PAIRS = ['EURUSD','GBPUSD','USDJPY','USDCHF','USDCAD','AUDUSD','NZDUSD','EURGBP','EURJPY','EURCHF','EURAUD','EURNZD','EURCAD',
  'GBPJPY','GBPCHF','GBPAUD','GBPNZD','GBPCAD','AUDJPY','AUDCHF','AUDNZD','AUDCAD','NZDJPY','NZDCHF','NZDCAD','CADJPY','CADCHF','CHFJPY','XAUUSD'];
const sym = p => p === 'XAUUSD' ? 'GC=F' : p + '=X';
const dec = p => p === 'XAUUSD' ? 2 : p.includes('JPY') ? 3 : 5;
const sleep = ms => new Promise(r => setTimeout(r, ms));
const HOUR = 3600;

async function hourly(s){
  for(let i = 0; i < 4; i++){
    const r = await fetch(`https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(s)}?interval=60m&range=6mo`, { headers:{ 'User-Agent':'Mozilla/5.0 (bias-engine ta)' } }).catch(e => ({ ok:false }));
    if(r.ok){ const j = await r.json(), x = j?.chart?.result?.[0], q = x?.indicators?.quote?.[0];
      if(x?.timestamp && q) return x.timestamp.map((t, k) => ({ t, o:q.open[k], h:q.high[k], l:q.low[k], c:q.close[k] })).filter(b => [b.o, b.h, b.l, b.c].every(v => v != null && isFinite(v))); }
    await sleep(1500 * (i + 1));
  }
  throw new Error(`no data for ${s}`);
}

// New York offset (hours) for a unix time, cached per UTC day
const offCache = new Map();
function nyOffset(t){
  const day = Math.floor(t / 86400); if(offCache.has(day)) return offCache.get(day);
  const f = new Intl.DateTimeFormat('en-US', { timeZone:'America/New_York', hourCycle:'h23', year:'numeric', month:'2-digit', day:'2-digit', hour:'2-digit' });
  const p = Object.fromEntries(f.formatToParts(new Date((day * 86400 + 12 * 3600) * 1000)).map(x => [x.type, x.value]));
  const asUtc = Date.UTC(+p.year, +p.month - 1, +p.day, +p.hour) / 1000, off = Math.round((asUtc - (day * 86400 + 12 * 3600)) / 3600);
  offCache.set(day, off); return off;
}
// trading session: starts 17:00 New York. Returns [sessionStartUnix, hoursIntoSession]
function session(t){
  const off = nyOffset(t), ny = t + off * HOUR, shifted = ny + 7 * HOUR;          // 17:00 NY → 00:00 of the trading day
  const dayStartShifted = Math.floor(shifted / 86400) * 86400;
  return [dayStartShifted - 7 * HOUR - off * HOUR, Math.floor((shifted - dayStartShifted) / HOUR)];
}
function group(bars, keyFn, len){
  const out = []; let cur = null;
  for(const b of bars){ const [k, start] = keyFn(b.t);
    if(!cur || cur.k !== k){ if(cur) out.push(cur); cur = { k, t:start, end:start + len, o:b.o, h:b.h, l:b.l, c:b.c }; }
    else { cur.h = Math.max(cur.h, b.h); cur.l = Math.min(cur.l, b.l); cur.c = b.c; } }
  if(cur) out.push(cur);
  return out;
}
const toD1 = bars => group(bars, t => { const [s] = session(t); return [s, s]; }, 24 * HOUR).filter(b => new Date((b.t + 7 * HOUR + 12 * HOUR) * 1000).getUTCDay() !== 6);
const toH4 = bars => group(bars, t => { const [s, h] = session(t), q = Math.floor(h / 4); return [s + q * 4 * HOUR, s + q * 4 * HOUR]; }, 4 * HOUR);

function atr(b, n = 14){ if(b.length < n + 1) return null; let a = 0;
  for(let i = 1; i <= n; i++) a += Math.max(b[i].h - b[i].l, Math.abs(b[i].h - b[i-1].c), Math.abs(b[i].l - b[i-1].c)); a /= n;
  for(let i = n + 1; i < b.length; i++) a = (a * (n - 1) + Math.max(b[i].h - b[i].l, Math.abs(b[i].h - b[i-1].c), Math.abs(b[i].l - b[i-1].c))) / n;
  return a; }
function swings(b, k){ const hi = [], lo = [];
  for(let i = k; i < b.length - k; i++){ let H = true, L = true;
    for(let j = 1; j <= k; j++){ if(!(b[i].h > b[i-j].h && b[i].h >= b[i+j].h)) H = false; if(!(b[i].l < b[i-j].l && b[i].l <= b[i+j].l)) L = false; }
    if(H) hi.push({ i, p:b[i].h, t:b[i].t }); if(L) lo.push({ i, p:b[i].l, t:b[i].t }); }
  return { hi, lo }; }
// structure: walk the bars; a close beyond the latest confirmed swing = a break. Same direction = BOS, opposite = CHoCH.
function structure(b, k){
  const { hi, lo } = swings(b, k); let dir = null, last = null, sh = null, sl = null, hiI = 0, loI = 0;
  for(let i = 0; i < b.length; i++){
    while(hiI < hi.length && hi[hiI].i + k <= i){ sh = { ...hi[hiI], broken:false }; hiI++; }
    while(loI < lo.length && lo[loI].i + k <= i){ sl = { ...lo[loI], broken:false }; loI++; }
    if(sh && !sh.broken && b[i].c > sh.p){ sh.broken = true; last = { type: dir === 'down' ? 'CHoCH' : 'BOS', dir:'up', level:sh.p, t:b[i].t }; dir = 'up'; }
    if(sl && !sl.broken && b[i].c < sl.p){ sl.broken = true; last = { type: dir === 'up' ? 'CHoCH' : 'BOS', dir:'down', level:sl.p, t:b[i].t }; dir = 'down'; }
  }
  const h2 = hi.slice(-2), l2 = lo.slice(-2);
  const trend = h2.length === 2 && l2.length === 2 ? (h2[1].p > h2[0].p && l2[1].p > l2[0].p ? 'up' : h2[1].p < h2[0].p && l2[1].p < l2[0].p ? 'down' : 'range') : 'unclear';
  return { dir, trend, last, swingHigh:hi.at(-1) || null, swingLow:lo.at(-1) || null, hi, lo };
}
// supply / demand zones (base of 1–3 small-bodied bars, then a strong departure ≥ 1.5 ATR)
function zones(b, A){
  const out = [], small = x => Math.abs(x.c - x.o) <= 0.5 * (x.h - x.l || 1e-12), big = x => Math.abs(x.c - x.o) >= 0.6 * (x.h - x.l || 1e-12);
  for(let i = 0; i < b.length - 2; i++){
    for(let n = 1; n <= 3 && i + n <= b.length; n++){
      const base = b.slice(i, i + n); if(!base.every(small)) break;
      const after = b.slice(i + n, i + n + 3); if(!after.length || !after.some(big)) continue;
      const bHi = Math.max(...base.map(x => x.h)), bLo = Math.min(...base.map(x => x.l));
      const up = Math.max(...after.map(x => x.h)) - bHi, dn = bLo - Math.min(...after.map(x => x.l));
      let z = null;
      if(up >= 1.5 * A && up > dn) z = { kind:'demand', lo:bLo, hi:Math.max(...base.map(x => Math.max(x.o, x.c))), t:base[0].t, dep:up / A };
      else if(dn >= 1.5 * A) z = { kind:'supply', hi:bHi, lo:Math.min(...base.map(x => Math.min(x.o, x.c))), t:base[0].t, dep:dn / A };
      if(!z) continue;
      let status = 'fresh';
      for(let j = i + n + 3; j < b.length; j++){
        if(z.kind === 'demand'){ if(b[j].c < z.lo){ status = 'broken'; break; } if(b[j].l <= z.hi) status = 'tested'; }
        else { if(b[j].c > z.hi){ status = 'broken'; break; } if(b[j].h >= z.lo) status = 'tested'; } }
      if(status !== 'broken') out.push({ ...z, status });
      break;
    }
  }
  return out;
}
const isoWeekKey = t => { const d = new Date(t * 1000), x = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate())); const day = x.getUTCDay() || 7; x.setUTCDate(x.getUTCDate() + 4 - day); const y = x.getUTCFullYear(); return y * 100 + Math.ceil(((x - Date.UTC(y, 0, 1)) / 864e5 + 1) / 7); };

// ───────── fundamental bias of the relevant week (from the repo imports) ─────────
function isoWeek(dt){ const d = new Date(Date.UTC(dt.getUTCFullYear(), dt.getUTCMonth(), dt.getUTCDate())); const day = d.getUTCDay() || 7; d.setUTCDate(d.getUTCDate() + 4 - day); const y = d.getUTCFullYear(); return { year:y, week:Math.ceil(((d - Date.UTC(y, 0, 1)) / 864e5 + 1) / 7) }; }
function loadBias(){
  const now = new Date(), ref = new Date(now); const dow = now.getUTCDay();
  if(dow === 6) ref.setUTCDate(now.getUTCDate() + 2); else if(dow === 0) ref.setUTCDate(now.getUTCDate() + 1);   // weekend → the coming week
  const target = isoWeek(ref), key = target.year * 100 + target.week;
  const files = existsSync('imports') ? readdirSync('imports').filter(f => /^\d{4}-W\d{2}-(final|phase1)/.test(f)) : [];
  let best = null;
  for(const f of files){ let j; try{ j = JSON.parse(readFileSync('imports/' + f, 'utf8')); }catch(e){ continue; }
    if(j.format !== 'daily-observer-fundamentals') continue;
    const k = j.valid_week.year * 100 + j.valid_week.week, rank = k * 10 + (/final/.test(f) ? 2 : 1);
    if(k <= key && (!best || rank > best.rank)) best = { rank, j, phase:/final/.test(f) ? 'FINAL' : 'PHASE 1' }; }
  if(!best) return { week:null, pairs:{} };
  return { week:`${best.j.valid_week.year}-W${String(best.j.valid_week.week).padStart(2, '0')} ${best.phase}`, pairs:Object.fromEntries(best.j.pairs.map(p => [p.pair, p])) };
}

// ───────── one pair ─────────
function analyse(p, raw, fb, now){
  const D = dec(p), f = v => v == null ? null : +v.toFixed(D);
  const d1all = toD1(raw), h4all = toH4(raw), h1all = raw.map(b => ({ ...b, end:b.t + HOUR }));
  const closed = arr => arr.filter(b => b.end <= now);
  const d1 = closed(d1all), h4 = closed(h4all), h1 = closed(h1all);
  const last = raw.at(-1), price = last.c, A = atr(d1), A4 = atr(h4);
  if(!A || d1.length < 40) throw new Error('not enough daily bars');
  const sD = structure(d1, 2), s4 = structure(h4, 3), s1 = structure(h1, 3);
  // zones near price
  const zz = [...zones(d1.slice(-90), A).map(z => ({ ...z, tf:'D1' })), ...zones(h4.slice(-180), A4).map(z => ({ ...z, tf:'H4' }))];
  const dem = zz.filter(z => z.kind === 'demand' && z.hi < price && price - z.hi <= 3 * A).sort((a, b) => b.hi - a.hi);
  const sup = zz.filter(z => z.kind === 'supply' && z.lo > price && z.lo - price <= 3 * A).sort((a, b) => a.lo - b.lo);
  const inZone = zz.find(z => price >= z.lo && price <= z.hi) || null;
  // liquidity pools
  const lastD = d1.at(-1), weeks = new Map(); d1.forEach(b => { const k = isoWeekKey(b.t + 12 * HOUR); const w = weeks.get(k) || { h:-Infinity, l:Infinity }; w.h = Math.max(w.h, b.h); w.l = Math.min(w.l, b.l); weeks.set(k, w); });
  const wk = [...weeks.keys()].sort(), curW = isoWeekKey(now), prevW = wk.filter(k => k < curW).at(-1), PW = prevW ? weeks.get(prevW) : null;
  const tol = 0.1 * A, eq = (arr, kind) => { const out = []; const rec = arr.filter(s => s.t >= d1.at(-60)?.t);
    for(let i = 0; i < rec.length; i++){ const g = rec.filter(s => Math.abs(s.p - rec[i].p) <= tol); if(g.length >= 2 && !out.some(o => Math.abs(o.p - rec[i].p) <= tol)) out.push({ p: g.reduce((a, s) => a + s.p, 0) / g.length, n:g.length, t:Math.max(...g.map(s => s.t)), kind }); }
    return out; };
  const pools = [
    { name:'previous day high', side:'BSL', p:lastD.h, t:lastD.t }, { name:'previous day low', side:'SSL', p:lastD.l, t:lastD.t },
    ...(PW ? [{ name:'previous week high', side:'BSL', p:PW.h, t:0 }, { name:'previous week low', side:'SSL', p:PW.l, t:0 }] : []),
    ...eq([...sD.hi, ...s4.hi], 'h').map(e => ({ name:`equal highs (${e.n})`, side:'BSL', p:e.p, t:e.t })),
    ...eq([...sD.lo, ...s4.lo], 'l').map(e => ({ name:`equal lows (${e.n})`, side:'SSL', p:e.p, t:e.t })),
  ];
  const resting = pools.filter(x => x.side === 'BSL' ? x.p > price : x.p < price);
  const bsl = resting.filter(x => x.side === 'BSL').sort((a, b) => a.p - b.p)[0] || null, ssl = resting.filter(x => x.side === 'SSL').sort((a, b) => b.p - a.p)[0] || null;
  // latest sweep on H1/H4 in the last 3 days: wick through a pool, close back
  let sweep = null; const since = now - 3 * 86400;
  for(const [tf, arr] of [['H1', h1], ['H4', h4]]) for(const b of arr.filter(x => x.t >= since)) for(const x of pools) {
    if(x.t && x.t >= b.t) continue;
    if(x.side === 'BSL' && b.h > x.p && b.c < x.p && (!sweep || b.t > sweep.t)) sweep = { side:'BSL', name:x.name, level:x.p, tf, t:b.t };
    if(x.side === 'SSL' && b.l < x.p && b.c > x.p && (!sweep || b.t > sweep.t)) sweep = { side:'SSL', name:x.name, level:x.p, tf, t:b.t }; }
  // location in the 3-month range
  const r66 = d1.slice(-66), hi66 = Math.max(...r66.map(b => b.h)), lo66 = Math.min(...r66.map(b => b.l)), pos = (price - lo66) / (hi66 - lo66 || 1);
  // ───── compare with the fundamental bias ─────
  const bias = fb?.bias || null, want = bias === 'bullish' ? 'up' : bias === 'bearish' ? 'down' : null;
  const W = x => x === 'up' ? 'up' : x === 'down' ? 'down' : 'unclear';
  const dD = sD.dir, d4 = s4.dir, upB = want === 'up';
  const turnLvl = want ? (upB ? s4.swingHigh?.p : s4.swingLow?.p) : null;                 // H4 level whose break turns structure toward the bias
  const invLvl = want ? (upB ? sD.swingLow?.p : sD.swingHigh?.p) : null;                  // D1 level that would break the bias-side structure
  let status, head;
  if(!want){ status = 'two-sided'; head = `No fundamental lean this week; price structure is ${W(dD)} on D1 and ${W(d4)} on H4.`; }
  else if(dD === want && d4 === want){ status = 'aligned'; head = `Price agrees with the ${bias} bias: D1 and H4 structure both point ${want}.`; }
  else if(dD === want){ status = 'pullback'; head = `D1 agrees with the ${bias} bias, H4 is pulling back against it. Waiting for H4 to turn back ${want}${turnLvl != null ? ` (a 4h close ${upB ? 'above' : 'below'} ${f(turnLvl)})` : ''}.`; }
  else if(d4 === want){ status = 'turning'; head = `D1 is still ${W(dD)}, but H4 has turned ${want} — an early turn toward the ${bias} bias, lower quality until D1 follows.`; }
  else { status = 'conflict'; head = `Price disagrees with the ${bias} bias: D1 and H4 structure point ${W(dD) === 'unclear' ? 'the other way or sideways' : W(dD)}${turnLvl != null ? `. It would start to agree on a 4h close ${upB ? 'above' : 'below'} ${f(turnLvl)}` : ''}.`; }
  const detail = [];
  const zSide = want ? (upB ? dem[0] : sup[0]) : null;
  if(inZone) detail.push(`Price is inside a ${inZone.tf} ${inZone.kind} zone ${f(inZone.lo)}–${f(inZone.hi)} (${inZone.status}).`);
  if(zSide) detail.push(`Nearest ${zSide.tf} ${zSide.kind} on the bias side: ${f(zSide.lo)}–${f(zSide.hi)} (${zSide.status}), ${((upB ? price - zSide.hi : zSide.lo - price) / A).toFixed(1)} ATR away.`);
  if(sweep) detail.push(`Latest sweep: ${sweep.side === 'BSL' ? 'buy-side' : 'sell-side'} liquidity (${sweep.name} ${f(sweep.level)}) taken and rejected on ${sweep.tf}.`);
  if(bsl || ssl) detail.push(`Resting liquidity: ${bsl ? `above ${f(bsl.p)} (${bsl.name})` : 'none close above'}; ${ssl ? `below ${f(ssl.p)} (${ssl.name})` : 'none close below'}.`);
  detail.push(`Location: ${pos >= 0.5 ? 'premium' : 'discount'} of the 3-month range (${Math.round(pos * 100)}%).`);
  if(status === 'aligned' && invLvl != null) detail.push(`The price read turns against the bias on a daily close ${upB ? 'below' : 'above'} ${f(invLvl)} (last D1 swing).`);
  const ev = s => s.last ? { type:s.last.type, dir:s.last.dir, level:f(s.last.level), at:new Date(s.last.t * 1000).toISOString() } : null;
  return { pair:p, price:f(price), price_time:new Date(last.t * 1000).toISOString(), bias, conviction:fb?.conviction || null, gap:fb ? fb.base_score - fb.quote_score : null,
    status, headline:head, detail,
    d1:{ structure:dD, trend:sD.trend, last:ev(sD), atr:f(A) }, h4:{ structure:d4, trend:s4.trend, last:ev(s4), atr:f(A4) }, h1:{ structure:s1.dir, trend:s1.trend, last:ev(s1) },
    zones:{ demand:dem.slice(0, 2).map(z => ({ tf:z.tf, lo:f(z.lo), hi:f(z.hi), status:z.status })), supply:sup.slice(0, 2).map(z => ({ tf:z.tf, lo:f(z.lo), hi:f(z.hi), status:z.status })), inside:inZone ? { tf:inZone.tf, kind:inZone.kind, lo:f(inZone.lo), hi:f(inZone.hi), status:inZone.status } : null },
    liquidity:{ above:bsl ? { level:f(bsl.p), name:bsl.name, atr:+((bsl.p - price) / A).toFixed(2) } : null, below:ssl ? { level:f(ssl.p), name:ssl.name, atr:+((price - ssl.p) / A).toFixed(2) } : null,
      last_sweep:sweep ? { side:sweep.side, name:sweep.name, level:f(sweep.level), tf:sweep.tf, at:new Date(sweep.t * 1000).toISOString() } : null },
    location:{ pct:Math.round(pos * 100), label:pos >= 0.5 ? 'premium' : 'discount', hi:f(hi66), lo:f(lo66) },
    watch_level:status === 'aligned' ? f(invLvl) : f(turnLvl) };
}

const fbAll = loadBias(), now = Math.floor(Date.now() / 1000), out = {}, errors = {};
for(const p of PAIRS){
  try{ out[p] = analyse(p, await hourly(sym(p)), fbAll.pairs[p], now); }catch(e){ errors[p] = String(e.message || e); }
  await sleep(300);
}
const n = Object.keys(out).length;
const res = { format:'bias-engine-ta', version:1, generated_at:new Date().toISOString(), fundamentals:fbAll.week,
  source:'Yahoo Finance hourly bars (FX PAIR=X, gold GC=F futures), regrouped into New-York-close daily and 4-hour bars. Levels can differ by a few pips from your broker.',
  note:'Technical context compared with the fundamental bias. Price never changes a fundamental score. Not a trade signal.',
  counts:Object.fromEntries(['aligned','pullback','turning','conflict','two-sided'].map(s => [s, Object.values(out).filter(x => x.status === s).length])),
  pairs:out, errors };
if(n < 20){ console.error('too many pairs failed', errors); process.exit(1); }
mkdirSync('exports', { recursive:true });
const txt = JSON.stringify(res, null, 1);
writeFileSync('exports/ta-latest.json', txt);
writeFileSync(`exports/ta-${res.generated_at.slice(0, 10)}.json`, txt);
console.log(`ta: ${n} pairs, fundamentals ${fbAll.week}`, res.counts, Object.keys(errors).length ? errors : '');
