# EMA 144/169 on 4H (the user's MA ribbon) as filter or entry zone.
import sys, os, datetime as D
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from swing2 import *
U = lambda *a: D.datetime(*a, tzinfo=D.timezone.utc)
data = {p: load(p) for p in USD}; usd = usd_strength(data); B = bias_table()
LONG = ['GBPUSD', 'AUDUSD', 'USDJPY', 'USDCHF', 'USDCAD', 'XAUUSD']
YRS = [(U(2024, 3, 1), U(2025, 1, 1)), (U(2025, 1, 1), U(2026, 1, 1)), (U(2026, 1, 1), U(2026, 11, 22))]
H = [(U(2026, 9, 27, 21), U(2026, 10, 25, 21)), (U(2026, 10, 25, 21), U(2026, 11, 22))]
EX = dict(partial=True, tp=3, hold='fri', cf='none')
def m(t):
    t = sorted(t, key=lambda x: x['tx']); eq = pk = d = 0
    for x in t: eq += x['R']; pk = max(pk, eq); d = min(d, eq - pk)
    return len(t), round(sum(x['R'] for x in t), 1), round(d, 1)
print('note: EURUSD/NZDUSD exports start in Aug, so the tunnel (300 4H bars) is not ready for them before Oct; bias test uses 6 pairs with long history + both where ready')
for en in ['SWP', 'D', 'A']:
    for vg in ['none', 'side', 'slope', 'both', 'near']:
        P = {**EX, 'entry': en, 'vegas': vg}
        hb = [m(sum([run(p, data[p], B, {**P, 'dirm': 'bias'}, a, b, usd) for p in USD], [])) for a, b in H]
        y = [m(sum([run(p, data[p], B, {**P, 'dirm': 'trend'}, a, b, usd) for p in LONG], [])) for a, b in YRS]
        print(f"{en:4} tunnel={vg:5} | bias {hb[0][0]+hb[1][0]:3}tr {hb[0][1]:+5.1f}/{hb[1][1]:+5.1f} = {hb[0][1]+hb[1][1]:+5.1f}R dd{min(hb[0][2],hb[1][2]):+5.1f} | 3y trend {sum(x[0] for x in y):4}tr {sum(x[1] for x in y):+6.1f}R {[x[1] for x in y]} dd{min(x[2] for x in y):+5.1f}")
P = {**EX, 'entry': 'VT'}
hb = [m(sum([run(p, data[p], B, {**P, 'dirm': 'bias'}, a, b, usd) for p in USD], [])) for a, b in H]
y = [m(sum([run(p, data[p], B, {**P, 'dirm': 'trend'}, a, b, usd) for p in LONG], [])) for a, b in YRS]
print(f"VT   limit at tunnel   | bias {hb[0][0]+hb[1][0]:3}tr {hb[0][1]:+5.1f}/{hb[1][1]:+5.1f} = {hb[0][1]+hb[1][1]:+5.1f}R | 3y trend {sum(x[0] for x in y):4}tr {sum(x[1] for x in y):+6.1f}R {[x[1] for x in y]} dd{min(x[2] for x in y):+5.1f}")
