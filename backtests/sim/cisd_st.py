# Exit variants for the CISD breaker model: 1H/HTF D W40-47 (engine bias, 06-22), pre-W40 (both dirs, 06-22), 3y 4H/HTF D (trend dir).
import sys, os, io, contextlib, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cisd
from smc import prep, H, PRE, USDP, EURP
ALL = USDP + EURP; D1 = {p: prep(p) for p in ALL}
B1 = dict(cisd.B)
with contextlib.redirect_stdout(io.StringIO()):
    import cisd_3y                      # loads 4H data + trend dir into cisd.B, patches htf_key
from smc_3y import LONG, DATA as D4, YRS
B4 = dict(cisd.B); hk4 = cisd.htf_key
import importlib; orig_hk = importlib.reload(cisd).htf_key   # fresh module for the 1H runs
def stats(t):
    t = sorted(t, key=lambda x: x['tx']); eq = pk = dd = 0
    for x in t: eq += x['R']; pk = max(pk, eq); dd = min(dd, eq - pk)
    return len(t), eq, dd, sum(x['R'] > 0 for x in t) / max(1, len(t))
def go(P):
    cisd.B.clear(); cisd.B.update(B1); cisd.htf_key = orig_hk
    a = stats(sum([cisd.run(p, D1[p], {**P, 'bias': True, 'hours': (6, 22)}, s, e) for p in ALL for s, e in H], []))
    b = stats(sum([cisd.run(p, D1[p], {**P, 'hours': (6, 22)}, *PRE) for p in ALL], []))
    cisd.B.clear(); cisd.B.update(B4); cisd.htf_key = hk4
    ys = [sum([cisd.run(p, D4[p], {**P, 'bias': True}, s, e) for p in LONG], []) for s, e in YRS]
    c = stats(sum(ys, []))
    yr = ','.join('%+.0f' % sum(x['R'] for x in y) for y in ys)
    return f"W40-47 {a[0]:2}tr {a[1]:+5.1f}R dd{a[2]:+5.1f} | preW40 {b[0]:2}tr {b[1]:+5.1f}R | 3y {c[0]:3}tr {c[1]:+5.1f}R {c[1]/max(1,c[0]):+.2f}/tr dd{c[2]:+5.1f} win {c[3]:.0%} [{yr}]"
V = [('TP 3R, no BE (best so far)', dict(be=None)),
     ('liq target, no BE', dict(liq=True, be=None)),
     ('ST 10/3 trail from entry, no TP', dict(tpR=0, be=None, stm=3, tract=0)),
     ('ST 10/3 trail from +1R, no TP', dict(tpR=0, be=None, stm=3, tract=1)),
     ('ST 10/2 trail from +1R, no TP', dict(tpR=0, be=None, stm=2, tract=1)),
     ('ST 10/3 trail from +1R, TP 3R', dict(tpR=3, be=None, stm=3, tract=1)),
     ('ST 10/3 trail from +2R, TP 4R', dict(tpR=4, be=None, stm=3, tract=2)),
     ('ST 10/3 trail from +2R, no TP', dict(tpR=0, be=None, stm=3, tract=2)),
     ('ST 10/2 trail from +2R, TP 5R', dict(tpR=5, be=None, stm=2, tract=2))]
for n, P in V: print(f"{n:<38} {go(P)}")
