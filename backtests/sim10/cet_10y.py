import sys; sys.path.insert(0, '/home/claude/analyst/backtests/sim10')
from ideas import *
from cet import cet_trades
for p in ['EURUSD', 'GBPUSD', 'XAUUSD']:
    bars, ks, info = load(p)
    for dm in ['both', 'trend']:
        f = lambda d, b, dm=dm: dirs_for(info[d], dm) if d in info else ()
        for (w0, w1, lab) in [(300, 780, '05-13 (indicator 3-10 GMT)'), (480, 1080, '08-18')]:
            for tp, sl in [(2, 'opp'), (3, 'opp'), (2, 'mid')]:
                print(summary(cet_trades(bars, f, COST[p], w0, w1, tp, sl), f"{p} CET {lab} {dm} tp{tp} sl{sl}"))
