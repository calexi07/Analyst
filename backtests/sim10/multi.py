# User's indicators as entry signals: Engulfing OB / Outside-bar OB, WaveTrend cross, Squeeze Momentum, US30 PSAR+EMA/SMMA pullback,
# BigBeluga-style BOS (pivot structure). Same trade engine for all: entry at the signal close, SL = k·ATR, TP in R, max hold N bars.
import sys, math
sys.path.insert(0, '/home/claude/analyst/backtests/sim'); sys.path.insert(0, '/home/claude/analyst/backtests/sim10')
def ema(a, n):
    o = []; k = 2 / (n + 1); v = None
    for x in a: v = x if v is None else v + k * (x - v); o.append(v)
    return o
def sma(a, n):
    o = []; s = 0
    for i, x in enumerate(a):
        s += x
        if i >= n: s -= a[i - n]
        o.append(s / n if i >= n - 1 else None)
    return o
def rma(a, n):
    o = []; v = None
    for i, x in enumerate(a):
        if i < n - 1: o.append(None); continue
        v = sum(a[i - n + 1:i + 1]) / n if v is None else (v * (n - 1) + x) / n; o.append(v)
    return o
def stdev(a, n):
    o = []
    for i in range(len(a)):
        if i < n - 1: o.append(None); continue
        w = a[i - n + 1:i + 1]; m = sum(w) / n; o.append(math.sqrt(sum((x - m) ** 2 for x in w) / n))
    return o
def linreg_last(w):
    n = len(w); xm = (n - 1) / 2; ym = sum(w) / n
    b = sum((i - xm) * (y - ym) for i, y in enumerate(w)) / sum((i - xm) ** 2 for i in range(n)); return ym + b * (n - 1 - xm)
def psar(b, st=0.02, inc=0.02, mx=0.2):
    o = [None] * len(b); up = True; af = st; ep = b[0]['h']; sar = b[0]['l']
    for i in range(1, len(b)):
        sar = sar + af * (ep - sar)
        if up:
            sar = min(sar, b[i-1]['l'], b[i-2]['l'] if i > 1 else b[i-1]['l'])
            if b[i]['l'] < sar: up = False; sar = ep; ep = b[i]['l']; af = st
            elif b[i]['h'] > ep: ep = b[i]['h']; af = min(mx, af + inc)
        else:
            sar = max(sar, b[i-1]['h'], b[i-2]['h'] if i > 1 else b[i-1]['h'])
            if b[i]['h'] > sar: up = True; sar = ep; ep = b[i]['h']; af = st
            elif b[i]['l'] < ep: ep = b[i]['l']; af = min(mx, af + inc)
        o[i] = sar
    return o
