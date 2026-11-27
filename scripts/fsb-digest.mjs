// Compact per-pair digest of data/fsb/<PAIR>.csv for the scheduled multi-timeframe analysis.
// Everything here is computed from the CSV (no judgement): the current state of the 9 structures, the supply/demand zones
// of each timeframe with their state after creation (fresh / tested n× / invalidated), ATR(14) on 1H, structure changes
// in the last 48 candles. Output: data/fsb/digest.json
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { PAIRS, parseCsv } from './fsb-export.mjs';

const TFS = ['D', '4H', '1H'], STR = ['swing', 'internal', 'fractal'];
const num = s => (s === '' || s == null ? null : +s);
export function digest(text) {
  const [hd, ...rs] = parseCsv(text), ix = c => hd.indexOf(c), col = (r, c) => num(r[ix(c)]);
  const bars = rs.map(r => ({ time: r[ix('time')], o: col(r, 'open'), h: col(r, 'high'), l: col(r, 'low'), c: col(r, 'close'), r }));
  const n = bars.length, last = bars[n - 1];
  // ATR(14) on 1H (simple average of true range)
  let atr = null; if (n > 15) { let s = 0; for (let i = n - 14; i < n; i++) { const b = bars[i], pc = bars[i - 1].c; s += Math.max(b.h - b.l, Math.abs(b.h - pc), Math.abs(b.l - pc)); } atr = s / 14; }
  const out = { last_time: last.time, close: last.c, atr14_1h: atr && +atr.toPrecision(5), rows: n, structures: {}, zones: {}, changes_48h: [] };
  for (const tf of TFS) for (const st of STR) {
    const k = `${tf} ${st}`, r = last.r;
    out.structures[k] = { trend: num(r[ix(`${k} trend`)]), choch: num(r[ix(`${k} CHoCH`)]), bos: num(r[ix(`${k} BOS`)]), pos: num(r[ix(`${k} pos %`)]) };
    for (let i = Math.max(1, n - 48); i < n; i++) { const a = num(bars[i - 1].r[ix(`${k} trend`)]), b = num(bars[i].r[ix(`${k} trend`)]);
      if (a !== b) out.changes_48h.push({ time: bars[i].time, structure: k, from: a, to: b, choch_after: num(bars[i].r[ix(`${k} CHoCH`)]) }); }
  }
  for (const tf of TFS) {
    const zk = r => ['zone dir (1 demand, -1 supply)', 'zone full high', 'zone full low', 'zone refined high', 'zone refined low'].map(c => r[ix(`${tf} ${c}`)]).join('|');
    const segs = []; let start = 0;
    for (let i = 1; i <= n; i++) if (i === n || zk(bars[i].r) !== zk(bars[start].r)) { segs.push([start, i - 1]); start = i; }
    out.zones[tf] = segs.slice(-4).reverse().map(([a]) => {
      const r = bars[a].r, dir = num(r[ix(`${tf} zone dir (1 demand, -1 supply)`)]);
      if (!dir) return null;
      const z = { dir: dir > 0 ? 'demand' : 'supply', since: bars[a].time, since_is_csv_start: a === 0,
        full: [num(r[ix(`${tf} zone full low`)]), num(r[ix(`${tf} zone full high`)])], refined: [num(r[ix(`${tf} zone refined low`)]), num(r[ix(`${tf} zone refined high`)])] };
      const [rl, rh] = z.refined, distal = dir > 0 ? z.full[0] : z.full[1];
      let tests = 0, inside = false, inval = null;
      for (let i = a + 1; i < n; i++) { const b = bars[i];
        const touch = dir > 0 ? b.l <= rh : b.h >= rl;
        if (touch && !inside) tests++; inside = touch;
        if (dir > 0 ? b.c < distal : b.c > distal) { inval = b.time; break; } }
      z.state = inval ? `invalidated ${inval}` : tests ? `tested ${tests}x` : 'fresh';
      z.current = a === segs.at(-1)[0];
      return z; }).filter(Boolean);
  }
  return out;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const all = { generated_at: new Date().toISOString(), pairs: {} };
  for (const p of PAIRS) { const f = `data/fsb/${p}.csv`; all.pairs[p] = existsSync(f) ? digest(readFileSync(f, 'utf8')) : null; }
  writeFileSync('data/fsb/digest.json', JSON.stringify(all, null, 1) + '\n');
  console.log(Object.entries(all.pairs).map(([p, d]) => `${p}:${d ? d.rows : '-'}`).join(' '));
}
