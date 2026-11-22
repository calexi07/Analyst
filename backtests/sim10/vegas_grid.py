import sys; sys.path.insert(0, '/home/claude/analyst/backtests/sim'); sys.path.insert(0, '/home/claude/analyst/backtests/sim10')
import vegas, harness, smc_3y, collections
from smc import H, cost_of, pip_of
from multi_10y import agg, PAIRS
from core import load, COST
def st(o):
    R = [r for _, r in o]; n = len(R)
    if not n: return '      0tr'
    yrs = collections.defaultdict(float)
    for t, r in o: yrs[t.year] += r
    return f"{n:5d}tr {sum(R)/n:+.2f}/tr" + (f" y+{sum(v > 0 for v in yrs.values())}/{len(yrs)}" if len(yrs) > 2 else '')
allw = lambda x: (1, -1)
def biasf(p):
    def f(x):
        if not any(q <= x['t'] < e for q, e in H): return None
        r = harness.B1.get((p, x['wk']))
        return ((1 if r[0] == 'U' else -1),) if r and r[0] in 'UD' else None
    return f
D10 = {tf: {p: vegas.prep(agg(load(p)[0], m)) for p in PAIRS} for tf, m in [('4H', 240), ('1H', 60)]}
for p in harness.ALL: vegas.prep(harness.D4[p]); vegas.prep(harness.D1[p])
print(f"{'entry/SL/exit':30} | {'10y 4H (12)':22} | {'10y 1H (12)':22} | {'3y 4H (6)':18} | {'bias 4H':16} | {'bias 1H':16}")
for entry in ['limit', 'fvg']:
    for sl in ['tunnel', 'atr']:
        for ex in ['tp2', 'tp3', 'tp5', 'tunnel_trail', 'chand']:
            c = []
            for tf, mh in [('4H', 60), ('1H', 120)]:
                o = []
                for p in PAIRS: o += vegas.trades(D10[tf][p], entry, allw, COST[p], sl, ex, mh)
                c.append(st(o))
            o = []
            for p in smc_3y.LONG: o += vegas.trades(harness.D4[p], entry, allw, cost_of(p) * pip_of(p), sl, ex, 60)
            c.append(st(o))
            for data, mh in [(harness.D4, 60), (harness.D1, 120)]:
                o = []
                for p in harness.ALL: o += vegas.trades(data[p], entry, biasf(p), cost_of(p) * pip_of(p), sl, ex, mh)
                c.append(st(o))
            print(f"{entry:7} {sl:6} {ex:12}       | " + " | ".join(c), flush=True)
