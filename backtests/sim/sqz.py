# Squeeze Momentum [LazyBear] (as published: the BB width uses multKC 1.5, KC 20/1.5 with true range; momentum = linreg(close -
# avg(avg(highest20, lowest20), sma20), 20, 0)). Tested as entry, as exit, and as filter/exit for BE Swing and CISD.
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smc import B, cost_of, pip_of
_c = {}
def squeeze(b, n=20, bbk=1.5, kck=1.5):
    key = (id(b), n, bbk, kck)
    if key in _c: return _c[key]
    N = len(b); h = np.array([x['h'] for x in b]); l = np.array([x['l'] for x in b]); c = np.array([x['c'] for x in b])
    tr = np.empty(N); tr[0] = h[0] - l[0]; tr[1:] = np.maximum(h[1:], c[:-1]) - np.minimum(l[1:], c[:-1])
    val = np.full(N, np.nan); on = np.zeros(N, bool); off = np.zeros(N, bool)
    xs = np.arange(n); xm = xs.mean(); den = ((xs - xm) ** 2).sum()
    for i in range(n - 1, N):
        w = c[i - n + 1:i + 1]; m = w.mean(); sd = w.std(); rm = tr[i - n + 1:i + 1].mean()
        ub, lb, uk, lk = m + bbk * sd, m - bbk * sd, m + kck * rm, m - kck * rm
        on[i] = lb > lk and ub < uk; off[i] = lb < lk and ub > uk
        if i >= 2 * n - 2:
            y = np.array([c[j] - ((h[j - n + 1:j + 1].max() + l[j - n + 1:j + 1].min()) / 2 + c[j - n + 1:j + 1].mean()) / 2 for j in range(i - n + 1, i + 1)])
            sl = ((xs - xm) * (y - y.mean())).sum() / den; val[i] = y.mean() + sl * (n - 1 - xm)
    _c[key] = (val, on, off)
    return val, on, off

DEF = dict(entry='fire', sl='atr', slk=1.0, tpR=3, trail=0, t2=0, tract=0, mx=None, bias=True, hours=None, recent=6)
def run(p, b, P, start, end):
    P = {**DEF, **P}; cost = cost_of(p) * pip_of(p); val, on, off = squeeze(b)
    res = []; pos = None
    for i in range(2, len(b)):
        x = b[i]; A = x['atr']; v, v1, v2 = val[i], val[i - 1], val[i - 2]
        if pos:
            d = pos['d']; px = None
            if (x['l'] <= pos['sl']) if d > 0 else (x['h'] >= pos['sl']): px = min(x['o'], pos['sl']) if d > 0 else max(x['o'], pos['sl']); why = 'SL'
            elif pos['tp'] and ((x['h'] >= pos['tp']) if d > 0 else (x['l'] <= pos['tp'])): px = max(x['o'], pos['tp']) if d > 0 else min(x['o'], pos['tp']); why = 'TP'
            elif P['mx'] == 'fade' and d * (v - v1) < 0 and d * v > 0: px = x['c']; why = 'fade'          # histogram turns dark
            elif P['mx'] == 'fade2' and d * (v - v1) < 0 and d * (v1 - v2) < 0: px = x['c']; why = 'fade2'
            elif P['mx'] == 'zero' and d * v < 0: px = x['c']; why = 'zero'
            elif P['mx'] == 'fade_after1R' and pos['best'] >= pos['r'] and d * (v - v1) < 0: px = x['c']; why = 'fade1R'
            if px is not None:
                res.append(dict(p=p, d=d, t=pos['t'], tx=x['tc'], wk=pos['wk'], R=d * (px - pos['e']) / pos['r'] - cost / pos['r'], why=why)); pos = None
            else:
                pos['best'] = max(pos['best'], d * ((x['h'] if d > 0 else x['l']) - pos['e']))
                if P['trail'] and pos['best'] >= P['tract'] * pos['r']:
                    k = P['t2'] if P['t2'] and pos['best'] >= 2 * pos['r'] else P['trail']
                    ns = x['c'] - d * k * A; pos['sl'] = max(pos['sl'], ns) if d > 0 else min(pos['sl'], ns)
        if pos or A is None or np.isnan(v) or np.isnan(v2) or not (start <= x['t'] < end): continue
        bi_ = B.get((p, x['wk']), ('-',))[0]; bd = 1 if bi_ == 'U' else -1 if bi_ == 'D' else 0
        d = None
        if P['entry'] == 'fire':        # squeeze released (was on, now not), momentum gives the side
            if on[i - 1] and not on[i] and v != 0: d = 1 if v > 0 else -1
        elif P['entry'] == 'fire_mom':  # released within `recent` bars and momentum rising in that side
            if on[max(0, i - P['recent']):i].any() and not on[i]:
                d = 1 if v > 0 and v > v1 else -1 if v < 0 and v < v1 else None
        elif P['entry'] == 'zero':      # momentum crosses zero
            if v > 0 >= v1: d = 1
            elif v < 0 <= v1: d = -1
        elif P['entry'] == 'turn':      # pullback ends: momentum against the bias but turning back (red -> maroon)
            if v < 0 and v > v1 and v1 <= v2: d = 1
            elif v > 0 and v < v1 and v1 >= v2: d = -1
        elif P['entry'] == 'turn_pos':  # in-trend dip: momentum positive, dark green -> lime
            if v > 0 and v > v1 and v1 <= v2: d = 1
            elif v < 0 and v < v1 and v1 >= v2: d = -1
        if d is None: continue
        if P['bias'] and bd != d: continue
        if P['hours'] and not (P['hours'][0] <= x['hr'] < P['hours'][1]): continue
        e = x['c']; r = P['slk'] * A if P['sl'] == 'atr' else abs(e - (min(y['l'] for y in b[i - 5:i + 1]) if d > 0 else max(y['h'] for y in b[i - 5:i + 1]))) + 0.1 * A
        if not (0.3 * A <= r <= 3 * A): continue
        pos = dict(d=d, e=e, r=r, sl=e - d * r, tp=e + d * P['tpR'] * r if P['tpR'] else None, t=x['t'], wk=x['wk'], best=0)
    return res
if __name__ == '__main__':
    from harness import go
    E = [('fire', 'squeeze fires'), ('fire_mom', 'fired <=6 bars + momentum rising'), ('zero', 'momentum zero cross'),
         ('turn', 'pullback end (red->maroon)'), ('turn_pos', 'in-trend dip end (dkgreen->lime)')]
    X = [('SL1 TP3', dict()), ('SL1 TP2', dict(tpR=2)), ('SL1.5 TP3', dict(slk=1.5)), ('SL swing5 TP3', dict(sl='swing')),
         ('your exit', dict(tpR=4, trail=0.75, t2=0.5)), ('exit: fade', dict(tpR=0, mx='fade')), ('exit: 2 fading bars', dict(tpR=0, mx='fade2')),
         ('exit: zero cross', dict(tpR=0, mx='zero')), ('TP4 + fade after 1R', dict(tpR=4, mx='fade_after1R'))]
    for e, en in E:
        print(f"== entry: {en}")
        for xn, P in X: print(f"  {xn:<22} {go(run, {'entry': e, **P})}", flush=True)
