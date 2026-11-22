# CM_MacD_Ult_MTF (ChrisMoody): MACD 12/26 (EMA), signal = SMA 9 of MACD, histogram = MACD - signal, 4-colour histogram.
# Tested as entry, exit, and as filter/exit for BE Swing and CISD.
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smc import B, cost_of, pip_of
_c = {}
def macd(b, f=12, s=26, g=9):
    key = (id(b), len(b), f, s, g)
    if key in _c: return _c[key]
    c = np.array([x['c'] for x in b]); N = len(c)
    def ema(n):
        o = np.empty(N); k = 2 / (n + 1); o[0] = c[0]
        for i in range(1, N): o[i] = o[i - 1] + k * (c[i] - o[i - 1])
        return o
    m = ema(f) - ema(s); sg = np.full(N, np.nan)
    cs = np.cumsum(m); sg[g - 1:] = (cs[g - 1:] - np.concatenate([[0], cs[:-g]])) / g
    m[:s] = np.nan; sg[:s + g] = np.nan
    _c[key] = (m, sg, m - sg)
    return _c[key]

DEF = dict(entry='cross', sl='atr', slk=1.0, tpR=3, trail=0, t2=0, tract=0, mx=None, bias=True, hours=None)
def run(p, b, P, start, end):
    P = {**DEF, **P}; cost = cost_of(p) * pip_of(p); m, sg, hs = macd(b)
    res = []; pos = None
    for i in range(3, len(b)):
        x = b[i]; A = x['atr']
        if np.isnan(hs[i - 2]): continue
        h0, h1, h2 = hs[i], hs[i - 1], hs[i - 2]
        if pos:
            d = pos['d']; px = None
            if (x['l'] <= pos['sl']) if d > 0 else (x['h'] >= pos['sl']): px = min(x['o'], pos['sl']) if d > 0 else max(x['o'], pos['sl']); why = 'SL'
            elif pos['tp'] and ((x['h'] >= pos['tp']) if d > 0 else (x['l'] <= pos['tp'])): px = max(x['o'], pos['tp']) if d > 0 else min(x['o'], pos['tp']); why = 'TP'
            elif P['mx'] == 'cross' and d * h0 < 0: px = x['c']; why = 'cross'
            elif P['mx'] == 'zero' and d * m[i] < 0: px = x['c']; why = 'zero'
            elif P['mx'] == 'fade2' and d * (h0 - h1) < 0 and d * (h1 - h2) < 0: px = x['c']; why = 'fade2'
            elif P['mx'] == 'cross_1R' and pos['best'] >= pos['r'] and d * h0 < 0: px = x['c']; why = 'cross1R'
            if px is not None:
                res.append(dict(p=p, d=d, t=pos['t'], tx=x['tc'], wk=pos['wk'], R=d * (px - pos['e']) / pos['r'] - cost / pos['r'], why=why)); pos = None
            else:
                pos['best'] = max(pos['best'], d * ((x['h'] if d > 0 else x['l']) - pos['e']))
                if P['trail'] and pos['best'] >= P['tract'] * pos['r']:
                    k = P['t2'] if P['t2'] and pos['best'] >= 2 * pos['r'] else P['trail']
                    ns = x['c'] - d * k * A; pos['sl'] = max(pos['sl'], ns) if d > 0 else min(pos['sl'], ns)
        if pos or A is None or not (start <= x['t'] < end): continue
        d = None; E = P['entry']
        up, dn = h0 > 0 >= h1, h0 < 0 <= h1          # MACD crosses its signal line
        if E == 'cross': d = 1 if up else -1 if dn else None
        elif E == 'cross_pb':                        # cross on the far side of zero (pullback in trend)
            d = 1 if up and m[i] < 0 else -1 if dn and m[i] > 0 else None
        elif E == 'cross_tr':                        # cross on the trend side of zero
            d = 1 if up and m[i] > 0 else -1 if dn and m[i] < 0 else None
        elif E == 'zero': d = 1 if m[i] > 0 >= m[i - 1] else -1 if m[i] < 0 <= m[i - 1] else None
        elif E == 'hturn':                           # histogram below zero turns up (red -> maroon)
            d = 1 if h0 <= 0 and h0 > h1 and h1 <= h2 else -1 if h0 > 0 and h0 < h1 and h1 >= h2 else None
        elif E == 'hturn_pos':                       # histogram above zero turns up again (blue -> aqua)
            d = 1 if h0 > 0 and h0 > h1 and h1 <= h2 else -1 if h0 <= 0 and h0 < h1 and h1 >= h2 else None
        if d is None: continue
        bi_ = B.get((p, x['wk']), ('-',))[0]; bd = 1 if bi_ == 'U' else -1 if bi_ == 'D' else 0
        if P['bias'] and bd != d: continue
        if P['hours'] and not (P['hours'][0] <= x['hr'] < P['hours'][1]): continue
        e = x['c']; r = P['slk'] * A if P['sl'] == 'atr' else abs(e - (min(y['l'] for y in b[i - 5:i + 1]) if d > 0 else max(y['h'] for y in b[i - 5:i + 1]))) + 0.1 * A
        if not (0.3 * A <= r <= 3 * A): continue
        pos = dict(d=d, e=e, r=r, sl=e - d * r, tp=e + d * P['tpR'] * r if P['tpR'] else None, t=x['t'], wk=x['wk'], best=0)
    return res
if __name__ == '__main__':
    from harness import go
    E = [('cross', 'MACD x signal (any)'), ('cross_pb', 'cross on far side of zero (pullback)'), ('cross_tr', 'cross on trend side of zero'),
         ('zero', 'MACD zero cross'), ('hturn', 'hist red -> maroon'), ('hturn_pos', 'hist blue -> aqua')]
    X = [('SL1 TP3', dict()), ('SL1 TP2', dict(tpR=2)), ('SL1.5 TP3', dict(slk=1.5)), ('SL swing5 TP3', dict(sl='swing')),
         ('your exit', dict(tpR=4, trail=0.75, t2=0.5)), ('exit: cross against', dict(tpR=0, mx='cross')), ('exit: MACD zero', dict(tpR=0, mx='zero')),
         ('exit: hist 2 fading', dict(tpR=0, mx='fade2')), ('TP4 + cross after 1R', dict(tpR=4, mx='cross_1R'))]
    for e, en in E:
        print(f"== entry: {en}")
        for xn, P in X: print(f"  {xn:<22} {go(run, {'entry': e, **P})}", flush=True)
