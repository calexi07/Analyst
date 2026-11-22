import sys, collections, time
sys.path.insert(0, '/home/claude/analyst/backtests/sim10')
import sd, sd_data
from core import COST
T0 = time.time()
def st(o):
    R = [x[1] for x in o]; n = len(R)
    if not n: return '     0tr'
    y = collections.defaultdict(float)
    for t, r, z in o: y[t.year] += r
    return f"{n:5d}tr {sum(R):+7.1f}R {sum(R)/n:+.2f}/tr y+{sum(v > 0 for v in y.values())}/{len(y)}"
P = ['EURUSD', 'GBPUSD', 'XAUUSD']
DATA = {p: sd_data.ten_year(p) for p in P}
print(f"data {time.time()-T0:.0f}s", flush=True)
for htf in ['4H', '1H']:
    ZZ = {p: sd.zones(DATA[p][1][htf]) for p in P}
    print(f"\n== HTF {htf}: zones " + ", ".join(f"{p} {len(ZZ[p])}" for p in P), flush=True)
    for dirn in ['trend', 'both']:
        for conf, entry, sl in [('none', 'limit', 'htf'), ('choch', 'mkt', 'ltf'), ('choch', 'mkt', 'htf')]:
            for tp in [2.0, 3.0]:
                o = []
                for p in P:
                    l, hh, trend = DATA[p]
                    f = trend if dirn == 'trend' else (lambda x: (1, -1))
                    o += sd.run(l, hh[htf], ZZ[p], f, COST[p], conf=conf, entry=entry, sl=sl, tp=tp)
                print(f"  {dirn:5} {conf:5} {entry:5} SL {sl:3} TP{tp:.0f}: {st(o)}   ({time.time()-T0:.0f}s)", flush=True)
