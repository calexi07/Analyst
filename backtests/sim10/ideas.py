import sys, itertools, datetime as D
sys.path.insert(0, '/home/claude/analyst/backtests/sim10')
from core import *

def dirs_for(I, mode):
    s = I['sma']; pc = I['pdc']
    if mode == 'both': return (1, -1)
    if s is None or pc is None: return ()
    t = 1 if pc > s else -1
    if mode == 'trend': return (t,)
    if mode == 'anti': return (-t,)
    if mode == 'pday': return (1 if I['pdc'] > I['pdo'] else -1,)

def run(p, idea, P):
    bars, ks, info = load(p); cost = COST[p]; out = []
    for k in ks:
        I = info[k]; ix = I['ix']
        if I['adr'] is None or len(ix) < 60: continue
        D_ = dirs_for(I, P.get('dir', 'trend'))
        if not D_: continue
        xm = P.get('xm', 21 * 60 + 45); done = False
        if idea in ('asia_sweep', 'pd_sweep'):
            if idea == 'asia_sweep': hi, lo = rng(bars, ix, 0, P.get('a1', 8 * 60))
            else: hi, lo = I['pdh'], I['pdl']
            if hi is None: continue
            ext = {1: None, -1: None}
            for q in ix:
                b = bars[q]
                if not (P['w0'] <= b['m'] < P['w1']): continue
                for d in D_:
                    lvl = lo if d > 0 else hi
                    if (b['l'] < lvl) if d > 0 else (b['h'] > lvl):
                        ext[d] = b['l'] if d > 0 and (ext[d] is None or b['l'] < ext[d]) else (b['h'] if d < 0 and (ext[d] is None or b['h'] > ext[d]) else ext[d])
                    if ext[d] is not None and ((b['c'] > lvl) if d > 0 else (b['c'] < lvl)):
                        e = b['c']; sl = ext[d] - d * 0.1 * b['atr']; r = abs(e - sl)
                        if r < 0.3 * b['atr'] or r > P.get('maxr', 0.6) * I['adr']: ext[d] = None; continue
                        tp = (hi if d > 0 else lo) if P['tp'] == 'opp' else e + d * P['tp'] * r
                        if P['tp'] == 'opp' and (tp - e) * d < r: ext[d] = None; continue
                        out.append(manage(bars, ix, q + 1 if q + 1 in ix else q, d, e, sl, tp, xm, cost)[::-1]); done = True; break
                if done: break
        elif idea == 'ema_pb':
            for q in ix:
                b = bars[q]
                if not (P['w0'] <= b['m'] < P['w1']): continue
                for d in D_:
                    if (b['e20'] - b['e50']) * d > 0 and ((b['l'] <= b['e20'] <= b['c']) if d > 0 else (b['h'] >= b['e20'] >= b['c'])) and (b['c'] - b['o']) * d > 0:
                        e = b['c']; sl = (b['l'] if d > 0 else b['h']) - d * 0.2 * b['atr']; r = abs(e - sl)
                        if not (0.3 * b['atr'] <= r <= 4 * b['atr']): continue
                        out.append(manage(bars, ix, q + 1 if q + 1 in ix else q, d, e, sl, e + d * P['tp'] * r, xm, cost)[::-1]); done = True; break
                if done: break
        elif idea == 'orb':
            hi, lo = rng(bars, ix, P['r0'], P['r1'])
            if hi is None or hi <= lo: continue
            for q in ix:
                b = bars[q]
                if b['m'] < P['r1'] or b['m'] >= P['until']: continue
                hit = [d for d in D_ if ((b['h'] >= hi) if d > 0 else (b['l'] <= lo))]
                if hit:
                    d = hit[0]; e = max(b['o'], hi) if d > 0 else min(b['o'], lo); sl = lo if d > 0 else hi
                    if P.get('slm'): sl = (hi + lo) / 2
                    r = abs(e - sl)
                    if r <= 0 or r > P.get('maxr', 0.6) * I['adr']: break
                    out.append(manage(bars, ix, q, d, e, sl, e + d * P['tp'] * r, xm, cost)[::-1]); break
        elif idea == 'mom':      # momentum: at time m, if the move since m0 > f·ADR in an allowed direction, ride it with stop f2·ADR
            v0 = next((bars[q]['o'] for q in ix if bars[q]['m'] >= P['m0']), None)
            q = next((q for q in ix if bars[q]['m'] >= P['m1'] - 15), None)
            if v0 is None or q is None: continue
            mv = bars[q]['c'] - v0; d = 1 if mv > 0 else -1
            if d not in D_ or abs(mv) < P['f'] * I['adr']: continue
            e = bars[q]['c']; sl = e - d * P['s'] * I['adr']
            out.append(manage(bars, ix, q + 1 if q + 1 in ix else q, d, e, sl, e + d * P['tp'] * abs(e - sl), xm, cost)[::-1])
    return [(t, r) for t, r in out]

def run2(p, idea, P):
    """extra ideas: random baseline, momentum with entry times, fades"""
    import random
    bars, ks, info = load(p); cost = COST[p]; out = []
    for k in ks:
        I = info[k]; ix = I['ix']
        if I['adr'] is None or len(ix) < 60: continue
        D_ = dirs_for(I, P.get('dir', 'both'))
        if not D_: continue
        xm = P.get('xm', 21 * 60 + 45)
        if idea == 'random':
            rnd = random.Random(k.toordinal() * 7 + P.get('seed', 0)); m = rnd.choice(range(600, 960, 15)); d = rnd.choice(D_)
            q = next((q for q in ix if bars[q]['m'] >= m), None)
            if q is None: continue
            e = bars[q]['c']; sl = e - d * P['s'] * I['adr']
            out.append(manage(bars, ix, q + 1 if q + 1 in ix else q, d, e, sl, e + d * P['tp'] * abs(e - sl), xm, cost)[::-1])
        elif idea in ('mom', 'fade'):
            v0 = next((bars[q]['o'] for q in ix if bars[q]['m'] >= P['m0']), None)
            q = next((q for q in ix if bars[q]['m'] >= P['m1'] - 15), None)
            if v0 is None or q is None: continue
            mv = bars[q]['c'] - v0; d = (1 if mv > 0 else -1) * (1 if idea == 'mom' else -1)
            if d not in D_ or abs(mv) < P['f'] * I['adr']: continue
            e = bars[q]['c']; sl = e - d * P['s'] * I['adr']
            tp = None if P['tp'] is None else e + d * P['tp'] * abs(e - sl)
            out.append(manage(bars, ix, q + 1 if q + 1 in ix else q, d, e, sl, tp, xm, cost)[::-1])
    return out
