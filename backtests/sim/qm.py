# Quasimodo (QM / over-and-under), bias direction only, 1H.
# Bullish QM: pivot low L1, pivot high H1, lower low L2 < L1, then price breaks above H1 (close) -> limit at L1 (the left
# shoulder), stop below L2 (+0.1 ATR), TP xR; order valid `life` bars, cancelled if price reaches +1R first. Bearish mirrors it.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smc import B, cost_of, pip_of
DEF = dict(cancel1R=True, ctx=None, tpm='R', lifeH=48, L=3, tpR=3, life=48, minR=0.3, maxR=3.0, entry='shoulder', bias=True, hours=None)
def run(p, b, P, start, end):
    P = {**DEF, **P}; L = P['L']; cost = cost_of(p) * pip_of(p); res = []; pos = None; pend = None
    pivs = []   # (index, +1 high / -1 low, price)
    import statistics as _St
    mins = _St.median([(b[j + 1]['t'] - b[j]['t']).total_seconds() / 60 for j in range(min(200, len(b) - 1))]) if len(b) > 1 else 60
    life = int(P['lifeH'] * 60 / mins)
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
            if i - pend['i'] > life or P['cancel1R'] and ((x['h'] >= pend['e'] + pend['r']) if d > 0 else (x['l'] <= pend['e'] - pend['r'])) and not ((x['l'] <= pend['e']) if d > 0 else (x['h'] >= pend['e'])): pend = None
            elif (x['l'] <= pend['e']) if d > 0 else (x['h'] >= pend['e']):
                e = min(x['o'], pend['e']) if d > 0 else max(x['o'], pend['e']); r = abs(e - pend['sl'])
                if (x['l'] <= pend['sl']) if d > 0 else (x['h'] >= pend['sl']): res.append(dict(p=p, d=d, t=x['t'], tx=x['tc'], wk=x['wk'], R=-1 - cost / r))
                else:
                    tp = e + d * P['tpR'] * r
                    if P['tpm'] == 'swing' and pend['ext'] is not None and d * (pend['ext'] - e) >= r: tp = pend['ext']
                    pos = dict(d=d, e=e, r=r, sl=pend['sl'], tp=tp, t=x['t'], wk=x['wk'])
                pend = None
        if pos or pend or A is None or not (start <= x['t'] < end): continue
        bi_ = B.get((p, x['wk']), ('-',))[0]; bd = 1 if bi_ == 'U' else -1 if bi_ == 'D' else 0
        if P['bias'] and bd == 0: continue
        if P['hours'] and not (P['hours'][0] <= x['hr'] < P['hours'][1]): continue
        for d in ((bd,) if P['bias'] else (1, -1)):
            if P['ctx'] is not None and P['ctx'][i] != d: continue
            # last three alternating pivots before now: shoulder S (same side as d's stop), head Hd, neck N
            seq = [q for q in pivs if q[0] < i]
            # H1 = a pivot on the far side (high for a long) that this close breaks; L2 = the deepest opposite pivot after H1;
            # L1 = the last opposite pivot before H1; QM needs L2 beyond L1 (lower low for a long)
            pc = b[i - 1]['c']
            H1 = next((q for q in reversed(seq) if q[1] == d and ((x['c'] > q[2] >= pc) if d > 0 else (x['c'] < q[2] <= pc))), None)
            if not H1: continue
            after = [q for q in seq if q[1] == -d and q[0] > H1[0]]
            before = [q for q in seq if q[1] == -d and q[0] < H1[0]]
            if not after or not before: continue
            L2 = min(after, key=lambda q: q[2]) if d > 0 else max(after, key=lambda q: q[2]); L1 = before[-1]
            if (L1[0], L2[0], H1[0]) in used: continue
            if not ((L2[2] < L1[2]) if d > 0 else (L2[2] > L1[2])): continue
            # price must not have closed beyond H1 between L2 and now (this is the first break)
            if any(((b[j]['c'] > H1[2]) if d > 0 else (b[j]['c'] < H1[2])) for j in range(L2[0], i)): continue
            used.add((L1[0], L2[0], H1[0]))
            e = L1[2] if P['entry'] == 'shoulder' else (L1[2] + L2[2]) / 2 if P['entry'] == 'mid' else (L1[2] + x['c']) / 2 if P['entry'] == 'half' else x['c']
            if P['entry'] == 'break':
                sl = L2[2] - d * 0.1 * A; r = abs(x['c'] - sl)
                if P['minR'] * A <= r <= P['maxR'] * A:
                    ext = max(y['h'] for y in b[L2[0]:i + 1]) if d > 0 else min(y['l'] for y in b[L2[0]:i + 1])
                    pos = dict(d=d, e=x['c'], r=r, sl=sl, tp=x['c'] + d * P['tpR'] * r, t=x['t'], wk=x['wk'])
                break
            sl = L2[2] - d * 0.1 * A; r = abs(e - sl)
            if P['minR'] * A <= r <= P['maxR'] * A and (x['c'] - e) * d > 0: pend = dict(d=d, e=e, sl=sl, r=r, i=i, ext=(max(y['h'] for y in b[L2[0]:i + 1]) if d > 0 else min(y['l'] for y in b[L2[0]:i + 1])))
            break
    return res
if __name__ == '__main__':
    from harness import go_bias
    for n, P in [('QM L3, shoulder, TP 2R', dict(tpR=2)), ('QM L3, shoulder, TP 3R', {}), ('QM L3, shoulder, TP 4R', dict(tpR=4)),
                 ('QM L3, mid shoulder-head, TP 3R', dict(entry='mid')), ('QM L5, shoulder, TP 3R', dict(L=5)), ('QM L2, shoulder, TP 3R', dict(L=2))]:
        print(f"  {n:<34} {go_bias(run, P, hours=None)}", flush=True)
