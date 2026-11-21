# Full search: entries (incl. S/R, supply/demand OB, FVG, opens, sweeps) x confirmation x "price above opens" filter x Friday rule,
# exit = half at 1R, rest BE, TP 3R. Bias weeks W40-W47 (8 USD pairs) for bias and bias+trend; 3 years with trend direction (6 pairs).
import sys, os, itertools, datetime as D, collections, statistics as S, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from swing2 import *
U = lambda *a: D.datetime(*a, tzinfo=D.timezone.utc)
data = {p: load(p) for p in USD}; usd = usd_strength(data); B = bias_table()
LONG = ['GBPUSD', 'AUDUSD', 'USDJPY', 'USDCHF', 'USDCAD', 'XAUUSD']
YRS = [(U(2024, 3, 1), U(2025, 1, 1)), (U(2025, 1, 1), U(2026, 1, 1)), (U(2026, 1, 1), U(2026, 11, 22))]
H = [(U(2026, 9, 27, 21), U(2026, 10, 25, 21)), (U(2026, 10, 25, 21), U(2026, 11, 22))]
ENT = ['A', 'D', 'WO', 'DO', 'YO', 'SR', 'SRS', 'SWP', 'OB', 'FVG', 'OBFVG']
FRI = {'Friday close': dict(fri=True, hold='fri'), 'no Friday close, max 5 days': dict(fri=False, hold=5), 'no Friday close, no time limit': dict(fri=False, hold=1000)}
def m(t):
    t = sorted(t, key=lambda x: x['tx']); eq = pk = d = 0
    for x in t: eq += x['R']; pk = max(pk, eq); d = min(d, eq - pk)
    return len(t), round(sum(x['R'] for x in t), 1), round(d, 1)
rows = []
for en, cf, op, fk in itertools.product(ENT, ['none', 'wtd'], ['none', 'w', 'wm', 'wmy'], FRI):
    P = dict(partial=True, tp=3, entry=en, cf=cf, opens=op, **FRI[fk])
    r = dict(entry=en, cf=cf, opens=op, fri=fk)
    for dm in ['bias', 'both']:
        h = [m(sum([run(p, data[p], B, {**P, 'dirm': dm}, a, b, usd) for p in USD], [])) for a, b in H]
        r[dm] = dict(n=h[0][0] + h[1][0], h1=h[0][1], h2=h[1][1], R=round(h[0][1] + h[1][1], 1), dd=min(h[0][2], h[1][2]))
    y = [m(sum([run(p, data[p], B, {**P, 'dirm': 'trend'}, a, b, usd) for p in LONG], [])) for a, b in YRS]
    r['trend'] = dict(n=sum(x[0] for x in y), y=[x[1] for x in y], R=round(sum(x[1] for x in y), 1), dd=min(x[2] for x in y))
    rows.append(r)
json.dump(rows, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'usd_full.json'), 'w'))
print(len(rows), 'variants')
