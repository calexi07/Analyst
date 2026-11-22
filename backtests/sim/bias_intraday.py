import harness, datetime as D, collections, itertools
from smc import B, H, USDP, EURP, cost_of, pip_of
from zoneinfo import ZoneInfo
BUC = ZoneInfo('Europe/Bucharest'); ALL = USDP + EURP
def sim(eh=10, k=1.0, tp=2.0, xh=21, conf=None, mingap=0, pairs=ALL, mom=None, anti=False):
    out = []
    for p in pairs:
        b = harness.D1[p]; cost = cost_of(p) * pip_of(p); days = collections.OrderedDict()
        for i, x in enumerate(b): days.setdefault(x['t'].astimezone(BUC).date(), []).append(i)
        for d0, ix in days.items():
            t0 = b[ix[0]]['t']
            if not any(s <= t0 < e for s, e in H) or d0.weekday() > 4: continue
            bb = harness.B1.get((p, b[ix[len(ix)//2]]['wk']))
            if not bb or bb[0] not in 'UD': continue
            if abs(bb[2]) < mingap: continue
            if conf and bb[1] not in conf: continue
            d = 1 if bb[0] == 'U' else -1
            if anti: d = -d
            q = next((i for i in ix if b[i]['t'].astimezone(BUC).hour == eh), None)
            if q is None or not b[q]['atr']: continue
            if mom:   # London move (open of mom h0 to entry) must be in the bias direction
                q0 = next((i for i in ix if b[i]['t'].astimezone(BUC).hour == mom), None)
                if q0 is None or (b[q-1]['c'] - b[q0]['o']) * d <= 0: continue
            e = b[q]['o']; r = k * b[q]['atr']; sl = e - d * r; tpp = e + d * tp * r if tp else None; R = None
            for i in ix[ix.index(q):]:
                x = b[i]; h = x['t'].astimezone(BUC).hour
                if (x['l'] <= sl) if d > 0 else (x['h'] >= sl): R = -1; break
                if tpp and ((x['h'] >= tpp) if d > 0 else (x['l'] <= tpp)): R = tp; break
                if h >= xh: R = d * (x['c'] - e) / r; break
            if R is None: R = d * (b[ix[-1]]['c'] - e) / r
            out.append((t0, p, R - cost / r))
    return out
def rep(o, lab):
    R = [x[2] for x in o]; h1 = sum(x[2] for x in o if x[0] < H[0][1]); n = len(R)
    print(f"{lab:52} {n:4d}tr {sum(R):+6.1f}R {sum(R)/max(1,n):+.3f}/tr halves {h1:+5.1f}/{sum(R)-h1:+5.1f}  per 2wk {sum(R)/4:+.1f}R")
rep(sim(), "bias · 10:00 · SL1ATR · TP2 · exit 21h")
rep(sim(anti=True), "AGAINST bias (control)")
for eh in [9, 10, 11, 15, 16]:
    for k, tp in [(1, 2), (1.5, 2), (1, 3), (1, None)]:
        rep(sim(eh=eh, k=k, tp=tp), f"bias · {eh}:00 · SL{k}ATR · TP{tp}")
for c in [('h',), ('h', 'm')]:
    rep(sim(conf=c), f"bias conv {c} · 10:00")
for g in [5, 7, 9]:
    rep(sim(mingap=g), f"bias |gap|>={g} · 10:00")
rep(sim(mom=9, eh=11), "bias + London 9-11 move with bias · 11:00")
rep(sim(mom=9, eh=12, k=1), "bias + London 9-12 move with bias · 12:00")

print()
from zoneinfo import ZoneInfo
for lab, o in [("A: 10:00 · SL1ATR · TP3", sim(eh=10, k=1, tp=3)), ("B: London 9-12 confirms · 12:00 · TP2", sim(mom=9, eh=12)),
               ("B3: London 9-12 confirms · 12:00 · TP3", sim(mom=9, eh=12, tp=3)), ("C: London 9-11 confirms · 11:00 · TP3", sim(mom=9, eh=11, tp=3))]:
    byd = collections.defaultdict(float); byw = collections.defaultdict(float); n_d = collections.Counter()
    for t, p, r in o: dd = t.astimezone(BUC).date(); byd[dd] += r; n_d[dd] += 1; byw[dd.isocalendar()[1]] += r
    eq = pk = mdd = 0
    for d in sorted(byd): eq += byd[d]; pk = max(pk, eq); mdd = min(mdd, eq - pk)
    print(f"{lab:42} total {sum(byd.values()):+.1f}R · weeks {' '.join(f'{v:+.0f}' for k, v in sorted(byw.items()))} · worst day {min(byd.values()):+.1f}R (max {max(n_d.values())} trades/day, avg {sum(n_d.values())/len(n_d):.1f}) · max DD {mdd:.1f}R")
