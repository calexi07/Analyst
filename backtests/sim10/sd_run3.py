# 2026 (Aug-Nov), weekly bias, LTF 5m or 15m, HTF 1H / 4H, EURUSD GBPUSD XAUUSD
import sys
sys.path.insert(0, '/home/claude/analyst/backtests/sim10')
import sd, sd_data
from smc import cost_of, pip_of
P = ['EURUSD', 'GBPUSD', 'XAUUSD']
def st(o):
    R = [x[1] for x in o]; n = len(R)
    if not n: return '   0tr'
    mid = o[0][0] + (o[-1][0] - o[0][0]) / 2; h1 = sum(x[1] for x in o if x[0] < mid)
    return f"{n:3d}tr {sum(R):+6.1f}R {sum(R)/n:+.2f}/tr ({h1:+.1f}/{sum(R)-h1:+.1f})"
for ltf in ['5', '15']:
    D = {p: sd_data.y2026(p, ltf) for p in P}
    for htf in ['4H', '1H']:
        ZZ = {p: sd.zones(D[p][1][htf]) for p in P}
        for lab, kw in [('limit proximal, SL distal, TP2', dict(conf='none', entry='limit', sl='htf', tp=2.0)),
                        ('limit proximal, SL distal, TP3', dict(conf='none', entry='limit', sl='htf', tp=3.0)),
                        ('CHoCH, SL LTF leg, TP2', dict(conf='choch', entry='mkt', sl='ltf', tp=2.0)),
                        ('CHoCH, SL LTF leg, TP3', dict(conf='choch', entry='mkt', sl='ltf', tp=3.0)),
                        ('CHoCH, SL LTF leg, TP5', dict(conf='choch', entry='mkt', sl='ltf', tp=5.0)),
                        ('CHoCH, SL distal, TP2', dict(conf='choch', entry='mkt', sl='htf', tp=2.0)),
                        ('CHoCH, SL distal, TP3', dict(conf='choch', entry='mkt', sl='htf', tp=3.0))]:
            arm = 96 if ltf == '5' else 32
            w = []; a = []
            for p in P:
                l, hh, biasf = D[p]
                c = cost_of(p) * pip_of(p)
                w += sd.run(l, hh[htf], ZZ[p], biasf, c, arm=arm, maxh=(288 if ltf == '5' else 96) * 3, **kw)
                a += sd.run(l, hh[htf], ZZ[p], lambda x, f=biasf: tuple(-v for v in f(x)), c, arm=arm, maxh=(288 if ltf == '5' else 96) * 3, **kw)
            w.sort(key=lambda x: x[0]); a.sort(key=lambda x: x[0])
            print(f"LTF {ltf:>2}m HTF {htf} · {lab:32} with bias {st(w):36} | against {st(a)}", flush=True)
