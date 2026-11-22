# Full Supertrend grid on BE Swing (entry C, 1H path, hours 06-22): trailing, entry filter, stop placement, TP.
# Ranked on the 8 USD pairs (W40-43 / W44-47 halves); the best are re-checked on the 6 EUR crosses (|gap| >= 5) as a hold-out.
import sys, os, itertools, collections, multiprocessing as MP
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mtf_c import *
USD = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'USDCAD', 'AUDUSD', 'NZDUSD', 'XAUUSD']
EUR = ['EURGBP', 'EURJPY', 'EURCHF', 'EURAUD', 'EURNZD', 'EURCAD']
B = bias_table(); D4 = {p: prep4(p) for p in USD + EUR}; D1 = {p: load1h(p) for p in USD + EUR}
def ev(P, pairs=USD):
    hs = [sum([run_c(p, D4[p], D1[p], B, {'hours': (6, 22), **P}, a, c) for p in pairs], []) for a, c in H]
    t = sorted(hs[0] + hs[1], key=lambda x: x['tx']); eq = pk = dd = 0
    for x in t: eq += x['R']; pk = max(pk, eq); dd = min(dd, eq - pk)
    return dict(n=len(t), h1=sum(x['R'] for x in hs[0]), h2=sum(x['R'] for x in hs[1]), dd=dd, win=sum(x['R'] > 0 for x in t) / max(1, len(t)),
                tp=sum(x['why'] == 'TP' for x in t))
def fmt(r): return f"{r['n']:3}tr win {r['win']:.0%} TP {r['tp']:2} {r['h1']:+5.1f}/{r['h2']:+5.1f} = {r['h1'] + r['h2']:+5.1f}R dd {r['dd']:+5.1f}"
def job(P): return P, ev(P)
if __name__ == '__main__':
    G = []
    for tf, per, m, tp in itertools.product(['4h', '1h'], [7, 10, 14], [1.0, 1.5, 2.0, 3.0], [4, 0]):
        for trm, stat in [('st', 0), ('st_after', 1), ('st_after', 2), ('tighter', 0)]:
            G.append(dict(grp='trail', trm=trm, stat=stat, sttf=tf, stp=per, stm=m, tp=tp))
    for per, m in itertools.product([7, 10, 14], [1.5, 2.0, 3.0]):
        G.append(dict(grp='filter', stf=True, stp=per, stm=m))
        for slm in ['st', 'wider', 'tighter']:
            G.append(dict(grp='stop', slm=slm, stp=per, stm=m))
    for k in [0.75, 1.25, 1.5]:
        for tp in [3, 4, 5]: G.append(dict(grp='stop', slk=k, tp=tp))
    for tp in [3, 5, 6, 0]: G.append(dict(grp='tp', tp=tp))
    base = ev({}); print('BASE (your settings)                     ', fmt(base))
    with MP.Pool(4) as pool: R = pool.map(job, [{k: v for k, v in P.items() if k != 'grp'} | {'_g': P['grp']} for P in G])
    R = [({k: v for k, v in P.items() if k != '_g'}, r, P['_g']) for P, r in R]
    for g in ['trail', 'filter', 'stop', 'tp']:
        rows = sorted([x for x in R if x[2] == g], key=lambda x: -(x[1]['h1'] + x[1]['h2']))
        better = [x for x in rows if x[1]['h1'] > base['h1'] and x[1]['h2'] > base['h2']]
        print(f"\n== {g}: {len(rows)} variants, {sum(x[1]['h1'] + x[1]['h2'] > base['h1'] + base['h2'] for x in rows)} beat the total, {len(better)} beat both halves")
        for P, r, _ in rows[:6]: print(f"  {str(P):<78} {fmt(r)}")
    top = sorted(R, key=lambda x: -min(x[1]['h1'] - base['h1'], x[1]['h2'] - base['h2']))[:8]
    eb = ev({'mingap': 5}, EUR); print('\n== hold-out EUR crosses |gap|>=5. BASE:', fmt(eb))
    for P, r, _ in top: print(f"  {str(P):<78} USD {r['h1'] + r['h2']:+5.1f}R | EUR {fmt(ev({**P, 'mingap': 5}, EUR))}")
