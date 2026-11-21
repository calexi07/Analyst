# TradingView built-in strategies (approximate logic) on 4H candles, taken only in the engine's bias direction.
# Entry at the signal candle's close; exit on the opposite signal, at Friday's close, or at a 2x daily-ATR stop.
# Result in R where 1R = one daily ATR (position sized on the daily ATR). 14 pairs, W40-W47.
import sys, os, datetime as D, statistics as St, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from swing2 import *
U = lambda *a: D.datetime(*a, tzinfo=D.timezone.utc)
H = [(U(2026, 9, 27, 21), U(2026, 10, 25, 21)), (U(2026, 10, 25, 21), U(2026, 11, 22))]
PAIRS = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'USDCAD', 'AUDUSD', 'NZDUSD', 'XAUUSD', 'EURGBP', 'EURJPY', 'EURCHF', 'EURAUD', 'EURNZD', 'EURCAD']
B = bias_table()
def ema(v, n):
    o, a = [], None
    for x in v: a = x if a is None else a + 2 / (n + 1) * (x - a); o.append(a)
    return o
def sma(v, n): return [None if i < n - 1 else sum(v[i - n + 1:i + 1]) / n for i in range(len(v))]
def signals(b):
    c = [x['c'] for x in b]; h = [x['h'] for x in b]; l = [x['l'] for x in b]; n = len(b); S = collections.defaultdict(lambda: [0] * n)
    m20 = sma(c, 20); sd = [None if i < 19 else St.pstdev(c[i - 19:i + 1]) for i in range(n)]
    tr = [h[i] - l[i] if i == 0 else max(h[i], c[i - 1]) - min(l[i], c[i - 1]) for i in range(n)]; atr = ema(tr, 10)
    e12, e26 = ema(c, 12), ema(c, 26); macd = [a - b_ for a, b_ in zip(e12, e26)]; sig = ema(macd, 9); hist = [a - b_ for a, b_ in zip(macd, sig)]
    s9, s18 = sma(c, 9), sma(c, 18)
    # RSI 14
    up = [0] + [max(c[i] - c[i - 1], 0) for i in range(1, n)]; dn = [0] + [max(c[i - 1] - c[i], 0) for i in range(1, n)]
    ru, rd = ema(up, 27), ema(dn, 27); rsi = [100 - 100 / (1 + (u / d if d else 1e9)) for u, d in zip(ru, rd)]
    # supertrend 10/3 and parabolic SAR
    st_dir = [1] * n; fu = fl = None
    for i in range(n):
        hl2 = (h[i] + l[i]) / 2; ub = hl2 + 3 * atr[i]; lb = hl2 - 3 * atr[i]
        fu = ub if fu is None or ub < fu or c[i - 1] > fu else fu; fl = lb if fl is None or lb > fl or c[i - 1] < fl else fl
        st_dir[i] = st_dir[i - 1] if i else 1
        if c[i] > fu: st_dir[i] = 1
        elif c[i] < fl: st_dir[i] = -1
    psar_dir = [1] * n; sar = l[0]; ep = h[0]; af = 0.02; d_ = 1
    for i in range(1, n):
        sar = sar + af * (ep - sar)
        if d_ > 0 and l[i] < sar: d_ = -1; sar = ep; ep = l[i]; af = 0.02
        elif d_ < 0 and h[i] > sar: d_ = 1; sar = ep; ep = h[i]; af = 0.02
        elif (d_ > 0 and h[i] > ep) or (d_ < 0 and l[i] < ep): ep = h[i] if d_ > 0 else l[i]; af = min(af + 0.02, 0.2)
        psar_dir[i] = d_
    for i in range(27, n):
        if m20[i] and m20[i - 1]:
            lo, lo1 = m20[i] - 2 * sd[i], m20[i - 1] - 2 * sd[i - 1]; hi, hi1 = m20[i] + 2 * sd[i], m20[i - 1] + 2 * sd[i - 1]
            S['Bollinger Bands'][i] = 1 if c[i - 1] < lo1 and c[i] > lo else -1 if c[i - 1] > hi1 and c[i] < hi else 0
            ku, kl = m20[i] + atr[i] * 1.5, m20[i] - atr[i] * 1.5
            S['Keltner channels'][i] = 1 if c[i] > ku else -1 if c[i] < kl else 0
        S['Channel breakout'][i] = 1 if h[i] > max(h[i - 5:i]) else -1 if l[i] < min(l[i - 5:i]) else 0
        S['MACD'][i] = 1 if hist[i - 1] <= 0 < hist[i] else -1 if hist[i - 1] >= 0 > hist[i] else 0
        mom, mom1 = c[i] - c[i - 12], (c[i] - c[i - 12]) - (c[i - 1] - c[i - 13])
        S['Momentum'][i] = 1 if mom > 0 and mom1 > 0 else -1 if mom < 0 and mom1 < 0 else 0
        if s18[i] and s18[i - 1]: S['MA crossover 9/18'][i] = 1 if s9[i - 1] <= s18[i - 1] and s9[i] > s18[i] else -1 if s9[i - 1] >= s18[i - 1] and s9[i] < s18[i] else 0
        S['Parabolic SAR'][i] = psar_dir[i] if psar_dir[i] != psar_dir[i - 1] else 0
        S['SuperTrend 10/3'][i] = st_dir[i] if st_dir[i] != st_dir[i - 1] else 0
        S['RSI 30/70'][i] = 1 if rsi[i - 1] < 30 <= rsi[i] else -1 if rsi[i - 1] > 70 >= rsi[i] else 0
        ib = h[i - 1] < h[i - 2] and l[i - 1] > l[i - 2]
        S['Inside bar'][i] = (1 if c[i] > h[i - 1] else -1 if c[i] < l[i - 1] else 0) if ib else 0
        S['Outside bar'][i] = (1 if c[i] > o_ else -1) if (h[i] > h[i - 1] and l[i] < l[i - 1] and (o_ := b[i]['o']) != c[i]) else 0
        S['Consecutive up/down (3)'][i] = 1 if c[i] > c[i - 1] > c[i - 2] > c[i - 3] else -1 if c[i] < c[i - 1] < c[i - 2] < c[i - 3] else 0
    return S
