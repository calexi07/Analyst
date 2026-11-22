# EURUSD Quasimodo grid on 5m / 15m / 30m, bias weeks only. Ranked by the worse half (both halves must hold up).
import sys, os, itertools, multiprocessing as MP
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qm, ltf
from smc import prep, B, H
from harness import B1
B.clear(); B.update(B1)
import harness as _hh; h1 = _hh.D1['EURUSD']   # real 1H (prep() is patched to 4H once smc_3y is imported)
DATA = {'5m': ltf.load('EURUSD', '5'), '15m': ltf.load('EURUSD', '15'), '30m': ltf.load('EURUSD', '30')}
CTX = {k: ltf.struct_ctx(h1, v) for k, v in DATA.items()}
def ev(args):
    tf, P = args; Q = dict(P); Q['ctx'] = CTX[tf] if P.get('ctx') else None
    hs = [qm.run('EURUSD', DATA[tf], Q, a, c) for a, c in H]
    t = sorted(hs[0] + hs[1], key=lambda x: x['tx']); eq = pk = dd = 0
    for x in t: eq += x['R']; pk = max(pk, eq); dd = min(dd, eq - pk)
    return tf, P, dict(n=len(t), h1=sum(x['R'] for x in hs[0]), h2=sum(x['R'] for x in hs[1]), dd=dd, win=sum(x['R'] > 0 for x in t) / max(1, len(t)))
if __name__ == '__main__':
    G = []
    for tf in DATA:
        for L, ent, tp, slb, ctx, hrs, canc in itertools.product([2, 3, 4, 5, 6], ['shoulder', 'half', 'break'], [2, 3, 4], [0.1, 0.5],
                                                           [False, True], [None, (6, 22)], [False]):
            G.append((tf, dict(L=L, entry=ent, tpR=tp, slb=slb, ctx=ctx, hours=hrs, cancel1R=canc, maxR=6)))
    with MP.Pool(2) as pool: R = pool.map(ev, G, chunksize=20)
    for tf in DATA:
        rows = [(P, r) for t_, P, r in R if t_ == tf and r['n'] >= 10]
        rows.sort(key=lambda x: -min(x[1]['h1'], x[1]['h2']))
        both = sum(1 for _, r in rows if r['h1'] > 0 and r['h2'] > 0)
        print(f"== {tf}: {len(rows)} variants with >=10 trades, {both} positive in both halves")
        for P, r in rows[:8]:
            tag = f"L{P['L']} {P['entry']:<8} TP{P['tpR']} SL+{P['slb']}ATR {'1H' if P['ctx'] else '  '} {'06-22' if P['hours'] else 'all  '}"
            print(f"  {tag}  {r['n']:3}tr {r['n']/8:.1f}/wk win {r['win']:.0%} {(r['h1']+r['h2'])/r['n']:+.2f}R/tr | {r['h1']:+5.1f}/{r['h2']:+5.1f} = {r['h1']+r['h2']:+5.1f}R dd {r['dd']:+.1f}")
    import json; json.dump([(t_, P, r) for t_, P, r in R], open('/tmp/qm_grid.json', 'w'))
