# CET as a stand-alone swing strategy on 4H/1H: contraction → first close beyond → SL other side, TP R, max hold N bars (no daily close)
import sys; sys.path.insert(0, '/home/claude/analyst/backtests/sim')
import harness, smc_3y
from smc import H, cost_of, pip_of
def cet_swing(b, dirf, cost, tp, maxh, retest=False):
    out = []; zone = None; pos = None; pend = None
    for i in range(2, len(b)):
        x = b[i]
        if pos:
            e, s, t, d, r, j = pos
            if (x['l'] <= s) if d > 0 else (x['h'] >= s): out.append((x['t'], d * (s - e) / r - cost / r)); pos = None
            elif (x['h'] >= t) if d > 0 else (x['l'] <= t): out.append((x['t'], d * (t - e) / r - cost / r)); pos = None
            elif i - j >= maxh: out.append((x['t'], d * (x['c'] - e) / r - cost / r)); pos = None
            continue
        if pend:   # retest entry: limit at the broken edge
            lv, s, d, k = pend
            if i - k > 6: pend = None
            elif (x['l'] <= lv) if d > 0 else (x['h'] >= lv):
                r = abs(lv - s); pos = (lv, s, lv + d * tp * r, d, r, i); pend = None; continue
        a, m, c = b[i-2], b[i-1], x
        bt = lambda y: (max(y['o'], y['c']), min(y['o'], y['c']))
        (at, ab), (mt, mb), (ct, cb) = bt(a), bt(m), bt(c)
        if (mt - mb) > (ct - cb) and (mt - mb) > (at - ab) and at <= mt and ab >= mb and ct <= mt and cb >= mb:
            zone = [max(a['h'], m['h'], c['h']), min(a['l'], m['l'], c['l'])]; continue
        if zone:
            d = 1 if x['c'] > zone[0] else -1 if x['c'] < zone[1] else 0
            if d:
                D_ = dirf(x); z = zone; zone = None
                if D_ and d in D_:
                    s = z[1] if d > 0 else z[0]
                    if retest: pend = (z[0] if d > 0 else z[1], s, d, i)
                    else:
                        e = x['c']; r = abs(e - s)
                        if r > 0: pos = (e, s, e + d * tp * r, d, r, i)
    return out
def st(o, lab):
    R = [r for _, r in o]; n = len(R)
    print(f"{lab:58} {n:4d}tr {sum(R):+6.1f}R {sum(R)/max(1,n):+.2f}/tr win {sum(r>0 for r in R)/max(1,n):.0%}")
for tf, data, maxh in [('4H', harness.D4, 30), ('1H', harness.D1, 72)]:
    for tp in [2, 3]:
        for rt in [False, True]:
            w = []; a = []
            for p in harness.ALL:
                c = cost_of(p) * pip_of(p)
                def f(x, p=p, s=1):
                    if not any(q <= x['t'] < e for q, e in H): return ()
                    r = harness.B1.get((p, x['wk'])); return ((1 if r[0] == 'U' else -1) * s,) if r and r[0] in 'UD' else ()
                w += cet_swing(data[p], f, c, tp, maxh, rt); a += cet_swing(data[p], lambda x, p=p, f=f: tuple(-v for v in f(x)), c, tp, maxh, rt)
            st(w, f"{tf} bias W40-47 14 pairs TP{tp} {'retest' if rt else 'break close'}"); st(a, f"   … against bias")
# 3 years 4H, 6 pairs, direction = daily SMA20 trend (no bias history)
for tp in [2, 3]:
    for rt in [False, True]:
        o = []; o2 = []
        for p in smc_3y.LONG:
            c = cost_of(p) * pip_of(p)
            f = lambda x, p=p: ((1 if harness.BT[(p, x['wk'])][0] == 'U' else -1),) if (p, x['wk']) in harness.BT else ()
            o += cet_swing(harness.D4[p], f, c, tp, 30, rt); o2 += cet_swing(harness.D4[p], lambda x: (1, -1), c, tp, 30, rt)
        st(o, f"4H 3y 6 pairs trend TP{tp} {'retest' if rt else 'break close'}"); st(o2, f"   … both directions")
