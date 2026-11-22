# BE MACD (1H, MACD 12/26 + SMA9 signal, any cross in the bias direction, 06-22 Bucharest, SL 1.5 ATR) with many exits:
# targets, break-even / profit locks, step ladders, ATR and chandelier trailing, Supertrend, swing pivots, partials,
# and indicator exits (MACD, squeeze, VWAP-type). Bias weeks W40-W47, 14 pairs. Conservative: stop before target in a bar.
import sys, os, json, itertools, collections, statistics as St, multiprocessing as MP
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness
from smc import B, H, cost_of, pip_of
import macd as M, st as ST
B.clear(); B.update(harness.B1)
D1 = harness.D1; ALL = list(D1)
_ind = {}
def ind(p):
    if p in _ind: return _ind[p]
    b = D1[p]; m, sg, hs = M.macd(b)
    up, dn, tr, _ = ST.supertrend(b, 10, 3.0)
    up2, dn2, tr2, _ = ST.supertrend(b, 10, 2.0)
    _ind[p] = dict(m=m, hs=hs, st=(up, dn, tr), st2=(up2, dn2, tr2))
    return _ind[p]

DEF = dict(slk=1.5, tpR=3.0, be=None, lock=None, ladder=None, trail=None, tract=0.0, tsrc='close', st=None, piv=None,
           part=None, mx=None, mxR=0.0, tmax=None, fri=False)
def run(p, P, start, end):
    P = {**DEF, **P}; b = D1[p]; I = ind(p); m, hs = I['m'], I['hs']; cost = cost_of(p) * pip_of(p)
    res = []; pos = None
    for i in range(3, len(b)):
        x = b[i]; A = x['atr']
        if np.isnan(hs[i - 2]): continue
        h0, h1, h2 = hs[i], hs[i - 1], hs[i - 2]
        if pos:
            d = pos['d']; r = pos['r']; px = None
            if (x['l'] <= pos['sl']) if d > 0 else (x['h'] >= pos['sl']):
                px = min(x['o'], pos['sl']) if d > 0 else max(x['o'], pos['sl']); why = 'SL'
            elif pos['tp'] and ((x['h'] >= pos['tp']) if d > 0 else (x['l'] <= pos['tp'])):
                px = max(x['o'], pos['tp']) if d > 0 else min(x['o'], pos['tp']); why = 'TP'
            # partial: first half at partR
            if px is None and P['part'] and not pos['pd'] and ((x['h'] - pos['e']) * d if d > 0 else (pos['e'] - x['l'])) >= P['part'][0] * r:
                pos['bank'] += P['part'][1] * P['part'][0]; pos['w'] -= P['part'][1]; pos['pd'] = True
                if P['part'][2] is not None: pos['sl'] = max(pos['sl'], pos['e'] + P['part'][2] * r) if d > 0 else min(pos['sl'], pos['e'] - P['part'][2] * r)
            if px is None:
                bR = pos['best'] / r
                if P['mx'] and bR >= P['mxR']:
                    if P['mx'] == 'cross' and d * h0 < 0: px, why = x['c'], 'MACD'
                    elif P['mx'] == 'fade2' and d * (h0 - h1) < 0 and d * (h1 - h2) < 0: px, why = x['c'], 'fade'
                    elif P['mx'] == 'st' and I['st'][2][i] == -d: px, why = x['c'], 'STflip'
                if P['tmax'] and i - pos['i'] >= P['tmax']: px, why = x['c'], 'time'
                if P['fri'] and x['dow'] == 4 and x['last_of_day']: px, why = x['c'], 'Fri'
            if px is not None:
                R = pos['bank'] + pos['w'] * d * (px - pos['e']) / r - cost / r
                res.append(dict(p=p, d=d, t=pos['t'], tx=x['tc'], wk=pos['wk'], R=R, why=why, mfe=pos['best'] / r)); pos = None
            else:
                pos['best'] = max(pos['best'], d * ((x['h'] if d > 0 else x['l']) - pos['e'])); bR = pos['best'] / r
                ns = None
                def tight(v):
                    pos['sl'] = max(pos['sl'], v) if d > 0 else min(pos['sl'], v)
                if P['be'] and bR >= P['be'][0]: tight(pos['e'] + d * P['be'][1] * r)
                if P['lock']:
                    for trig, lk in P['lock']:
                        if bR >= trig: tight(pos['e'] + d * lk * r)
                if P['ladder'] and bR >= P['ladder'][0]:     # stop trails best R minus a fixed gap (in R), in whole steps
                    step = P['ladder'][2]; lk = (int(bR / step) * step) - P['ladder'][1]; tight(pos['e'] + d * lk * r)
                if P['trail'] and bR >= P['tract']:
                    k = P['trail'][1] if len(P['trail']) > 1 and P['trail'][1] and bR >= P['trail'][2] else P['trail'][0]
                    ref = x['c'] if P['tsrc'] == 'close' else (pos['e'] + d * pos['best'])
                    tight(ref - d * k * A)
                if P['st'] and bR >= P['st'][1]:
                    up, dn, tr = I['st'] if P['st'][0] == 3 else I['st2']
                    ln = up[i] if d > 0 else dn[i]
                    if ln is not None and tr[i] == d: tight(ln)
                if P['piv'] and bR >= P['piv'][1]:            # last confirmed swing low/high (L bars each side)
                    L = P['piv'][0]; k = i - L
                    if k - L >= 0:
                        seg = b[k - L:k + L + 1]
                        if d > 0 and b[k]['l'] == min(y['l'] for y in seg): tight(b[k]['l'] - 0.1 * A)
                        if d < 0 and b[k]['h'] == max(y['h'] for y in seg): tight(b[k]['h'] + 0.1 * A)
        if pos or A is None or not (start <= x['t'] < end): continue
        d = 1 if h0 > 0 >= h1 else -1 if h0 < 0 <= h1 else None
        if d is None: continue
        bi_ = B.get((p, x['wk']), ('-',))[0]; bd = 1 if bi_ == 'U' else -1 if bi_ == 'D' else 0
        if bd != d or not (6 <= x['hr'] < 22): continue
        e = x['c']; r = P['slk'] * A
        pos = dict(d=d, e=e, r=r, sl=e - d * r, tp=e + d * P['tpR'] * r if P['tpR'] else None, t=x['t'], wk=x['wk'], best=0.0, i=i, bank=0.0, w=1.0, pd=False)
    return res

