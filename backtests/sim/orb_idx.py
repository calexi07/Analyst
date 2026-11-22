# Opening-range breakout grid for an instrument without fundamental bias (e.g. GER40): OCO both sides, long only,
# short only, and in the daily SMA20 trend direction. All data, halves split in the middle.
import sys, datetime as D, itertools, json, collections
import intraday as T
p = sys.argv[1]; data = T.prep(p); b5 = data[0]
a, c = b5[0]['t'], b5[-1]['t'] + D.timedelta(minutes=5); mid = a + (c - a) / 2
print(p, b5[0]['t'].date(), '->', b5[-1]['t'].date(), '| halves split', mid.date())
R = {'pre 09:00-10:00': (540, 600, 780), 'open 10:00-10:15': (600, 615, 780), 'open 10:00-10:30': (600, 630, 780),
     'open 10:00-11:00': (600, 660, 840), 'US 16:30-16:45': (990, 1005, 1140), 'US 16:30-17:00': (990, 1020, 1140)}
def oco(P):
    L = T.run(p, data, {**P, 'dirm': 'long'}, a, c); S = T.run(p, data, {**P, 'dirm': 'short'}, a, c); by = {}
    for x in L + S:
        if x['cd'] not in by or x['t'] < by[x['cd']]['t']: by[x['cd']] = x
    return list(by.values())
out = []
for (rn, (r0, r1, un)), tp, tm, sl, dm in itertools.product(R.items(), [1.0, 1.5, 2.0, 3.0], [36, 48], ['range', 'mid'], ['oco', 'long', 'short', 'trend']):
    P = dict(idea='orb', r0=r0, r1=r1, until=un, tp=tp, tmax=tm, sl=sl)
    t = oco(P) if dm == 'oco' else T.run(p, data, {**P, 'dirm': dm}, a, c)
    eq = pk = dd = 0
    for x in sorted(t, key=lambda z: z['t']): eq += x['R']; pk = max(pk, eq); dd = min(dd, eq - pk)
    out.append(dict(rng=rn, tp=tp, tmax=tm, sl=sl, dir=dm, n=len(t), h1=sum(x['R'] for x in t if x['t'] < mid), h2=sum(x['R'] for x in t if x['t'] >= mid), dd=dd, win=sum(x['R'] > 0 for x in t)))
json.dump(out, open(f'/tmp/orb_{p}.json', 'w'))
g = collections.defaultdict(list)
for r in out: g[(r['rng'], r['dir'])].append(r)
print(f"{'range':<18}{'direction':<7} variants +both halves | median R/tr | best (by weaker half)")
for (rn, dm), rows in g.items():
    good = sum(r['h1'] > 0 and r['h2'] > 0 for r in rows); med = sorted((r['h1'] + r['h2']) / max(1, r['n']) for r in rows)[len(rows) // 2]
    b = max(rows, key=lambda r: min(r['h1'], r['h2'])); t = b['h1'] + b['h2']
    print(f"{rn:<18}{dm:<7} {good:2}/{len(rows)}  {med:+.2f} | TP{b['tp']} {b['tmax']*5//60}h sl {b['sl']}: {b['n']}tr win {b['win']/max(1,b['n']):.0%} {t/max(1,b['n']):+.2f}R/tr {b['h1']:+.1f}/{b['h2']:+.1f} dd {b['dd']:.1f}")
