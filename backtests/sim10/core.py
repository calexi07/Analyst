# 10-year intraday research on 15m bars (ejtraderLabs/historical-data, 2012-2022, broker time ≈ Bucharest).
# One engine for all ideas: per day, signal → entry (market at bar close or stop), SL, TP in R, exit at a clock time.
# Conservative: when SL and TP fall in the same 15m bar, SL first. Costs per round trip in price units.
import csv, datetime as D, collections, math, os
DATA = '/tmp/fx/ej'
SC = {'EURUSD': 1e-5, 'GBPUSD': 1e-5, 'XAUUSD': 1e-2, 'AUDUSD': 1e-5, 'EURCHF': 1e-5, 'EURGBP': 1e-5, 'USDCAD': 1e-5, 'USDCHF': 1e-5, 'AUDJPY': 1e-3, 'EURJPY': 1e-3, 'GBPJPY': 1e-3, 'USDJPY': 1e-3}
COST = {'EURUSD': 0.00010, 'GBPUSD': 0.00015, 'XAUUSD': 0.35, 'AUDUSD': 0.00012, 'EURCHF': 0.00018, 'EURGBP': 0.00015, 'USDCAD': 0.00018, 'USDCHF': 0.00016, 'AUDJPY': 0.020, 'EURJPY': 0.018, 'GBPJPY': 0.028, 'USDJPY': 0.012}
_cache = {}
def load(p):
    if p in _cache: return _cache[p]
    s = SC[p]; bars = []
    for r in list(csv.reader(open(f'{DATA}/{p}m15.csv')))[1:]:
        t = D.datetime.fromisoformat(r[0]); o, h, l, c = (float(x) * s for x in r[1:5])
        bars.append(dict(t=t, d=t.date(), m=t.hour * 60 + t.minute, o=o, h=h, l=l, c=c))
    # ATR(14) on 15m, EMA20/50
    A = e20 = e50 = None
    for i, b in enumerate(bars):
        tr = b['h'] - b['l'] if i == 0 else max(b['h'], bars[i-1]['c']) - min(b['l'], bars[i-1]['c'])
        A = tr if A is None else (A * 13 + tr) / 14; b['atr'] = A
        e20 = b['c'] if e20 is None else e20 + 2/21 * (b['c'] - e20); e50 = b['c'] if e50 is None else e50 + 2/51 * (b['c'] - e50)
        b['e20'], b['e50'] = e20, e50
    days = collections.OrderedDict()
    for i, b in enumerate(bars): days.setdefault(b['d'], []).append(i)
    ks = [k for k in days if k.weekday() < 5]
    info = {}
    closes = []
    for j, k in enumerate(ks):
        ix = days[k]; hi = max(bars[i]['h'] for i in ix); lo = min(bars[i]['l'] for i in ix)
        prev = info.get(ks[j-1]) if j else None
        info[k] = dict(ix=ix, h=hi, l=lo, o=bars[ix[0]]['o'], c=bars[ix[-1]]['c'],
                       sma=sum(closes[-20:]) / 20 if len(closes) >= 20 else None,
                       adr=(sum(info[q]['h'] - info[q]['l'] for q in ks[max(0, j-14):j]) / min(14, j)) if j else None,
                       pdh=prev['h'] if prev else None, pdl=prev['l'] if prev else None, pdc=prev['c'] if prev else None, pdo=prev['o'] if prev else None)
        closes.append(info[k]['c'])
    _cache[p] = (bars, ks, info); return _cache[p]

def rng(bars, ix, m0, m1):
    v = [bars[i] for i in ix if m0 <= bars[i]['m'] < m1]
    return (max(x['h'] for x in v), min(x['l'] for x in v)) if v else (None, None)

def manage(bars, ix, k, d, e, sl, tp, xm, cost):
    """from bar index position k (entry filled during/at it) manage until exit; returns R"""
    r = abs(e - sl)
    for q in ix[ix.index(k):]:
        b = bars[q]
        if q != k or True:
            if (b['l'] <= sl) if d > 0 else (b['h'] >= sl): px = min(b['o'], sl) if d > 0 else max(b['o'], sl); return d * (px - e) / r - cost / r, b['t']
            if tp is not None and ((b['h'] >= tp) if d > 0 else (b['l'] <= tp)): px = max(b['o'], tp) if d > 0 else min(b['o'], tp); return d * (px - e) / r - cost / r, b['t']
        if b['m'] >= xm: return d * (b['c'] - e) / r - cost / r, b['t']
    b = bars[ix[-1]]; return d * (b['c'] - e) / r - cost / r, b['t']

def summary(tr, label=''):
    if not tr: return f"{label:44} no trades"
    R = [x[1] for x in tr]; n = len(R); yrs = collections.defaultdict(float)
    for t, r in tr: yrs[t.year] += r
    eq = pk = dd = 0
    for r in R: eq += r; pk = max(pk, eq); dd = min(dd, eq - pk)
    mid = D.date(2017, 7, 1); h1 = sum(r for t, r in tr if t.date() < mid); h2 = sum(R) - h1
    pos = sum(v > 0 for v in yrs.values())
    return f"{label:44} {n:5d}tr {sum(R):+7.1f}R {sum(R)/n:+.3f}/tr win {sum(r>0 for r in R)/n:.0%} DD {dd:6.1f} halves {h1:+6.1f}/{h2:+6.1f} yrs+ {pos}/{len(yrs)} ({sum(R)/max(1,len(yrs)):+.1f}R/yr)"
