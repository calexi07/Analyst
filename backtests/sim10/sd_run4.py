# 14 pairs, weekly bias W40-W47: 4H zones (harness 4H) with 1H CHoCH / limit; also daily-like zones: 4H zones + 15m? (no 15m for 14 pairs)
import sys, datetime as D
sys.path.insert(0, '/home/claude/analyst/backtests/sim10'); sys.path.append('/home/claude/analyst/backtests/sim')
import sd, harness
from smc import H, cost_of, pip_of
def st(o):
    R = [x[1] for x in o]; n = len(R)
    if not n: return '   0tr'
    h1 = sum(x[1] for x in o if x[0] < H[0][1])
    return f"{n:3d}tr {sum(R):+6.1f}R {sum(R)/n:+.2f}/tr ({h1:+.1f}/{sum(R)-h1:+.1f})"
HT = {}
for p in harness.ALL:
    h = [dict(t=x['t'], tc=x['t'] + D.timedelta(hours=4), o=x['o'], h=x['h'], l=x['l'], c=x['c']) for x in harness.D4[p]]
    sd.atr_(h); HT[p] = (h, sd.zones(h))
for lab, kw in [('limit proximal, SL distal, TP2', dict(conf='none', entry='limit', sl='htf', tp=2.0)),
                ('limit proximal, SL distal, TP3', dict(conf='none', entry='limit', sl='htf', tp=3.0)),
                ('1H CHoCH, SL 1H leg, TP3', dict(conf='choch', entry='mkt', sl='ltf', tp=3.0)),
                ('1H CHoCH, SL distal, TP2', dict(conf='choch', entry='mkt', sl='htf', tp=2.0)),
                ('1H CHoCH, SL distal, TP3', dict(conf='choch', entry='mkt', sl='htf', tp=3.0))]:
    w = []; a = []
    for p in harness.ALL:
        l = [dict(t=x['t'], o=x['o'], h=x['h'], l=x['l'], c=x['c'], atr=x['atr'], wk=x['wk']) for x in harness.D1[p]]
        def f(x, p=p, s=1):
            if not any(q <= x['t'] < e for q, e in H): return ()
            r = harness.B1.get((p, x['wk'])); return ((1 if r[0] == 'U' else -1) * s,) if r and r[0] in 'UD' else ()
        h, Z = HT[p]; c = cost_of(p) * pip_of(p)
        w += sd.run(l, h, Z, f, c, arm=24, maxh=120, **kw); a += sd.run(l, h, Z, lambda x, f=f: tuple(-v for v in f(x)), c, arm=24, maxh=120, **kw)
    w.sort(key=lambda x: x[0]); a.sort(key=lambda x: x[0])
    print(f"4H zones → {lab:32} with bias {st(w):34} | against {st(a)}", flush=True)
import smc_3y, collections
print('--- 3 years, 6 pairs, 4H zones, limit at proximal (4H path), direction = daily SMA20 trend (BT)')
for tp in [2.0, 3.0]:
    o = []
    for p in smc_3y.LONG:
        h, Z = HT[p]
        l = [dict(t=x['tc'] - D.timedelta(hours=4), o=x['o'], h=x['h'], l=x['l'], c=x['c'], atr=x['atr'], wk=b['wk']) for x, b in zip(h, harness.D4[p])]
        f = lambda x, p=p: ((1 if harness.BT[(p, x['wk'])][0] == 'U' else -1),) if (p, x['wk']) in harness.BT else ()
        o += sd.run(l, h, Z, f, cost_of(p) * pip_of(p), conf='none', entry='limit', sl='htf', tp=tp, maxh=60)
    y = collections.defaultdict(float)
    for t, r, z in o: y[t.year] += r
    R = [x[1] for x in o]; print(f"   TP{tp:.0f}: {len(R)}tr {sum(R):+.1f}R {sum(R)/len(R):+.2f}/tr per year {dict((k, round(v, 1)) for k, v in sorted(y.items()))}")
