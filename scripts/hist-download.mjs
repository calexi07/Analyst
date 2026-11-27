// Downloads public Dukascopy candles (bid) for one instrument, year by year, into hist/<PAIR>_<tf>.csv.gz
// Usage: node scripts/hist-download.mjs eurusd 2012 m15,h1
import { getHistoricalRates } from 'dukascopy-node';
import { mkdirSync, createWriteStream } from 'node:fs';
import { createGzip } from 'node:zlib';
const [inst, fromYear, tfs] = [process.argv[2], +process.argv[3], (process.argv[4] || 'h1').split(',')];
mkdirSync('hist', { recursive: true });
const now = new Date();
for (const tf of tfs) {
  const gz = createGzip(); gz.pipe(createWriteStream(`hist/${inst.toUpperCase()}_${tf}.csv.gz`));
  gz.write('time_utc,open,high,low,close\n');
  let total = 0;
  for (let y = fromYear; y <= now.getUTCFullYear(); y++) {
    const from = new Date(Date.UTC(y, 0, 1)), to = y === now.getUTCFullYear() ? now : new Date(Date.UTC(y + 1, 0, 1));
    let rows = [];
    for (let attempt = 1; attempt <= 4; attempt++) {
      try {
        rows = await getHistoricalRates({ instrument: inst, dates: { from, to }, timeframe: tf, priceType: 'bid', format: 'array',
          batchSize: 15, pauseBetweenBatchesMs: 300, retryCount: 5, pauseBetweenRetriesMs: 1500, ignoreFlats: true, useCache: false });
        break;
      } catch (e) { console.error(inst, tf, y, 'attempt', attempt, e.message); await new Promise(r => setTimeout(r, 5000 * attempt)); }
    }
    for (const r of rows) gz.write(`${new Date(r[0]).toISOString()},${r[1]},${r[2]},${r[3]},${r[4]}\n`);
    total += rows.length; console.log(inst, tf, y, rows.length);
  }
  await new Promise(r => gz.end(r));
  console.log('DONE', inst, tf, total);
}
