# "Trend Volume Profile and Rolling POC [BigBeluga]": SMA25 +/- ATR50 x1 bands; trend turns bull when close crosses above the
# upper band, bear when close is below the lower band after a bull phase (as written). Rolling POC = highest bin of the profile
# since the trend started (bins 0.2 ATR). FX data has no volume -> every bar weighs 1 (time-at-price profile).
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smc import B, cost_of, pip_of
_c = {}
def tvp(b, ma=25, al=50, am=1.0, bin_=0.2):
    key = (id(b), len(b), ma, al, am)
    if key in _c: return _c[key]
    N = len(b); h = np.array([x['h'] for x in b]); l = np.array([x['l'] for x in b]); c = np.array([x['c'] for x in b])
    tr = np.empty(N); tr[0] = h[0] - l[0]; tr[1:] = np.maximum(h[1:], c[:-1]) - np.minimum(l[1:], c[:-1])
    atr = np.full(N, np.nan); atr[al - 1] = tr[:al].mean()
    for i in range(al, N): atr[i] = (atr[i - 1] * (al - 1) + tr[i]) / al
    cs = np.cumsum(c); bas = np.full(N, np.nan); bas[ma - 1:] = (cs[ma - 1:] - np.concatenate([[0], cs[:-ma]])) / ma
    up = bas + am * atr; lo = bas - am * atr
    pend = 0; act = np.zeros(N, int); start = np.zeros(N, int); poc = np.full(N, np.nan); st = 0
    for i in range(1, N):
        if np.isnan(up[i]) or np.isnan(up[i - 1]): continue
        if c[i] > up[i] and c[i - 1] <= up[i - 1]: newp = 1
        elif c[i] < lo[i] and pend > 0: newp = -1
        else: newp = pend
        if newp != pend: st = i; pend = newp
        act[i] = pend; start[i] = st
        if pend != 0:
            wl, wh = l[st:i + 1], h[st:i + 1]; rl, rh = wl.min(), wh.max()
            span = max(rh - rl, atr[i] * 0.1); bh = max(atr[i] * bin_, 1e-9); n = int(min(max(round(span / bh), 2), 100)); bh = span / n
            edges = rl + np.arange(n) * bh
            ov = np.minimum(wh[:, None], edges[None, :] + bh) - np.maximum(wl[:, None], edges[None, :])
            rng = (wh - wl)[:, None]
            vol = np.where(ov > 0, ov / np.where(rng > 0, rng, 1), 0).sum(0)
            flat = (wh - wl) <= 0
            if flat.any():
                for j in np.where(flat)[0]: vol[min(max(int((wl[j] - rl) // bh), 0), n - 1)] += 1
            poc[i] = rl + (np.argmax(vol) + 0.5) * bh
    _c[key] = dict(bas=bas, up=up, lo=lo, act=act, start=start, poc=poc, atr=atr)
    return _c[key]

DEF = dict(entry='flip', sl='atr', slk=1.0, tpR=3, trail=0, t2=0, tract=0, mx=None, bias=True, hours=None, life=12)
def run(p, b, P, start, end):
    P = {**DEF, **P}; cost = cost_of(p) * pip_of(p); T = tvp(b); act, poc, bas, up, lo = T['act'], T['poc'], T['bas'], T['up'], T['lo']
    res = []; pos = None; pend = None
    def fill(i, d, e, r):
        return dict(i=i, d=d, e=e, r=r, sl=e - d * r, tp=e + d * P['tpR'] * r if P['tpR'] else None, t=b[i]['t'], wk=b[i]['wk'], best=0)
    for i in range(2, len(b)):
        x = b[i]; A = x['atr']
        if pos:
            d = pos['d']; px = None
            if (x['l'] <= pos['sl']) if d > 0 else (x['h'] >= pos['sl']): px = min(x['o'], pos['sl']) if d > 0 else max(x['o'], pos['sl']); why = 'SL'
            elif pos['tp'] and ((x['h'] >= pos['tp']) if d > 0 else (x['l'] <= pos['tp'])): px = max(x['o'], pos['tp']) if d > 0 else min(x['o'], pos['tp']); why = 'TP'
            elif P['mx'] == 'flip' and act[i] == -d: px = x['c']; why = 'flip'
            elif P['mx'] == 'poc' and d * (x['c'] - poc[i]) < 0 and pos['best'] >= pos['r']: px = x['c']; why = 'pocx'
            if px is not None:
                res.append(dict(p=p, d=d, t=pos['t'], tx=x['tc'], wk=pos['wk'], R=d * (px - pos['e']) / pos['r'] - cost / pos['r'], why=why)); pos = None
            else:
                pos['best'] = max(pos['best'], d * ((x['h'] if d > 0 else x['l']) - pos['e']))
                if P['trail'] == 'band':            # trend boundary line as trailing stop
                    ln = lo[i] if d > 0 else up[i]; pos['sl'] = max(pos['sl'], ln) if d > 0 else min(pos['sl'], ln)
                elif P['trail'] == 'poc' and pos['best'] >= pos['r']:
                    ln = poc[i] - d * 0.2 * A; pos['sl'] = max(pos['sl'], ln) if d > 0 else min(pos['sl'], ln)
                elif P['trail'] and not isinstance(P['trail'], str) and pos['best'] >= P['tract'] * pos['r']:
                    k = P['t2'] if P['t2'] and pos['best'] >= 2 * pos['r'] else P['trail']
                    ns = x['c'] - d * k * A; pos['sl'] = max(pos['sl'], ns) if d > 0 else min(pos['sl'], ns)
        if pend and not pos:
            d = pend['d']
            if i - pend['i'] > P['life'] or act[i - 1] != d: pend = None      # known at the previous close (no look-ahead)
            elif (x['l'] <= pend['e']) if d > 0 else (x['h'] >= pend['e']):
                e = min(x['o'], pend['e']) if d > 0 else max(x['o'], pend['e']); pos = fill(i, d, e, pend['r']); pend = None
                if (x['l'] <= pos['sl']) if d > 0 else (x['h'] >= pos['sl']):
                    res.append(dict(p=p, d=d, t=x['t'], tx=x['tc'], wk=x['wk'], R=-1 - cost / pos['r'], why='SL fill')); pos = None
        if pos or pend or A is None or np.isnan(poc[i]) or not (start <= x['t'] < end): continue
        d = act[i]
        if d == 0: continue
        bi_ = B.get((p, x['wk']), ('-',))[0]; bd = 1 if bi_ == 'U' else -1 if bi_ == 'D' else 0
        if P['bias'] and bd != d: continue
        if P['hours'] and not (P['hours'][0] <= x['hr'] < P['hours'][1]): continue
        E = P['entry']; r = P['slk'] * A
        if E == 'flip':
            if act[i - 1] == d: continue
            e = x['c']
            if P['sl'] == 'band': r = abs(e - (lo[i] if d > 0 else up[i])) + 0.1 * A
            if 0.3 * A <= r <= 3 * A: pos = fill(i, d, e, r)
        else:
            # pullback limits while the trend is active and price is extended away from the level
            lvl = poc[i] if E == 'poc' else bas[i] if E == 'basis' else (lo[i] if d > 0 else up[i])
            if d * (x['c'] - lvl) < 0.5 * A: continue          # need price away from the level first
            if i - T['start'][i] < 3: continue
            if P['sl'] == 'band': r = abs(lvl - (lo[i] if d > 0 else up[i])) + 0.3 * A
            if 0.3 * A <= r <= 3 * A: pend = dict(i=i, d=d, e=lvl, r=r)
    return res
if __name__ == '__main__':
    from harness import go
    E = [('flip', 'trend flip (BULL/BEAR)'), ('poc', 'pullback to rolling POC (limit)'), ('basis', 'pullback to SMA25 basis'), ('band', 'pullback to trend boundary band')]
    X = [('SL1 TP3', dict()), ('SL1 TP2', dict(tpR=2)), ('SL1.5 TP3', dict(slk=1.5)), ('SL beyond band TP3', dict(sl='band')),
         ('your exit', dict(tpR=4, trail=0.75, t2=0.5)), ('exit: trend flip', dict(tpR=0, mx='flip')), ('trail: boundary band', dict(tpR=0, trail='band')),
         ('trail: POC after +1R', dict(tpR=0, trail='poc')), ('TP4 + trail band', dict(tpR=4, trail='band'))]
    for e, en in E:
        print(f"== entry: {en}")
        for xn, P in X: print(f"  {xn:<22} {go(run, {'entry': e, **P})}", flush=True)
