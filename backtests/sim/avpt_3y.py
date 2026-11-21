# 3-year robustness for avpt.py on 4H (6 long-history pairs) and pre-W40 on 1H, direction = weekly trend proxy (close vs 20-day SMA).
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smc, smc_3y, avpt
from smc_3y import LONG, DATA, YRS
def wkdir(b):
    closes = {}; [closes.__setitem__(x['day'], x['c']) for x in b]; days = sorted(closes); wl = {}; out = {}
    for i, d in enumerate(days):
        if i >= 19: wl[d.isocalendar()[:2]] = closes[d] - sum(closes[q] for q in days[i - 19:i + 1]) / 20
    ws = sorted(wl)
    for a, nx in zip(ws, ws[1:]): out[nx] = 'U' if wl[a] > 0 else 'D'
    return out
for p in LONG:
    for wk, v in wkdir(DATA[p]).items(): avpt.B[(p, wk)] = (v,)
def rep(n, ys):
    t = sorted(sum(ys, []), key=lambda x: x['tx']); eq = pk = dd = 0
    for x in t: eq += x['R']; pk = max(pk, eq); dd = min(dd, eq - pk)
    print(f"{n:<34} {len(t):4}tr {eq:+6.1f}R {eq / max(1, len(t)):+.2f}R/tr dd {dd:+.1f} [{', '.join('%+.1f' % sum(x['R'] for x in y) for y in ys)}]")
for n, P in [('Balanced, both dirs', {}), ('Balanced, trend dir', dict(bias=True)), ('Balanced, trend, 06-22', dict(bias=True, hours=(6, 22))),
             ('Aggressive, trend dir', dict(prof='aggr', bias=True)), ('Deep, trend dir', dict(prof='deep', bias=True)),
             ('Balanced, trend, no BE', dict(bias=True, be=False))]:
    rep('4H 3y ' + n, [sum([avpt.run(p, DATA[p], P, a, c) for p in LONG], []) for a, c in YRS])
