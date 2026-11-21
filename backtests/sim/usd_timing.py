# Entry timing and variable-length exits for BE Swing on the USD pairs (default = both agree + WTD + half at 1R, TP 3R, to Friday).
import sys, os, datetime as D, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'usd_ideas.py')).read().split('IDEAS = [')[0])
BASE = dict(dirm='both', partial=True, tp=3, hold='fri')
fmt = lambda s: f"{s['n']:3}tr {s['R']:+6.1f}R ({s['exp']:+.2f})"
def dd(P):
    tr = sorted(sum([run(p, data[p], B, P, H1[0], H2[1], usd) for p in USD], []), key=lambda x: x['tx']); eq = pk = m = 0
    for x in tr: eq += x['R']; pk = max(pk, eq); m = min(m, eq - pk)
    return tr, round(m, 1)
tr, m = dd(BASE)
print('Default: entries by trading day', collections.Counter(x['t'].astimezone(NY).strftime('%a') for x in tr))
print('Default: hold time (days)', sorted(round((x['tx'] - x['t']).total_seconds() / 86400, 1) for x in tr))
V = [('Default', {}), ('No Monday entries', {'nomon': True}), ('Confirmation needs WTD ≥ 0.25 ATR', {'minwtd': 0.25}), ('Confirmation needs WTD ≥ 0.5 ATR', {'minwtd': 0.5}), ('Entry: break of yesterday high/low', {'entry': 'D'}), ('Break of yesterday + WTD ≥ 0.25 ATR', {'entry': 'D', 'minwtd': 0.25}),
     ('Entry: pullback then resumption candle', {'entry': 'P'}), ('Entry: limit at 4H EMA20', {'entry': 'E'}),
     ('Rest: exit on 4H close across EMA20', {'restx': 'ema20'}), ('Rest: exit on close beyond yesterday low/high', {'restx': 'prevday'}),
     ('Rest: trail 2×ATR', {'restx': 'trail', 'trail': 2.0}), ('Rest: trail 1×ATR', {'restx': 'trail', 'trail': 1.0}), ('Rest: no TP + trail 1.5×ATR', {'restx': 'trail', 'trail': 1.5, 'tp': 0})]
print(f"\n{'variant':<46}| bias W40-43 | bias W44-47 | maxDD | avg hold | trend 2024 | 2025 | 2026")
for n, P in V:
    Q = {**BASE, **P}; b = bias_run(Q); tr, m = dd(Q); t = trend_run({k: v for k, v in Q.items() if k != 'dirm'})
    h = sum((x['tx'] - x['t']).total_seconds() for x in tr) / max(len(tr), 1) / 86400
    print(f"{n:<46}| {fmt(b[0])} | {fmt(b[1])} | {m:+.1f} | {h:.1f}d | " + ' | '.join(fmt(x) for x in t))
