# CET v1 (candle colouring): after a contraction, trade the first E (expansion) candle or the first T (trend) candle,
# in the side it left the zone; SL = other side of the zone H-L; TP in R; max hold. Tested with bias (2026) and on 10y 15m.
import sys; sys.path.insert(0, '/home/claude/analyst/backtests/sim'); sys.path.insert(0, '/home/claude/analyst/backtests/sim10')
def sig_stream(b):
    """yield (i, kind, dir, zone) for E / T candles after the latest contraction (first of each kind per zone)"""
    z = None
    for i in range(2, len(b)):
        a, m, c = b[i-2], b[i-1], b[i]
        bt = lambda y: (max(y['o'], y['c']), min(y['o'], y['c']))
        (at, ab), (mt, mb), (ct, cb) = bt(a), bt(m), bt(c)
        if (mt - mb) > (ct - cb) and (mt - mb) > (at - ab) and at <= mt and ab >= mb and ct <= mt and cb >= mb:
            z = dict(h=max(a['h'], m['h'], c['h']), l=min(a['l'], m['l'], c['l']), bt=mt, bb=mb, E=False, T=False); continue
        if not z: continue
        x = c; xt, xb = bt(x)
        opens_in = z['bb'] <= x['o'] <= z['bt']; breaks = x['h'] > z['h'] or x['l'] < z['l']
        within = x['h'] <= z['h'] and x['l'] >= z['l']
        if within and xt <= z['bt'] and xb >= z['bb']: continue           # C
        if within and opens_in: continue                                  # B
        if opens_in and breaks and not z['E']:                            # E: direction = side of the close vs the master body
            z['E'] = True; d = 1 if x['c'] > z['bt'] else -1 if x['c'] < z['bb'] else 0
            if d: yield i, 'E', d, z
        elif (xb > z['bt'] or xt < z['bb']) and not z['T'] and not opens_in:   # T: whole body outside the master body
            z['T'] = True; yield i, 'T', (1 if xb > z['bt'] else -1), z
def trade(b, kind, dirf, cost, tp, maxh):
    out = []; busy = -1
    for i, k, d, z in sig_stream(b):
        if k != kind or i <= busy: continue
        D_ = dirf(b[i])
        if not D_ or d not in D_: continue
        e = b[i]['c']; s = z['l'] if d > 0 else z['h']; r = abs(e - s)
        if r <= 0 or (s - e) * d >= 0: continue
        t = e + d * tp * r; res = None
        for j in range(i + 1, min(len(b), i + 1 + maxh)):
            x = b[j]
            if (x['l'] <= s) if d > 0 else (x['h'] >= s): res = -1; break
            if (x['h'] >= t) if d > 0 else (x['l'] <= t): res = tp; break
        else: j = min(len(b) - 1, i + maxh); res = d * (b[j]['c'] - e) / r
        out.append((b[i]['t'], res - cost / r)); busy = j
    return out
def st(o, lab):
    R = [r for _, r in o]; n = len(R)
    print(f"{lab:60} {n:5d}tr {sum(R):+7.1f}R {sum(R)/max(1,n):+.2f}/tr win {sum(r>0 for r in R)/max(1,n):.0%}")
import harness, smc_3y
from smc import H, cost_of, pip_of
for kind in ['E', 'T']:
    for tf, data, mh in [('4H', harness.D4, 30), ('1H', harness.D1, 48)]:
        for tp in [2, 3]:
            w = []; a = []
            for p in harness.ALL:
                c = cost_of(p) * pip_of(p)
                def f(x, p=p, s=1):
                    if not any(q <= x['t'] < e for q, e in H): return ()
                    r = harness.B1.get((p, x['wk'])); return ((1 if r[0] == 'U' else -1) * s,) if r and r[0] in 'UD' else ()
                w += trade(data[p], kind, f, c, tp, mh); a += trade(data[p], kind, lambda x, f=f: tuple(-v for v in f(x)), c, tp, mh)
            st(w, f"{kind} candle · {tf} · bias W40-47 · 14 pairs · TP{tp}"); st(a, "     … against bias")
    o = []
    for p in smc_3y.LONG:
        c = cost_of(p) * pip_of(p)
        f = lambda x, p=p: ((1 if harness.BT[(p, x['wk'])][0] == 'U' else -1),) if (p, x['wk']) in harness.BT else ()
        o += trade(harness.D4[p], kind, f, c, 2, 30)
    st(o, f"{kind} candle · 4H · 3 years · 6 pairs · trend · TP2")
from core import load, COST
for kind in ['E', 'T']:
    for p in ['EURUSD', 'GBPUSD', 'XAUUSD']:
        bars, ks, info = load(p)
        st(trade(bars, kind, lambda x: (1, -1), COST[p], 2, 32), f"{kind} candle · 15m · 10 years · {p} · both · TP2 (max 8h)")
