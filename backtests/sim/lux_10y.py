# LuxAlgo internal CHoCH → internal OB limit, on 10 years of 15m (2012-2022), direction from the daily SMA20 trend (no bias history)
import sys; sys.path.insert(0, '/home/claude/analyst/backtests/sim10'); sys.path.insert(0, '/home/claude/analyst/backtests/sim')
import collections, datetime as D
import lux5
from core import load, COST
import smc
def adapt(p):
    bars, ks, info = load(p); out = []
    for x in bars:
        y = dict(x); y['lt'] = x['t']; y['cd'] = x['d']; y['day'] = x['d']; y['wk'] = x['t'].isocalendar()[:2]; out.append(y)
    prevd = {k: dict(sma=v['sma']) for k, v in info.items()}
    return out, prevd, None
for p in ['EURUSD', 'GBPUSD', 'XAUUSD', 'EURJPY', 'USDJPY', 'GBPJPY']:
    data = adapt(p)
    smc.cost_of = lambda q, p=p: 1.0; smc.pip_of = lambda q, p=p: COST[p]; lux5.cost_of = smc.cost_of; lux5.pip_of = smc.pip_of
    for mode, dirm, tp, tmax in [('choch_ob', 'trend', 2.0, 16), ('choch_ob', 'both', 2.0, 16), ('choch', 'trend', 3.0, 16)]:
        o = lux5.run(p, data, 5, mode, dirm, tp, (540, 1080), tmax, 8)
        R = [r for _, r in o]; yrs = collections.defaultdict(float)
        for t, r in o: yrs[t.year] += r
        print(f"{p} {mode:8} {dirm:5} TP{tp:.0f}: {len(R)}tr {sum(R):+.1f}R {sum(R)/max(1,len(R)):+.3f}/tr · years+ {sum(v>0 for v in yrs.values())}/{len(yrs)}")
