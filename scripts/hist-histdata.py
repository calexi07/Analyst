"""Download free HistData.com 1-minute bars (generic ASCII, times in EST without DST = UTC-5) and build 15m and 1H CSVs in UTC.
Usage: python scripts/hist-histdata.py EURUSD 2012
Output: hist/<PAIR>_m15.csv.gz, hist/<PAIR>_h1.csv.gz (time_utc = candle open), hist/<PAIR>_report.txt"""
import sys, re, io, os, gzip, zipfile, time, datetime as dt, urllib.request, urllib.parse, http.cookiejar
import pandas as pd
pair, y0 = sys.argv[1].upper(), int(sys.argv[2]); low = pair.lower()
os.makedirs('hist', exist_ok=True)
cj = http.cookiejar.CookieJar(); op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36'}
def get_zip(path):
    page = f'https://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/{low}/{path}'
    for a in range(5):
        try:
            html = op.open(urllib.request.Request(page, headers=UA), timeout=60).read().decode('utf-8', 'ignore')
            form = re.search(r'<form[^>]*id="file_down"[^>]*>(.*?)</form>', html, re.S)
            if not form: return None, 'no form'
            fields = dict(re.findall(r'<input[^>]*name="([^"]+)"[^>]*value="([^"]*)"', form.group(1)))
            data = urllib.parse.urlencode(fields).encode()
            req = urllib.request.Request('https://www.histdata.com/get.php', data=data, headers={**UA, 'Referer': page, 'Content-Type': 'application/x-www-form-urlencoded'})
            raw = op.open(req, timeout=120).read()
            if raw[:2] != b'PK': return None, f'not a zip ({len(raw)} bytes)'
            return raw, 'ok'
        except Exception as e:
            err = str(e)[:80]; time.sleep(5 * (a + 1))
    return None, err
today = dt.date.today(); jobs = [str(y) for y in range(y0, today.year)] + [f'{today.year}/{m}' for m in range(1, today.month + 1)]
frames, log = [], []
for j in jobs:
    raw, msg = get_zip(j); log.append(f'{j} {msg}'); print(pair, j, msg, flush=True)
    if raw is None: continue
    z = zipfile.ZipFile(io.BytesIO(raw)); name = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    df = pd.read_csv(z.open(name), sep=';', header=None, names=['dt', 'open', 'high', 'low', 'close', 'vol'])
    frames.append(df); time.sleep(1)
df = pd.concat(frames, ignore_index=True)
t = pd.to_datetime(df.dt, format='%Y%m%d %H%M%S') + pd.Timedelta(hours=5)   # EST (fixed UTC-5) -> UTC
df = df.assign(time=t.dt.tz_localize('UTC')).drop_duplicates('time').sort_values('time').set_index('time')
for tf, rule in [('m15', '15min'), ('h1', '1h')]:
    g = df.resample(rule).agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'}).dropna(); g.index.name = 'time_utc'
    with gzip.open(f'hist/{pair}_{tf}.csv.gz', 'wt') as f: g.to_csv(f)
with open(f'hist/{pair}_report.txt', 'w') as f:
    f.write(f'{pair} HistData minute rows {len(df)} first {df.index.min()} last {df.index.max()}\n' + '\n'.join(log) + '\n')
print(open(f'hist/{pair}_report.txt').read())
