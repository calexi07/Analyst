import sys, collections
sys.path.insert(0, '/home/claude/analyst/backtests/sim10')
from absorb import loadv, run
from core import COST, load
from ideas import dirs_for
P = ['EURUSD','GBPUSD','XAUUSD','AUDUSD','USDCAD','USDCHF','USDJPY','EURGBP','EURJPY','EURCHF','GBPJPY','AUDJPY']
INFO = {p: load(p)[2] for p in P}
def st(o):
    R = [r for _, r in o]; n = len(R)
    if not n: return '      0tr'
    y = collections.defaultdict(float)
    for t, r in o: y[t.year] += r
    return f"{n:6d}tr {sum(R)/n:+.3f}/tr y+{sum(v > 0 for v in y.values())}/{len(y)}"
for tf, mins, mh in [('4H', 240, 30), ('1H', 60, 48), ('15m', 15, 64)]:
    data = {p: loadv(p, mins) for p in P}
    print(f"\n=== {tf}", flush=True)
    for dirn in ['none', 'trend', 'against-trend']:
        def mk(p):
            if dirn == 'none': return lambda x: None
            def f(x, p=p):
                dd = x['t'].date(); I = INFO[p].get(dd)
                if not I: return ()
                t = dirs_for(I, 'trend'); return t if dirn == 'trend' else tuple(-v for v in t)
            return f
        for k in [1.5, 2.0, 3.0]:
            for res in ['none', 'close_half', 'close_third', 'small_range']:
                for conf, tp in [(False, 2.0), (True, 2.0)]:
                    o = []
                    for p in P: o += run(data[p], COST[p], mk(p), 20, k, res, conf, tp, mh)
                    print(f"  {dirn:13} vol≥{k}× {res:11} {'confirm' if conf else 'at close':8} TP{tp:.0f}: {st(o)}", flush=True)