def run(p, b, sig, start, end, usebias=True):
    cost = cost_of(p) * pip_of(p); res = []; pos = None
    for i, x in enumerate(b):
        if pos:
            d, e, sl, A = pos
            if (x['l'] <= sl) if d > 0 else (x['h'] >= sl): res.append((x['wk'], (sl - e) * d / A - cost / A)); pos = None; continue
            last = x['dow'] == 4 and (i + 1 == len(b) or b[i + 1]['day'] != x['day'])
            if sig[i] == -d or last: res.append((x['wk'], (x['c'] - e) * d / A - cost / A)); pos = None
            continue
        if not (start <= x['t'] < end) or x['atr'] is None or x['dow'] > 3: continue
        bi = B.get((p, x['wk']), ('-',))[0]; bd = 1 if bi == 'U' else -1 if bi == 'D' else 0
        if sig[i] and (not usebias or sig[i] == bd): pos = (sig[i], x['c'], x['c'] - sig[i] * 2 * x['atr'], x['atr'])
    return res
DATA = {p: load(p) for p in PAIRS}; SIG = {p: signals(DATA[p]) for p in PAIRS}
names = list(SIG['EURUSD'].keys()); rows = []
for nm in names:
    for ub in (True, False):
        hs = [sum([run(p, DATA[p], SIG[p][nm], a, c, ub) for p in PAIRS], []) for a, c in H]
        t = hs[0] + hs[1]; R = [r for _, r in t]
        rows.append((nm, ub, len(t), sum(r for _, r in hs[0]), sum(r for _, r in hs[1]), sum(R), sum(r > 0 for r in R) / max(1, len(R))))
for nm, ub, n, a, b_, s, w in sorted(rows, key=lambda z: (not z[1], -z[5])):
    print(f"{'bias only ' if ub else 'both sides'} {nm:<26} {n:4}tr win {w:.0%} {a:+6.1f}/{b_:+6.1f} = {s:+6.1f}R")