def signals(b, kind):
    """list of (i, dir)"""
    O = [x['o'] for x in b]; Hh = [x['h'] for x in b]; L = [x['l'] for x in b]; C = [x['c'] for x in b]; n = len(b); out = []
    if kind in ('eob', 'obob'):
        for i in range(1, n):
            bull = C[i] > O[i] and C[i-1] < O[i-1]; bear = C[i] < O[i] and C[i-1] > O[i-1]
            if kind == 'eob':
                if bull and C[i] > O[i-1]: out.append((i, 1))
                if bear and C[i] < O[i-1]: out.append((i, -1))
            else:
                if bull and C[i] > Hh[i-1] and L[i] < L[i-1]: out.append((i, 1))
                if bear and C[i] < L[i-1] and Hh[i] > Hh[i-1]: out.append((i, -1))
    elif kind.startswith('wt'):
        ap = [(Hh[i] + L[i] + C[i]) / 3 for i in range(n)]; esa = ema(ap, 10); d = ema([abs(ap[i] - esa[i]) for i in range(n)], 10)
        ci = [(ap[i] - esa[i]) / (0.015 * d[i]) if d[i] else 0 for i in range(n)]; w1 = ema(ci, 21); w2 = sma(w1, 4)
        for i in range(30, n):
            if w2[i] is None or w2[i-1] is None: continue
            up = w1[i] > w2[i] and w1[i-1] <= w2[i-1]; dn = w1[i] < w2[i] and w1[i-1] >= w2[i-1]
            if kind == 'wt_os':
                up = up and w1[i] < -53; dn = dn and w1[i] > 53
            if up: out.append((i, 1))
            if dn: out.append((i, -1))
    elif kind.startswith('sqz'):
        bas = sma(C, 20); dev = stdev(C, 20); tr = [Hh[0] - L[0]] + [max(Hh[i], C[i-1]) - min(L[i], C[i-1]) for i in range(1, n)]; rm = sma(tr, 20)
        val = [None] * n; on = [False] * n
        for i in range(39, n):
            hh = max(Hh[i-19:i+1]); ll = min(L[i-19:i+1]); src = [C[j] - ((max(Hh[j-19:j+1]) + min(L[j-19:j+1])) / 2 + bas[j]) / 2 for j in range(i - 19, i + 1)]
            val[i] = linreg_last(src)
            ub = bas[i] + 1.5 * dev[i]; lb = bas[i] - 1.5 * dev[i]; uk = bas[i] + 1.5 * rm[i]; lk = bas[i] - 1.5 * rm[i]   # the user's script uses multKC for BB too
            on[i] = lb > lk and ub < uk
        for i in range(41, n):
            if val[i] is None or val[i-1] is None or val[i-2] is None: continue
            if kind == 'sqz_flip':      # maroon → lime / green → red (the user's "răsturnare" alerts)
                if val[i] > 0 and val[i] > val[i-1] and val[i-1] < 0 and val[i-1] >= val[i-2]: out.append((i, 1))
                if val[i] < 0 and val[i] < val[i-1] and val[i-1] > 0 and val[i-1] <= val[i-2]: out.append((i, -1))
            elif kind == 'sqz_zero':
                if val[i] > 0 and val[i-1] <= 0: out.append((i, 1))
                if val[i] < 0 and val[i-1] >= 0: out.append((i, -1))
            elif kind == 'sqz_fire':    # squeeze releases: momentum side
                if on[i-1] and not on[i]: out.append((i, 1 if val[i] > 0 else -1))
    elif kind.startswith('us30'):
        ps = psar(b); e50 = ema(C, 50); s50 = rma(C, 50); s100 = rma(C, 100); armed = 0
        for i in range(101, n):
            if ps[i] is None or ps[i-1] is None or s100[i] is None: continue
            d = 1 if ps[i] < C[i] else -1; d1 = 1 if ps[i-1] < C[i-1] else -1; mid = (Hh[i] + L[i]) / 2
            if d == 1 and d1 == -1 and C[i] > ps[i-1] and mid > e50[i] and s100[i] < s50[i] < e50[i]: armed = 1
            if d == -1 and d1 == 1 and C[i] < ps[i-1] and mid < e50[i] and s100[i] > s50[i] > e50[i]: armed = -1
            if kind == 'us30_setup' and armed and d != d1: out.append((i, armed)); armed = 0; continue
            if armed == 1 and C[i] <= s50[i]: out.append((i, 1)); armed = 0
            elif armed == -1 and C[i] >= s50[i]: out.append((i, -1)); armed = 0
    elif kind == 'bos':
        ph = pl = None; used_h = used_l = None; k = 5
        for i in range(2 * k, n):
            j = i - k
            if Hh[j] == max(Hh[j-k:j+k+1]): ph = Hh[j]
            if L[j] == min(L[j-k:j+k+1]): pl = L[j]
            if ph is not None and C[i] > ph and C[i-1] <= ph and used_h != ph: out.append((i, 1)); used_h = ph
            if pl is not None and C[i] < pl and C[i-1] >= pl and used_l != pl: out.append((i, -1)); used_l = pl
    return out
def trades(b, kind, dirf, cost, k=1.5, tp=3.0, maxh=48, hrs=None):
    out = []; busy = -1
    for i, d in signals(b, kind):
        if i <= busy or not b[i].get('atr'): continue
        if hrs and not (hrs[0] <= b[i]['bh'] < hrs[1]): continue
        D_ = dirf(b[i])
        if D_ is None or d not in D_: continue
        e = b[i]['c']; r = k * b[i]['atr']; s = e - d * r; t = e + d * tp * r
        res = None
        for j in range(i + 1, min(len(b), i + 1 + maxh)):
            x = b[j]
            if (x['l'] <= s) if d > 0 else (x['h'] >= s): res = -1; break
            if (x['h'] >= t) if d > 0 else (x['l'] <= t): res = tp; break
        else:
            j = min(len(b) - 1, i + maxh); res = d * (b[j]['c'] - e) / r
        out.append((b[i]['t'], res - cost / r)); busy = j
    return out
