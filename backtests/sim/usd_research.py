# Technical-framework search on 3 years of 4H data (6 USD pairs, trend direction instead of bias), exit fixed at the
# current default (half at 1R, rest BE, TP 3R, to Friday). Scored per year so that one lucky year cannot carry a variant.
import sys, os, itertools, datetime as D, collections, statistics as S, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from swing2 import *
U = lambda *a: D.datetime(*a, tzinfo=D.timezone.utc)
data = {p: load(p) for p in USD}; usd = usd_strength(data); B = {}
LONG = ['GBPUSD', 'AUDUSD', 'USDJPY', 'USDCHF', 'USDCAD', 'XAUUSD']
YRS = [(U(2024, 3, 1), U(2025, 1, 1)), (U(2025, 1, 1), U(2026, 1, 1)), (U(2026, 1, 1), U(2026, 11, 22))]
EXIT = dict(partial=True, tp=3, hold='fri')
FILT = {'none': {}, 'adx20': {'adx': 20}, 'adx25': {'adx': 25}, 'er.3': {'er': 0.3}, 'vol>30%': {'atrp': (0.3, 1.0)}, 'vol<70%': {'atrp': (0.0, 0.7)}}
rows = []
for ts, en, fk, cf in itertools.product(['sma20', 'sma50', 'sma100', 'ret20', 'ret60', 'dual'], ['A', 'D', 'DC'], FILT, ['wtd', 'none']):
    P = {**EXIT, **FILT[fk], 'dirm': 'trend', 'tsrc': ts, 'entry': en, 'cf': cf}
    yr = []; allt = []
    for a, b in YRS:
        t = sum([run(p, data[p], B, P, a, b, usd) for p in LONG], []); yr.append(sum(x['R'] for x in t)); allt += t
    eq = pk = m = 0
    for x in sorted(allt, key=lambda x: x['tx']): eq += x['R']; pk = max(pk, eq); m = min(m, eq - pk)
    n = len(allt); tot = sum(yr)
    rows.append(dict(ts=ts, entry=en, filt=fk, cf=cf, n=n, R=round(tot, 1), exp=round(tot / n, 3) if n else 0, y=[round(v, 1) for v in yr], minyr=round(min(yr), 1), dd=round(m, 1), perwk=round(tot / 142, 2)))
rows.sort(key=lambda r: (r['minyr'], r['R']), reverse=True)
json.dump(rows, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'usd_research.json'), 'w'), indent=0)
print('variants', len(rows), 'positive every year:', sum(r['minyr'] > 0 for r in rows))
for r in rows[:15]: print(r)
for k in ['ts', 'entry', 'filt', 'cf']:
    g = collections.defaultdict(list)
    for r in rows: g[r[k]].append(r['R'])
    print(k, {a: round(S.median(v), 1) for a, v in g.items()})
