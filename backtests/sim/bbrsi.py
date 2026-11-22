# Bollinger + RSI Double Strategy (ChartArt v1.1): RSI(6) crosses 50 on the same bar the close crosses back inside a
# Bollinger band (SMA 200, 2 sd); long at the lower band, short at the upper. Plus variants with BB 20 and pullback reads.
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smc import B, cost_of, pip_of
_c = {}
def calc(b, bl, rl):
    key = (id(b), len(b), bl, rl)
    if key in _c: return _c[key]
    c = np.array([x['c'] for x in b]); N = len(c)
    bas = np.full(N, np.nan); sd = np.full(N, np.nan)
    for i in range(bl - 1, N): w = c[i - bl + 1:i + 1]; bas[i] = w.mean(); sd[i] = w.std(ddof=0)
    d = np.diff(c, prepend=c[0]); up = np.maximum(d, 0); dn = np.maximum(-d, 0); au = np.zeros(N); ad = np.zeros(N)
    au[rl] = up[1:rl + 1].mean(); ad[rl] = dn[1:rl + 1].mean()
    for i in range(rl + 1, N): au[i] = (au[i - 1] * (rl - 1) + up[i]) / rl; ad[i] = (ad[i - 1] * (rl - 1) + dn[i]) / rl
    rsi = np.where(ad > 0, 100 - 100 / (1 + au / np.where(ad > 0, ad, 1)), 100); rsi[:rl + 1] = np.nan
    _c[key] = (bas, sd, rsi); return _c[key]
DEF = dict(entry='orig', bl=200, rl=6, k=2.0, sl='atr', slk=1.5, tpR=3, mx=None, trail=0, t2=0, win=3)
def run(p, b, P, start, end):
    P = {**DEF, **P}; cost = cost_of(p) * pip_of(p); bas, sd, rsi = calc(b, P['bl'], P['rl'])
    up_, lo_ = bas + P['k'] * sd, bas - P['k'] * sd
    res = []; pos = None; lastIn = {1: -99, -1: -99}
    for i in range(2, len(b)):
        x = b[i]; A = x['atr']; c, c1 = x['c'], b[i - 1]['c']
        if np.isnan(rsi[i - 1]) or np.isnan(bas[i - 1]): continue
        crL = c > lo_[i] and c1 <= lo_[i - 1]; crS = c < up_[i] and c1 >= up_[i - 1]
        if crL: lastIn[1] = i
        if crS: lastIn[-1] = i
        rU = rsi[i] > 50 >= rsi[i - 1]; rD = rsi[i] < 50 <= rsi[i - 1]
        if pos:
            d = pos['d']; px = None
            if (x['l'] <= pos['sl']) if d > 0 else (x['h'] >= pos['sl']): px = min(x['o'], pos['sl']) if d > 0 else max(x['o'], pos['sl']); why = 'SL'
            elif pos['tp'] and ((x['h'] >= pos['tp']) if d > 0 else (x['l'] <= pos['tp'])): px = max(x['o'], pos['tp']) if d > 0 else min(x['o'], pos['tp']); why = 'TP'
            elif P['mx'] == 'band' and d * (c - (up_[i] if d > 0 else lo_[i])) >= 0: px = c; why = 'band'
            elif P['mx'] == 'basis' and d * (c - bas[i]) >= 0 and pos['below']: px = c; why = 'basis'
            elif P['mx'] == 'rsi' and (rD if d > 0 else rU): px = c; why = 'rsi'
            if px is not None:
                res.append(dict(p=p, d=d, t=pos['t'], tx=x['tc'], wk=pos['wk'], R=d * (px - pos['e']) / pos['r'] - cost / pos['r'], why=why)); pos = None
            else:
                pos['best'] = max(pos['best'], d * ((x['h'] if d > 0 else x['l']) - pos['e']))
                if P['trail']:
                    kk = P['t2'] if P['t2'] and pos['best'] >= 2 * pos['r'] else P['trail']
                    ns = c - d * kk * A; pos['sl'] = max(pos['sl'], ns) if d > 0 else min(pos['sl'], ns)
        if pos or A is None or not (start <= x['t'] < end): continue
        E = P['entry']; d = 0
        if E == 'orig': d = 1 if (rU and crL) else -1 if (rD and crS) else 0
        elif E == 'window': d = 1 if (rU and i - lastIn[1] <= P['win']) else -1 if (rD and i - lastIn[-1] <= P['win']) else 0
        elif E == 'rsi_pb':   # RSI crosses back through 50 while price is on the far side of the basis (pullback)
            d = 1 if (rU and c < bas[i]) else -1 if (rD and c > bas[i]) else 0
        elif E == 'rsi':      # RSI(6) cross of 50 alone
            d = 1 if rU else -1 if rD else 0
        if not d: continue
        bi_ = B.get((p, x['wk']), ('-',))[0]; bd = 1 if bi_ == 'U' else -1 if bi_ == 'D' else 0
        if P['bias'] and bd != d: continue
        if P['hours'] and not (P['hours'][0] <= x['hr'] < P['hours'][1]): continue
        r = P['slk'] * A if P['sl'] == 'atr' else max(abs(c - min(y['l'] if d > 0 else y['h'] for y in b[i - 5:i + 1])) + 0.1 * A, 0.3 * A)
        if P['sl'] == 'swing' and d < 0: r = max(abs(max(y['h'] for y in b[i - 5:i + 1]) - c) + 0.1 * A, 0.3 * A)
        pos = dict(d=d, e=c, r=r, sl=c - d * r, tp=c + d * P['tpR'] * r if P['tpR'] else None, t=x['t'], wk=x['wk'], best=0, below=True)
    return res
if __name__ == '__main__':
    from harness import go_bias
    print('baseline: random entry in bias direction, SL1.5 TP3 = +0.19R/tr')
    E = [('orig', dict(), 'original: BB200 + RSI6 cross on same bar'), ('orig', dict(bl=20), 'same, BB 20'),
         ('window', dict(bl=20), 'BB20 re-entry, RSI cross within 3 bars'), ('rsi_pb', dict(bl=20), 'RSI6 back through 50, price beyond BB20 basis'),
         ('rsi_pb', dict(bl=50), 'same, basis 50'), ('rsi', dict(), 'RSI6 cross of 50 alone')]
    X = [('SL1.5 TP3', dict()), ('SL1 TP3', dict(slk=1.0)), ('SL swing TP3', dict(sl='swing')), ('SL1.5 TP2', dict(tpR=2)),
         ('your exit', dict(slk=1.0, tpR=4, trail=0.75, t2=0.5)), ('exit at opposite band', dict(tpR=0, mx='band')), ('exit RSI back', dict(tpR=0, mx='rsi'))]
    for e, ep, en in E:
        print('==', en)
        for xn, xp in X: print(f"  {xn:<22} {go_bias(run, {'entry': e, **ep, **xp})}", flush=True)
