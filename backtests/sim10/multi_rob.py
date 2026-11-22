import sys; sys.path.insert(0, '/home/claude/analyst/backtests/sim'); sys.path.insert(0, '/home/claude/analyst/backtests/sim10')
from multi import *
import harness, smc_3y, collections, random
from smc import cost_of, pip_of
def st(o):
    R = [r for _, r in o]; n = len(R); return f"{n:4d}tr {sum(R):+6.1f}R {sum(R)/max(1,n):+.2f}/tr"
both = lambda x: (1, -1)
print("RANDOM 4H 3y both dirs (k1.5 TP3):", end=' ')
o = []
for p in smc_3y.LONG:
    b = harness.D4[p]; c = cost_of(p) * pip_of(p); rnd = random.Random(3)
    for i in range(30, len(b) - 1, 5):
        if not b[i]['atr']: continue
        d = rnd.choice((1, -1)); e = b[i]['c']; r = 1.5 * b[i]['atr']; s = e - d * r; t = e + d * 3 * r; res = None
        for j in range(i + 1, min(len(b), i + 31)):
            y = b[j]
            if (y['l'] <= s) if d > 0 else (y['h'] >= s): res = -1; break
            if (y['h'] >= t) if d > 0 else (y['l'] <= t): res = 3; break
        else: j = min(len(b) - 1, i + 30); res = d * (b[j]['c'] - e) / r
        o.append((b[i]['t'], res - c / r))
print(st(o))
for kd in ['us30_setup', 'sqz_zero', 'sqz_flip', 'wt_os']:
    print(f"\n=== {kd} · 4H · 3 years · 6 pairs · no bias")
    for k, tp in [(1.0, 2), (1.5, 2), (1.5, 3), (2.0, 3), (1.5, 4)]:
        o = []
        for p in smc_3y.LONG: o += trades(harness.D4[p], kd, both, cost_of(p) * pip_of(p), k, tp, 30)
        print(f"   SL {k}ATR TP{tp}: {st(o)}")
    o = []; byp = collections.defaultdict(list); byy = collections.defaultdict(list)
    for p in smc_3y.LONG:
        t = trades(harness.D4[p], kd, both, cost_of(p) * pip_of(p), 1.5, 3, 30); o += t; byp[p] += t
        for x in t: byy[x[0].year].append(x)
    print("   per pair: " + " · ".join(f"{p} {sum(r for _, r in v):+.0f}R/{len(v)}" for p, v in byp.items()))
    print("   per year: " + " · ".join(f"{y} {sum(r for _, r in v):+.0f}R/{len(v)}" for y, v in sorted(byy.items())))
