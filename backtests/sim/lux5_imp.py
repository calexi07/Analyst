import intraday as T, lux5
P = ['EURUSD', 'GBPUSD', 'XAUUSD']; DATA = {p: T.prep(p) for p in P}
def go(lab, **k):
    k = {**dict(s=5, mode='choch_ob', dirm='bias', tp=5.0, extra=1.0), **k}; tot = []; per = []
    for p in P:
        o = lux5.run(p, DATA[p], **k); tot += o; per.append(f"{p[:3]} {sum(r for _, r in o):+.1f}/{len(o)}")
    tot.sort(); R = [r for _, r in tot]; n = len(R)
    if not n: print(f"{lab:46} none"); return
    mid = tot[0][0] + (tot[-1][0] - tot[0][0]) / 2; h1 = sum(r for t, r in tot if t < mid)
    print(f"{lab:46} {n:3d}tr {sum(R):+6.1f}R {sum(R)/n:+.2f}/tr ({h1:+.1f}/{sum(R)-h1:+.1f}) | " + " · ".join(per))
print("all with +1 pip extra cost, bias, TP 5R unless said")
go("BASE (s5, OB edge, minSL 0.5 ATR, 1/day)")
for tp in [2.0, 3.0, 4.0, 6.0]: go(f"TP {tp}", tp=tp)
for m in [1.0, 1.5, 2.0]: go(f"min SL {m} ATR(5m)", minr=m)
go("entry at OB middle", entry='mid')
for e in [50, 200, 600]: go(f"EMA{e} (5m) on trade side", ema=e)
for s in [3, 10]: go(f"structure length {s}", s=s)
for w in [(480, 1200), (600, 960), (540, 840), (840, 1080)]: go(f"window {w[0]//60}-{w[1]//60}", w=w)
go("2 trades a day", maxday=2)
go("OB valid 12 bars", ob_valid=12); go("OB valid 48 bars", ob_valid=48)
go("max hold 96 bars (8h)", tmax=96)
go("conviction medium/high", conv=('h', 'm'))
go("BOS → OB too (not only CHoCH)", mode='bos_ob')
go("min SL 1 ATR + EMA200", minr=1.0, ema=200)
print('--- hold neighbourhood')
for tm in [72, 96, 120, 999]:
    go(f"max hold {tm} bars", tmax=tm)
    go(f"max hold {tm} bars + TP 3", tmax=tm, tp=3.0)
