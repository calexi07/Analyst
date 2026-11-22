# Lower-timeframe EURUSD loader (5/15/30 min exports) in the same bar format as smc.prep, plus a 1H structure context.
import os, csv, datetime as D
from zoneinfo import ZoneInfo
from swing2 import NY
HERE = os.path.dirname(os.path.abspath(__file__)); BUC = ZoneInfo('Europe/Bucharest')
def load(pair, tf):
    out = []
    for r in csv.DictReader(open(os.path.join(HERE, f'../ohlc/FOREXCOM_{pair}_{tf}.csv'))):
        t = D.datetime.fromisoformat(r['time']).astimezone(D.timezone.utc)
        b = dict(t=t, tc=t + D.timedelta(minutes=int(tf)), o=float(r['open']), h=float(r['high']), l=float(r['low']), c=float(r['close']))
        ny = (t + D.timedelta(hours=7)).astimezone(NY); b['day'] = ny.date(); b['dow'] = ny.weekday(); b['wk'] = ny.date().isocalendar()[:2]
        b['hr'] = t.astimezone(BUC).hour; out.append(b)
    out.sort(key=lambda b: b['t']); A = None
    for i, b in enumerate(out):
        tr = b['h'] - b['l'] if i == 0 else max(b['h'], out[i - 1]['c']) - min(b['l'], out[i - 1]['c'])
        A = tr if A is None else (A * 13 + tr) / 14; b['atr'] = A if i >= 13 else None
    return out
def struct_ctx(h1, ltf, L=3):
    """1H market structure: +1 after a close above the last confirmed pivot high, -1 after a close below the last pivot low;
    mapped onto lower-timeframe bars using completed 1H candles only."""
    st = []; ph = pl = None; s = 0
    for i, x in enumerate(h1):
        k = i - L
        if k >= L:
            if h1[k]['h'] == max(y['h'] for y in h1[k - L:i + 1]): ph = h1[k]['h']
            if h1[k]['l'] == min(y['l'] for y in h1[k - L:i + 1]): pl = h1[k]['l']
        if ph is not None and x['c'] > ph: s = 1
        elif pl is not None and x['c'] < pl: s = -1
        st.append((x['tc'], s))
    out = []; j = -1; cur = 0
    for b in ltf:
        while j + 1 < len(st) and st[j + 1][0] <= b['t']: j += 1; cur = st[j][1]
        out.append(cur)
    return out
