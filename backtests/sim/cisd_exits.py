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
V = [('base: TP 3R, BE at 1R', {}),
     ('TP 3R, no BE', dict(be=None)),
     ('TP 2R, no BE', dict(tpR=2, be=None)),
     ('TP 4R, no BE', dict(tpR=4, be=None)),
     ('TP 5R, no BE', dict(tpR=5, be=None)),
     ('TP 4R, BE at 2R', dict(tpR=4, be=2)),
     ('TP 4R, lock +1R at 2R', dict(tpR=4, be=2, belock=1)),
     ('TP 3R, BE at 1.5R', dict(be=1.5)),
     ('50% at 1R + BE, rest TP 3R', dict(part=1)),
     ('50% at 2R, rest TP 4R, no BE', dict(part=2, tpR=4, be=None)),
     ('50% at 2R + BE, rest trail 1 ATR', dict(part=2, tpR=0, be=2, trail=1, tract=2)),
     ('liq target (next HTF high), no BE', dict(liq=True, tpR=3, be=None)),
     ('liq target, BE at 1R', dict(liq=True, tpR=3)),
     ('no TP, trail close-1ATR from +1R', dict(tpR=0, be=None, trail=1, tract=1)),
     ('no TP, trail close-1.5ATR from +1R', dict(tpR=0, be=None, trail=1.5, tract=1)),
     ('no TP, trail 2ATR from +1R', dict(tpR=0, be=None, trail=2, tract=1)),
     ('no TP, chandelier 2ATR from +1R', dict(tpR=0, be=None, trail=2, tract=1, trref='best')),
     ('no TP, chandelier 3ATR from +1R', dict(tpR=0, be=None, trail=3, tract=1, trref='best')),
     ('no TP, BE at 1R, chand 2ATR from 2R', dict(tpR=0, be=1, trail=2, tract=2, trref='best')),
     ('TP 6R, chand 2ATR from +2R', dict(tpR=6, be=None, trail=2, tract=2, trref='best')),
     ('no TP, trail 1.5ATR -> 0.75 after 3R', dict(tpR=0, be=None, trail=1.5, trail2=0.75, tr2at=3, tract=1)),
     ('no TP, swing-low trail from +1R', dict(tpR=0, be=None, swtrail=True, tract=1)),
     ('no TP, BE 1R + swing trail from 1.5R', dict(tpR=0, be=1, swtrail=True, tract=1.5)),
     ('TP 3R, no BE, time exit 48 bars', dict(be=None, tmax=48))]
for n, P in V: print(f"{n:<38} {go(P)}")
