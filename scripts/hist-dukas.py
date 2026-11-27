"""Download public Dukascopy minute candles (BID) day by day from datafeed.dukascopy.com and build 15m and 1H CSVs.
Usage: python scripts/hist-dukas.py EURUSD 2012
Output: hist/<PAIR>_m15.csv.gz, hist/<PAIR>_h1.csv.gz (time_utc = candle open, UTC), hist/<PAIR>_report.txt"""
import sys, lzma, struct, gzip, os, datetime as dt, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
pair, y0 = sys.argv[1].upper(), int(sys.argv[2])
point = 1e3 if 'JPY' in pair else 1e5
os.makedirs('hist', exist_ok=True)
def fetch(day):
    url = f'https://datafeed.dukascopy.com/datafeed/{pair}/{day.year}/{day.month-1:02d}/{day.day:02d}/BID_candles_min_1.bi5'
    for a in range(5):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as r: raw = r.read()
            if not raw: return day, []
            data = lzma.decompress(raw)
            base = int(dt.datetime(day.year, day.month, day.day, tzinfo=dt.timezone.utc).timestamp())
            out = []
            for k in range(0, len(data) - 23, 24):
                t, o, c, l, h, v = struct.unpack('>5if', data[k:k+24])
                if v > 0: out.append((base + t, o / point, h / point, l / point, c / point))
            return day, out
        except urllib.error.HTTPError as e:
            if e.code == 404: return day, []
            time.sleep(2 * (a + 1))
        except Exception:
            time.sleep(2 * (a + 1))
    return day, None
days = []; d = dt.date(y0, 1, 1); end = dt.date.today()
while d <= end:
    if d.weekday() != 5: days.append(d)   # no Saturday trading
    d += dt.timedelta(days=1)
rows, failed = [], []
with ThreadPoolExecutor(8) as ex:
    for day, out in ex.map(fetch, days):
        if out is None: failed.append(str(day))
        else: rows.extend(out)
df = pd.DataFrame(rows, columns=['t', 'open', 'high', 'low', 'close']).sort_values('t').drop_duplicates('t')
df['time'] = pd.to_datetime(df.t, unit='s', utc=True); df = df.set_index('time')
for tf, rule in [('m15', '15min'), ('h1', '1h')]:
    g = df.resample(rule).agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'}).dropna()
    g.index.name = 'time_utc'
    with gzip.open(f'hist/{pair}_{tf}.csv.gz', 'wt') as f: g.to_csv(f)
with open(f'hist/{pair}_report.txt', 'w') as f:
    f.write(f'{pair} days requested {len(days)} minute rows {len(df)} first {df.index.min()} last {df.index.max()} failed days {len(failed)}\n')
    f.write('\n'.join(failed[:200]))
print(open(f'hist/{pair}_report.txt').read()[:400])
