import sys, datetime as D; sys.path.insert(0, '/home/claude/analyst/backtests/sim'); sys.path.insert(0, '/home/claude/analyst/backtests/sim10')
from ideas import *
import importlib, cet; importlib.reload(cet)
print('--- 10y fade of the CET break (no bias)')
for p in ['EURUSD', 'GBPUSD', 'XAUUSD']:
    bars, ks, info = load(p); f = lambda d, b: (1, -1)
    for tp in [1, 2]:
        print(summary(cet.cet_trades(bars, f, COST[p], 480, 1080, tp, 'opp', fade=True), f"{p} CET FADE 08-18 tp{tp}"))
print('--- 2026, 1H, 14 pairs, weekly bias (W40-W47)')
import harness
from smc import H, cost_of, pip_of
from zoneinfo import ZoneInfo
BUC = ZoneInfo('Europe/Bucharest'); tot = []; anti = []
for p in harness.ALL:
    bb = []
    for x in harness.D1[p]:
        lt = x['t'].astimezone(BUC); bb.append(dict(t=x['t'], d=lt.date(), m=lt.hour * 60 + lt.minute, o=x['o'], h=x['h'], l=x['l'], c=x['c'], wk=x['wk']))
    def f(d, b, p=p, s=1):
        if not any(a <= b['t'] < e for a, e in H): return ()
        r = harness.B1.get((p, b['wk']))
        return ((1 if r[0] == 'U' else -1) * s,) if r and r[0] in 'UD' else ()
    c = cost_of(p) * pip_of(p)
    tot += cet.cet_trades(bb, f, c, 360, 1080, 2.0, 'opp'); anti += cet.cet_trades(bb, lambda d, b, p=p: tuple(-x for x in f(d, b)), c, 360, 1080, 2.0, 'opp')
R = [x[1] for x in tot]; A = [x[1] for x in anti]
print(f"CET 1H with bias: {len(R)} trades {sum(R):+.1f}R {sum(R)/max(1,len(R)):+.2f}/tr | against bias: {len(A)} trades {sum(A):+.1f}R")
