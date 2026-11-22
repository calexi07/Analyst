import sys; sys.path.insert(0, '/home/claude/analyst/backtests/sim'); sys.path.insert(0, '/home/claude/analyst/backtests/sim10')
from ma_react import ma_signals, trades
import harness, smc_3y, collections
from smc import H, cost_of, pip_of
from multi_10y import agg, PAIRS
from core import load, COST
def st(o):
    R = [r for _, r in o]; n = len(R)
    if not n: return '   0tr'
    yrs = collections.defaultdict(float)
    for t, r in o: yrs[t.year] += r
    return f"{n:5d}tr {sum(R):+7.1f}R {sum(R)/n:+.2f}/tr" + (f" yrs+ {sum(v > 0 for v in yrs.values())}/{len(yrs)}" if len(yrs) > 2 else '')
allw = lambda x: (1, -1)
def biasf(p, against=False):
    def f(x):
        if not any(q <= x['t'] < e for q, e in H): return None
        r = harness.B1.get((p, x['wk']))
        if not r or r[0] not in 'UD': return None
        v = 1 if r[0] == 'U' else -1; return (-v,) if against else (v,)
    return f
D10 = {tf: {p: agg(load(p)[0], m) for p in PAIRS} for tf, m in [('4H', 240), ('1H', 60)]}
print(f"{'variant':34} | {'4H bias W40-47':24} | {'4H against':20} | {'1H bias':22} | {'4H 3y 6 pairs':24} | {'4H 10y 12 instr':34} | {'1H 10y 12 instr':34}")
for touch in ['ema50', 'smma50', 'smma100', 'zone']:
    for sl in ['wick', 'smma100', 'atr']:
        for tp in [2.0, 3.0]:
            cells = []
            for data, mh, f in [(harness.D4, 30, biasf), (harness.D4, 30, lambda p: biasf(p, True)), (harness.D1, 60, biasf)]:
                o = []
                for p in harness.ALL: o += trades(data[p], ma_signals(data[p], touch), f(p), cost_of(p) * pip_of(p), sl, tp, mh)
                cells.append(st(o))
            o = []
            for p in smc_3y.LONG: o += trades(harness.D4[p], ma_signals(harness.D4[p], touch), allw, cost_of(p) * pip_of(p), sl, tp, 30)
            cells.append(st(o))
            for tf, mh in [('4H', 30), ('1H', 60)]:
                o = []
                for p in PAIRS: o += trades(D10[tf][p], ma_signals(D10[tf][p], touch), allw, COST[p], sl, tp, mh)
                cells.append(st(o))
            print(f"touch {touch:7} SL {sl:7} TP{tp:.0f}          | " + " | ".join(cells), flush=True)
