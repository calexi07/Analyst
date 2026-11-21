import sys, os, datetime as D, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from swing2 import *
U = lambda *a: D.datetime(*a, tzinfo=D.timezone.utc)
data = {p: load(p) for p in USD}; usd = usd_strength(data); B = bias_table()
LONG = ['GBPUSD', 'AUDUSD', 'USDJPY', 'USDCHF', 'USDCAD', 'XAUUSD']
YRS = [(U(2024, 3, 1), U(2025, 1, 1)), (U(2025, 1, 1), U(2026, 1, 1)), (U(2026, 1, 1), U(2026, 11, 22))]
H = [(U(2026, 9, 27, 21), U(2026, 10, 25, 21)), (U(2026, 10, 25, 21), U(2026, 11, 22))]
def m(t):
    t = sorted(t, key=lambda x: x['tx']); eq = pk = d = 0
    for x in t: eq += x['R']; pk = max(pk, eq); d = min(d, eq - pk)
    return len(t), round(sum(x['R'] for x in t), 1), round(d, 1)
for en, cf, op in itertools.product(['SWP', 'SD', 'SWO', 'D', 'WO'], ['none'], ['none', 'wm']):
    P = dict(partial=True, tp=3, hold='fri', entry=en, cf=cf, opens=op)
    hb = [m(sum([run(p, data[p], B, {**P, 'dirm': 'bias'}, a, b, usd) for p in USD], [])) for a, b in H]
    y = [m(sum([run(p, data[p], B, {**P, 'dirm': 'trend'}, a, b, usd) for p in LONG], [])) for a, b in YRS]
    print(f"{en:4} opens={op:4} | bias {hb[0][0]+hb[1][0]:3}tr {hb[0][1]:+5.1f}/{hb[1][1]:+5.1f} = {hb[0][1]+hb[1][1]:+5.1f}R dd{min(hb[0][2],hb[1][2]):+5.1f} | 3y trend {sum(x[0] for x in y):4}tr {sum(x[1] for x in y):+6.1f}R {[x[1] for x in y]} dd{min(x[2] for x in y):+5.1f}")
