import sys, collections
sys.path.insert(0, '/home/claude/analyst/backtests/sim10')
import vp
from absorb import loadv
from core import COST, load
from ideas import dirs_for
P = ['EURUSD','GBPUSD','XAUUSD','AUDUSD','USDCAD','USDCHF','USDJPY','EURGBP','EURJPY','EURCHF','GBPJPY','AUDJPY']
B = {p: loadv(p, 15) for p in P}; PR = {p: vp.profiles(B[p]) for p in P}; INFO = {p: load(p)[2] for p in P}
def st(o):
    R = [r for _, r in o]; n = len(R)
    if not n: return '     0tr'
    y = collections.defaultdict(float)
    for t, r in o: y[t.year] += r
    return f"{n:5d}tr {sum(R)/n:+.3f}/tr y+{sum(v > 0 for v in y.values())}/{len(y)}"
n = h = c = 0
for p in P:
    a, b, cc = vp.naked_poc(B[p], PR[p]); n += a; h += a * b; c += a * cc
print(f"NAKED POC: touched within 5 days {h/n:.1%} vs a control level at the same distance on the other side {c/n:.1%} ({n} days)")
for idea, tps in [('80', [None, 2.0]), ('reject', [None, 2.0, 3.0]), ('accept', [2.0, 3.0]), ('poc_pb', [2.0, 3.0])]:
    for tp in tps:
        for dirn in ['none', 'trend', 'against']:
            o = []
            for p in P:
                f = None if dirn == 'none' else (lambda k, p=p: (lambda t: t if dirn == 'trend' else tuple(-v for v in t))(dirs_for(INFO[p][k], 'trend')) if k in INFO[p] else ())
                o += vp.run(B[p], PR[p], idea, COST[p], f, tp=tp)
            print(f"{idea:7} TP {'level' if tp is None else str(tp)+'R':6} {dirn:8}: {st(o)}", flush=True)
