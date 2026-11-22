# London ORB on the 5m path: with the fundamental bias, against it, and without it (OCO both sides, first break wins).
import sys, datetime as D, collections
import intraday as T
U = lambda *a: D.datetime(*a, tzinfo=D.timezone.utc)
p = sys.argv[1]; data = T.prep(p)
print(p, '5m data', data[0][0]['t'].date(), '->', data[0][-1]['t'].date())
def oco(P, a, c):
    L = T.run(p, data, {**P, 'dirm': 'long'}, a, c); S = T.run(p, data, {**P, 'dirm': 'short'}, a, c)
    by = {}
    for x in L + S:
        if x['cd'] not in by or x['t'] < by[x['cd']]['t']: by[x['cd']] = x
    return list(by.values())
def s(t, cut=None):
    n = len(t); tot = sum(x['R'] for x in t)
    h = '' if cut is None else f" halves {sum(x['R'] for x in t if x['t'] < cut):+.1f}/{sum(x['R'] for x in t if x['t'] >= cut):+.1f}"
    eq = pk = dd = 0
    for x in sorted(t, key=lambda z: z['t']): eq += x['R']; pk = max(pk, eq); dd = min(dd, eq - pk)
    return f"{n:3}tr {tot:+6.1f}R ({tot/max(1,n):+.2f}/tr) win {sum(x['R']>0 for x in t)/max(1,n):.0%} dd {dd:+.1f}{h}"
full = (U(2026, 8, 24), U(2026, 11, 21)); bw = (U(2026, 9, 27, 21), U(2026, 11, 21)); cut = U(2026, 10, 25, 21)
for tp in (1.0, 1.5, 2.0, 3.0):
    for tm in (36, 48):
        P = dict(idea='lon_orb', tp=tp, tmax=tm)
        print(f"== TP {tp}R, max {tm*5//60}h")
        print(f"   WITH bias (bias weeks)        {s(T.run(p, data, {**P, 'dirm': 'bias'}, *bw), cut)}")
        print(f"   AGAINST bias (bias weeks)     {s(T.run(p, data, {**P, 'dirm': 'anti'}, *bw), cut)}")
        print(f"   no bias, both sides (bias wks){s(oco(P, *bw), cut)}")
        print(f"   no bias, both sides (all data){s(oco(P, *full), cut)}")
