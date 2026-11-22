# BE Swing (4H entry C, 1H path, bias+SMA20, Mon-Wed, 06-22): how wide should the trailing be?
import sys, os, itertools, collections, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mtf_c import *
PAIRS = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'USDCAD', 'AUDUSD', 'NZDUSD']
B = bias_table(); D4 = {p: prep4(p) for p in PAIRS}; D1 = {p: load1h(p) for p in PAIRS}
def ev(P):
    hs = [sum([run_c(p, D4[p], D1[p], B, {'hours': (6, 22), **P}, a, c) for p in PAIRS], []) for a, c in H]
    t = sorted(hs[0] + hs[1], key=lambda x: x['tx']); eq = pk = dd = 0; pp = collections.defaultdict(float); why = collections.Counter()
    for x in t: eq += x['R']; pk = max(pk, eq); dd = min(dd, eq - pk); pp[x['pair']] += x['R']; why[x['why']] += 1
    return dict(n=len(t), h1=sum(x['R'] for x in hs[0]), h2=sum(x['R'] for x in hs[1]), dd=dd, win=sum(x['R'] > 0 for x in t), neg=sum(v < 0 for v in pp.values()), why=dict(why))
R = []
for tp, k, t2, at in itertools.product([4, 6, 0], [0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0], ['none', 'half', 'fixed0.5'], [1.0, 2.0, 3.0]):
    if t2 == 'none' and at != 2.0: continue
    k2 = None if t2 == 'none' else (k / 2 if t2 == 'half' else 0.5)
    if k2 is not None and k2 >= k: continue
    P = dict(tp=tp, trk=k, trk2=k2, trat=at); R.append((P, ev(P)))
json.dump(R, open('/tmp/swtrail.json', 'w'))
cur = [r for P, r in R if P == dict(tp=4, trk=0.75, trk2=0.5, trat=2.0)][0]
f = lambda P, r: f"TP{P['tp'] or '-'} trail {P['trk']} → {P['trk2']} after {P['trat']}R | {r['n']}tr w{r['win']/r['n']:.0%} {(r['h1']+r['h2'])/r['n']:+.2f}R/tr {r['h1']:+.1f}/{r['h2']:+.1f}={r['h1']+r['h2']:+.1f} dd {r['dd']:.1f} neg {r['neg']} {r['why']}"
print('CURRENT', f(dict(tp=4, trk=0.75, trk2=0.5, trat=2.0), cur))
print('--- without tightening, by width (TP4):')
for P, r in R:
    if P['tp'] == 4 and P['trk2'] is None: print(' ', f(P, r))
print('--- top 15 by total, both halves positive:')
for P, r in sorted([x for x in R if x[1]['h1'] > 0 and x[1]['h2'] > 0], key=lambda x: -(x[1]['h1'] + x[1]['h2']))[:15]: print(' ', f(P, r))
