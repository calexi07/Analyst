import sys; sys.path.insert(0, '/home/claude/analyst/backtests/sim'); sys.path.insert(0, '/home/claude/analyst/backtests/sim10')
from multi import *
import harness, smc_3y
from smc import H, cost_of, pip_of
from zoneinfo import ZoneInfo
BUC = ZoneInfo('Europe/Bucharest')
for d in (harness.D1, harness.D4):
    for p in d:
        for x in d[p]: x['bh'] = x['t'].astimezone(BUC).hour
def st(o):
    R = [r for _, r in o]; n = len(R); return f"{n:4d}tr {sum(R):+6.1f}R {sum(R)/max(1,n):+.2f}/tr"
KINDS = ['eob', 'obob', 'wt', 'wt_os', 'sqz_flip', 'sqz_zero', 'sqz_fire', 'us30', 'us30_setup', 'bos']
print(f"{'signal':12} | {'1H bias W40-47 (14 pairs)':30} | {'1H AGAINST bias':22} | {'4H bias':22} | {'4H 3y trend (6 pairs)':24} | {'4H 3y both dirs':22}")
for kd in KINDS:
    row = []
    for data, mh, against in [(harness.D1, 48, False), (harness.D1, 48, True), (harness.D4, 30, False)]:
        o = []
        for p in harness.ALL:
            c = cost_of(p) * pip_of(p)
            def f(x, p=p):
                if not any(q <= x['t'] < e for q, e in H): return None
                r = harness.B1.get((p, x['wk']))
                if not r or r[0] not in 'UD': return None
                v = 1 if r[0] == 'U' else -1
                return (-v,) if against else (v,)
            o += trades(data[p], kd, f, c, 1.5, 3.0, mh, (6, 22) if data is harness.D1 else None)
        row.append(st(o))
    for both in (False, True):
        o = []
        for p in smc_3y.LONG:
            c = cost_of(p) * pip_of(p)
            f = (lambda x: (1, -1)) if both else (lambda x, p=p: ((1 if harness.BT[(p, x['wk'])][0] == 'U' else -1),) if (p, x['wk']) in harness.BT else None)
            o += trades(harness.D4[p], kd, f, c, 1.5, 3.0, 30)
        row.append(st(o))
    print(f"{kd:12} | " + " | ".join(row))
# reference: random entries
import random
for data, lab, mh in [(harness.D1, '1H', 48), (harness.D4, '4H', 30)]:
    o = []
    for p in harness.ALL:
        c = cost_of(p) * pip_of(p); rnd = random.Random(7)
        b = data[p]
        for i in range(30, len(b), 6 if lab == '1H' else 3):
            x = b[i]
            if not any(q <= x['t'] < e for q, e in H): continue
            r = harness.B1.get((p, x['wk']))
            if not r or r[0] not in 'UD': continue
            if lab == '1H' and not (6 <= x['bh'] < 22): continue
            if rnd.random() > 0.35: continue
            d = 1 if r[0] == 'U' else -1; e = x['c']; rr = 1.5 * x['atr']; s = e - d * rr; t = e + d * 3 * rr; res = None
            for j in range(i + 1, min(len(b), i + 1 + mh)):
                y = b[j]
                if (y['l'] <= s) if d > 0 else (y['h'] >= s): res = -1; break
                if (y['h'] >= t) if d > 0 else (y['l'] <= t): res = 3; break
            else: j = min(len(b) - 1, i + mh); res = d * (b[j]['c'] - e) / rr
            o.append((x['t'], res - c / rr))
    print(f"RANDOM in bias direction {lab}: {st(o)}")