def ev(P):
    hs = [sum([run(p, P, s, e) for p in ALL], []) for s, e in H]
    t = sorted(hs[0] + hs[1], key=lambda x: x['tx']); eq = pk = dd = 0
    for x in t: eq += x['R']; pk = max(pk, eq); dd = min(dd, eq - pk)
    pp = collections.defaultdict(float)
    for x in t: pp[x['p']] += x['R']
    giveback = sum(1 for x in t if x['R'] < 0 and x['mfe'] >= 2)
    return P, dict(n=len(t), h1=sum(x['R'] for x in hs[0]), h2=sum(x['R'] for x in hs[1]), dd=dd, win=sum(x['R'] > 0 for x in t),
                   neg=sum(v < 0 for v in pp.values()), gb=giveback, mfe2=sum(1 for x in t if x['mfe'] >= 2), mfe3=sum(1 for x in t if x['mfe'] >= 3))

def jobs():
    J = []
    for tp in [3.0, 4.0, 6.0, None]:
        base = dict(tpR=tp)
        J.append(base)
        for be in [(1.0, 0.0), (1.5, 0.0), (2.0, 0.0), (1.0, 0.2), (2.0, 1.0)]: J.append({**base, 'be': be})
        for lk in [((1.5, 0.0), (2.0, 1.0)), ((1.0, 0.0), (2.0, 1.0), (3.0, 2.0)), ((2.0, 0.5), (3.0, 1.5)), ((2.0, 1.0), (3.0, 2.0), (4.0, 3.0))]:
            J.append({**base, 'lock': lk})
        for lad in [(1.0, 1.0, 0.5), (1.5, 1.0, 0.5), (2.0, 1.0, 1.0), (1.0, 1.5, 0.5), (2.0, 1.5, 0.5)]: J.append({**base, 'ladder': lad})
        for k in [0.75, 1.0, 1.5, 2.0, 3.0]:
            for act in [0.0, 1.0, 1.5, 2.0]:
                for src in ['close', 'best']:
                    J.append({**base, 'trail': (k,), 'tract': act, 'tsrc': src})
                    J.append({**base, 'trail': (k, k / 2, 2.0), 'tract': act, 'tsrc': src})
        for stp in [(3, 0.0), (3, 1.0), (3, 2.0), (2, 0.0), (2, 1.0), (2, 2.0)]: J.append({**base, 'st': stp})
        for pv in [(2, 1.0), (3, 1.0), (5, 1.0), (3, 0.0), (3, 2.0), (5, 2.0)]: J.append({**base, 'piv': pv})
        for pt in [(1.0, 0.5, 0.0), (1.5, 0.5, 0.0), (2.0, 0.5, 0.0), (2.0, 0.5, 1.0), (1.0, 0.5, None), (2.0, 0.5, None)]: J.append({**base, 'part': pt})
        for mx in [('cross', 0.0), ('cross', 1.0), ('cross', 2.0), ('fade2', 1.0), ('fade2', 2.0), ('st', 0.0), ('st', 1.0)]:
            J.append({**base, 'mx': mx[0], 'mxR': mx[1]})
        for tm in [24, 48]: J.append({**base, 'tmax': tm})
        J.append({**base, 'fri': True})
        # combinations of the usual winners
        for be in [None, (1.0, 0.0), (1.5, 0.0)]:
            for k in [1.0, 1.5, 2.0]:
                for act in [1.0, 2.0]:
                    for pt in [None, (1.0, 0.5, 0.0), (2.0, 0.5, None)]:
                        J.append({**base, 'be': be, 'trail': (k,), 'tract': act, 'tsrc': 'best', 'part': pt})
                        J.append({**base, 'be': be, 'trail': (k,), 'tract': act, 'tsrc': 'close', 'part': pt})
    return J
if __name__ == '__main__':
    if len(sys.argv) > 1: print(ev(json.loads(sys.argv[1]))[1]); sys.exit()
    J = jobs(); print(len(J), 'runs', flush=True)
    with MP.Pool(2) as pool: R = pool.map(ev, J, chunksize=10)
    json.dump(R, open('/tmp/macdx.json', 'w')); print('done')
