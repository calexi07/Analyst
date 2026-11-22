# "Support and Resistance Levels with Breaks [LuxAlgo]": resistance = last confirmed pivot high (L/R bars), support = last pivot low.
# Long when the close crosses above resistance (short: below support). The volume filter cannot be used (no volume in FX data);
# 'body' = the script's "B" break (not a wick break), 'wick' = its "Bull/Bear Wick" break, 'any' = both.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smc import B, cost_of, pip_of
DEF = dict(L=15, R=15, kind='any', entry='close', sl='atr', slk=1.0, tpR=3, trail=0, tract=1, be=None, bias=True, hours=None, tmax=0, maxR=3)
def pivots(b, L, R, key, f):
    out = [None] * len(b); last = None
    for i in range(len(b)):
        k = i - R
        if k - L >= 0:
            v = b[k][key]; w = [x[key] for x in b[k - L:i + 1]]
            if v == f(w) and w.count(v) >= 1 and all((x != v) or (j == L) for j, x in enumerate(w) if j < L): last = (k, v)
        out[i] = last
    return out
def run(p, b, P, start, end):
    P = {**DEF, **P}; cost = cost_of(p) * pip_of(p)
    ph = pivots(b, P['L'], P['R'], 'h', max); pl = pivots(b, P['L'], P['R'], 'l', min)
    res = []; pos = None; pend = None
    for i in range(2, len(b)):
        x = b[i]; A = x['atr']
        if pos:
            d = pos['d']; px = None
            if (x['l'] <= pos['sl']) if d > 0 else (x['h'] >= pos['sl']): px = min(x['o'], pos['sl']) if d > 0 else max(x['o'], pos['sl']); why = 'SL'
            elif pos['tp'] and ((x['h'] >= pos['tp']) if d > 0 else (x['l'] <= pos['tp'])): px = max(x['o'], pos['tp']) if d > 0 else min(x['o'], pos['tp']); why = 'TP'
            elif P['tmax'] and i - pos['i'] >= P['tmax']: px = x['c']; why = 'time'
            if px is not None:
                res.append(dict(p=p, d=d, t=pos['t'], tx=x['tc'], wk=pos['wk'], R=d * (px - pos['e']) / pos['r'] - cost / pos['r'], why=why)); pos = None
            else:
                pos['best'] = max(pos['best'], d * ((x['h'] if d > 0 else x['l']) - pos['e']))
                if P['be'] is not None and pos['best'] >= P['be'] * pos['r']: pos['sl'] = pos['sl'] if d * (pos['sl'] - pos['e']) >= 0 else pos['e']
                if P['trail'] and pos['best'] >= P['tract'] * pos['r']:
                    ns = x['c'] - d * P['trail'] * A; pos['sl'] = max(pos['sl'], ns) if d > 0 else min(pos['sl'], ns)
        if pend and not pos:
            d = pend['d']
            if i - pend['i'] > 10: pend = None
            elif (x['l'] <= pend['e']) if d > 0 else (x['h'] >= pend['e']):
                e = min(x['o'], pend['e']) if d > 0 else max(x['o'], pend['e'])
                pos = dict(i=i, d=d, e=e, r=pend['r'], sl=e - d * pend['r'], tp=e + d * P['tpR'] * pend['r'] if P['tpR'] else None, t=x['t'], wk=x['wk'], best=0); pend = None
                if (x['l'] <= pos['sl']) if d > 0 else (x['h'] >= pos['sl']):
                    res.append(dict(p=p, d=d, t=x['t'], tx=x['tc'], wk=x['wk'], R=-1 - cost / pos['r'], why='SL fill bar')); pos = None
        if A is None or pos or not (start <= x['t'] < end): continue
        for d, lv, prev in ((1, ph[i - 1], ph[i - 2]), (-1, pl[i - 1], pl[i - 2])):
            if lv is None: continue
            lvl = lv[1]; pc = b[i - 1]['c']
            cross = (x['c'] > lvl and pc <= lvl) if d > 0 else (x['c'] < lvl and pc >= lvl)
            if not cross: continue
            wick = (x['o'] - x['l'] > x['c'] - x['o']) if d > 0 else (x['o'] - x['c'] < x['h'] - x['o'])
            if P['kind'] == 'body' and wick or P['kind'] == 'wick' and not wick: continue
            bi_ = B.get((p, x['wk']), ('-',))[0]; bd = 1 if bi_ == 'U' else -1 if bi_ == 'D' else 0
            if P['bias'] and bd != d: continue
            if P['hours'] and not (P['hours'][0] <= x['hr'] < P['hours'][1]): continue
            e = x['c'] if P['entry'] == 'close' else lvl
            if P['sl'] == 'atr': r = P['slk'] * A
            elif P['sl'] == 'bar': r = abs(e - (x['l'] if d > 0 else x['h'])) + 0.1 * A
            else:  # opposite level (support for longs)
                ol = pl[i] if d > 0 else ph[i]
                if ol is None: continue
                r = abs(e - ol[1]) + 0.1 * A
            if not (0.3 * A <= r <= P['maxR'] * A): continue
            if P['entry'] == 'close':
                pos = dict(i=i, d=d, e=e, r=r, sl=e - d * r, tp=e + d * P['tpR'] * r if P['tpR'] else None, t=x['t'], wk=x['wk'], best=0)
            else:
                pend = dict(i=i, d=d, e=e, r=r)
            break
    return res
if __name__ == '__main__':
    from harness import go
    V = [('15/15, any break, close, SL 1 ATR, TP 3R', {}),
         ('  body breaks only ("B")', dict(kind='body')),
         ('  wick breaks only', dict(kind='wick')),
         ('  SL at opposite level (support)', dict(sl='opp')),
         ('  SL beyond break candle', dict(sl='bar')),
         ('  TP 2R', dict(tpR=2)),
         ('  TP 4R', dict(tpR=4)),
         ('  your exit: TP 4R, trail 0.75 ATR from close', dict(tpR=4, trail=0.75, tract=0)),
         ('  retest: limit at the broken level', dict(entry='retest')),
         ('  retest, SL beyond break candle, TP 3R', dict(entry='retest', sl='bar')),
         ('10/10, any, close, TP 3R', dict(L=10, R=10)),
         ('10/10, retest, TP 3R', dict(L=10, R=10, entry='retest')),
         ('5/5, any, close, TP 3R', dict(L=5, R=5)),
         ('5/5, retest, TP 3R', dict(L=5, R=5, entry='retest')),
         ('20/20, any, close, TP 3R', dict(L=20, R=20))]
    for n, P in V: print(f"{n:<46} {go(run, P)}")
