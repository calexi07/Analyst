# 3-year robustness for cisd.py: 4H chart, HTF = Daily (and Weekly), 6 long-history pairs.
# Direction filter (no engine bias before W40): previous week's last daily close vs 20-day SMA, fixed for the week.
import sys, os, collections, datetime as D
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smc, smc_3y, cisd
from smc_3y import LONG, DATA, YRS
def wkdir(b):
    closes = {}; [closes.__setitem__(x['day'], x['c']) for x in b]
    days = sorted(closes); out = {}; wk_last = {}
    for i, d in enumerate(days):
        if i >= 19: wk_last[d.isocalendar()[:2]] = (closes[d] - sum(closes[q] for q in days[i - 19:i + 1]) / 20)
    wks = sorted(wk_last)
    for a, nx in zip(wks, wks[1:]): out[nx] = 'U' if wk_last[a] > 0 else 'D'
    return out
for p in LONG:
    for wk, v in wkdir(DATA[p]).items(): cisd.B[(p, wk)] = (v,)
def htfW(x, htf):
    return x['wk'] if htf == 'W' else x['day']
cisd.htf_key = htfW
for n, P in [('HTF D, both directions', dict()), ('HTF D, trend direction', dict(bias=True)), ('HTF D, trend, no BE', dict(bias=True, be=None)),
             ('HTF W, both directions', dict(htf='W')), ('HTF W, trend direction', dict(htf='W', bias=True)), ('HTF W, trend, no BE', dict(htf='W', bias=True, be=None))]:
    ys = [sum([cisd.run(p, DATA[p], P, a, c) for p in LONG], []) for a, c in YRS]
    t = sorted(sum(ys, []), key=lambda x: x['tx']); eq = pk = dd = 0
    for x in t: eq += x['R']; pk = max(pk, eq); dd = min(dd, eq - pk)
    w = sum(x['R'] > 0 for x in t) / max(1, len(t))
    print(f"{n:<26} {len(t):4}tr {eq:+6.1f}R  {eq / max(1, len(t)):+.2f}R/tr win {w:.0%} dd {dd:+.1f}  by year [{', '.join('%+.1f' % sum(x['R'] for x in y) for y in ys)}]")
