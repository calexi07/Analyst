import sys; sys.path.insert(0, '/home/claude/analyst/backtests/sim'); sys.path.insert(0, '/home/claude/analyst/backtests/sim10')
import vegas, harness, smc_3y, collections
from smc import H, cost_of, pip_of
from multi_10y import agg, PAIRS
from core import load, COST
# 1) reaction statistic at the tunnel, 10y
from ma_touch_stat import first
for tf, m in [('4H', 240), ('1H', 60)]:
    s = {'touch tunnel': [0, 0], 'no touch': [0, 0]}
    for p in PAIRS:
        b = vegas.prep(agg(load(p)[0], m))
        for i in range(200, len(b) - 1):
            x = b[i]
            if not x['atr']: continue
            d = 1 if x['t1'] > x['t2'] and x['c'] > x['tb'] else -1 if x['t1'] < x['t2'] and x['c'] < x['tt'] else 0
            if not d: continue
            k = 'touch tunnel' if x['l'] <= x['tt'] and x['h'] >= x['tb'] else 'no touch'
            r = first(b, i, d)
            if r is None: continue
            s[k][0] += r; s[k][1] += 1
    print(f"REACTION {tf}: " + " · ".join(f"{k}: {v[0]/v[1]:.1%} of {v[1]}" for k, v in s.items()), flush=True)
