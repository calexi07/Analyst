# Second page of TradingView built-in strategies, same test as tv_builtins.py.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tv_builtins.py')).read().split("DATA = {p")[0]
exec(src)
def signals2(b):
    c = [x['c'] for x in b]; h = [x['h'] for x in b]; l = [x['l'] for x in b]; n = len(b); S = collections.defaultdict(lambda: [0] * n)
    tr = [h[i] - l[i] if i == 0 else max(h[i], c[i - 1]) - min(l[i], c[i - 1]) for i in range(n)]
    # ADX 14
    pdm = [0] + [max(h[i] - h[i - 1], 0) if h[i] - h[i - 1] > l[i - 1] - l[i] else 0 for i in range(1, n)]
    ndm = [0] + [max(l[i - 1] - l[i], 0) if l[i - 1] - l[i] > h[i] - h[i - 1] else 0 for i in range(1, n)]
    a14 = ema(tr, 27); pdi = [100 * a / t if t else 0 for a, t in zip(ema(pdm, 27), a14)]; ndi = [100 * a / t if t else 0 for a, t in zip(ema(ndm, 27), a14)]
    dx = [100 * abs(p - q) / (p + q) if p + q else 0 for p, q in zip(pdi, ndi)]; adx = ema(dx, 27)
    e20, e50 = ema(c, 20), ema(c, 50)
    k_raw = [None if i < 13 else 100 * (c[i] - min(l[i - 13:i + 1])) / ((max(h[i - 13:i + 1]) - min(l[i - 13:i + 1])) or 1) for i in range(n)]
    k = [None if i < 15 or None in k_raw[i - 2:i + 1] else sum(k_raw[i - 2:i + 1]) / 3 for i in range(n)]
    dd = [None if i < 17 or None in k[i - 2:i + 1] else sum(k[i - 2:i + 1]) / 3 for i in range(n)]
    ph = [None] * n; pl = [None] * n; lph = lpl = None
    for i in range(6, n):
        q = i - 2
        if h[q] > max(h[q - 4:q]) and h[q] >= max(h[q + 1:i + 1]): lph = h[q]; ph[i] = h[q]
        if l[q] < min(l[q - 4:q]) and l[q] <= min(l[q + 1:i + 1]): lpl = l[q]; pl[i] = l[q]
        if i < 60: continue
        S['Pivot extension (fade pivots)'][i] = -1 if ph[i] else 1 if pl[i] else 0
        S['Pivot reversal (break last pivot)'][i] = 1 if lph and c[i] > lph >= c[i - 1] else -1 if lpl and c[i] < lpl <= c[i - 1] else 0
        S['Price channel 20'][i] = 1 if c[i] > max(h[i - 20:i]) else -1 if c[i] < min(l[i - 20:i]) else 0
        S['ADX breakout (ADX<18, 20-bar box)'][i] = (1 if c[i] > max(h[i - 20:i]) else -1 if c[i] < min(l[i - 20:i]) else 0) if adx[i - 1] < 18 else 0
        if k[i] is not None and dd[i] is not None and k[i - 1] is not None and dd[i - 1] is not None:
            S['Stochastic slow 14/3/3'][i] = 1 if k[i - 1] <= dd[i - 1] and k[i] > dd[i] and k[i] < 20 else -1 if k[i - 1] >= dd[i - 1] and k[i] < dd[i] and k[i] > 80 else 0
        S['Two MA crossover 20/50 EMA'][i] = 1 if e20[i - 1] <= e50[i - 1] and e20[i] > e50[i] else -1 if e20[i - 1] >= e50[i - 1] and e20[i] < e50[i] else 0
        av = sum(tr[i - 5:i]) / 5 * 0.75
        S['Volatility expansion close'][i] = 1 if c[i] > c[i - 1] + av else -1 if c[i] < c[i - 1] - av else 0
    return S
DATA = {p: load(p) for p in PAIRS}; SIG = {p: signals2(DATA[p]) for p in PAIRS}
LONG = ['GBPUSD', 'AUDUSD', 'USDJPY', 'USDCHF', 'USDCAD', 'XAUUSD']; YRS = [(U(2024, 3, 1), U(2025, 1, 1)), (U(2025, 1, 1), U(2026, 1, 1)), (U(2026, 1, 1), U(2026, 11, 22))]
for nm in SIG['EURUSD']:
    out = []
    for ub in (True, False):
        hs = [sum([run(p, DATA[p], SIG[p][nm], a, c, ub) for p in PAIRS], []) for a, c in H]
        R = [r for _, r in hs[0] + hs[1]]
        out.append(f"{'bias' if ub else 'both'} {len(R):3}tr {sum(r for _, r in hs[0]):+5.1f}/{sum(r for _, r in hs[1]):+5.1f}={sum(R):+5.1f}R")
    ys = [sum(r for p in LONG for _, r in run(p, DATA[p], SIG[p][nm], a, c, False)) for a, c in YRS]
    print(f"{nm:<36} {out[0]} | {out[1]} | 3y {sum(ys):+6.1f}R [{', '.join('%+.0f' % y for y in ys)}]")
