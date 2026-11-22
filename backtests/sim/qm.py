# Quasimodo (QM / over-and-under), bias direction only, 1H.
# Bullish QM: pivot low L1, pivot high H1, lower low L2 < L1, then price breaks above H1 (close) -> limit at L1 (the left
# shoulder), stop below L2 (+0.1 ATR), TP xR; order valid `life` bars, cancelled if price reaches +1R first. Bearish mirrors it.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smc import B, cost_of, pip_of
DEF = dict(L=3, tpR=3, life=48, minR=0.3, maxR=3.0, entry='shoulder', bias=True, hours=None)
def run(p, b, P, start, end):
    P = {**DEF, **P}; L = P['L']; cost = cost_of(p) * pip_of(p); res = []; pos = None; pend = None
    pivs = []   # (index, +1 high / -1 low, price)
    used = set()
    for i in range(2 * L, len(b)):
        x = b[i]; A = x['atr']; k = i - L
        if b[k]['h'] == max(y['h'] for y in b[k - L:i + 1]) and b[k]['h'] > max(y['h'] for y in b[k - L:k]): pivs.append((k, 1, b[k]['h']))
        if b[k]['l'] == min(y['l'] for y in b[k - L:i + 1]) and b[k]['l'] < min(y['l'] for y in b[k - L:k]): pivs.append((k, -1, b[k]['l']))
        pivs[:] = pivs[-30:]
        if pos:
            d = pos['d']; px = None
            if (x['l'] <= pos['sl']) if d > 0 else (x['h'] >= pos['sl']): px = min(x['o'], pos['sl']) if d > 0 else max(x['o'], pos['sl'])
            elif (x['h'] >= pos['tp']) if d > 0 else (x['l'] <= pos['tp']): px = max(x['o'], pos['tp']) if d > 0 else min(x['o'], pos['tp'])
            if px is not None: res.append(dict(p=p, d=d, t=pos['t'], tx=x['tc'], wk=pos['wk'], R=d * (px - pos['e']) / pos['r'] - cost / pos['r'])); pos = None
        if pend and not pos:
            d = pend['d']
            if i - pend['i'] > P['life'] or ((x['h'] >= pend['e'] + pend['r']) if d > 0 else (x['l'] <= pend['e'] - pend['r'])) and not ((x['l'] <= pend['e']) if d > 0 else (x['h'] >= pend['e'])): pend = None
            elif (x['l'] <= pend['e']) if d > 0 else (x['h'] >= pend['e']):
                e = min(x['o'], pend['e']) if d > 0 else max(x['o'], pend['e']); r = abs(e - pend['sl'])
                if (x['l'] <= pend['sl']) if d > 0 else (x['h'] >= pend['sl']): res.append(dict(p=p, d=d, t=x['t'], tx=x['tc'], wk=x['wk'], R=-1 - cost / r))
                else: pos = dict(d=d, e=e, r=r, sl=pend['sl'], tp=e + d * P['tpR'] * r, t=x['t'], wk=x['wk'])
                pend = None
        if pos or pend or A is None or not (start <= x['t'] < end): continue
        bi_ = B.get((p, x['wk']), ('-',))[0]; bd = 1 if bi_ == 'U' else -1 if bi_ == 'D' else 0
        if P['bias'] and bd == 0: continue
        for d in ((bd,) if P['bias'] else (1, -1)):
            # last three alternating pivots before now: shoulder S (same side as d's stop), head Hd, neck N
            seq = [q for q in pivs if q[0] < i]
            # for a long: ... low L1, high H1, low L2 (L2 < L1), break of H1
            lows = [q for q in seq if q[1] == -d]; highs = [q for q in seq if q[1] == d]
            if len(lows) < 2 or not highs: continue
            L2 = lows[-1]; H1 = next((q for q in reversed(highs) if q[0] < L2[0]), None)
            if not H1: continue
            L1 = next((q for q in reversed(lows[:-1]) if q[0] < H1[0]), None)
            if not L1 or (L1[0], L2[0], H1[0]) in used: continue
            if not ((L2[2] < L1[2]) if d > 0 else (L2[2] > L1[2])): continue
            if not ((x['c'] > H1[2] and b[i - 1]['c'] <= H1[2]) if d > 0 else (x['c'] < H1[2] and b[i - 1]['c'] >= H1[2])): continue
            used.add((L1[0], L2[0], H1[0]))
            e = L1[2] if P['entry'] == 'shoulder' else (L1[2] + L2[2]) / 2
            sl = L2[2] - d * 0.1 * A; r = abs(e - sl)
            if P['minR'] * A <= r <= P['maxR'] * A and (x['c'] - e) * d > 0: pend = dict(d=d, e=e, sl=sl, r=r, i=i)
            break
    return res
if __name__ == '__main__':
    from harness import go_bias
    for n, P in [('QM L3, shoulder, TP 2R', dict(tpR=2)), ('QM L3, shoulder, TP 3R', {}), ('QM L3, shoulder, TP 4R', dict(tpR=4)),
                 ('QM L3, mid shoulder-head, TP 3R', dict(entry='mid')), ('QM L5, shoulder, TP 3R', dict(L=5)), ('QM L2, shoulder, TP 3R', dict(L=2))]:
        print(f"  {n:<34} {go_bias(run, P, hours=None)}", flush=True)
