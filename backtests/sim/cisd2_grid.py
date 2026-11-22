# Stage A: every entry model x stop model x entry mode x target x break-even, per chart timeframe (EURUSD, bias weeks).
import sys, os, itertools, json, multiprocessing as MP
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cisd2, harness, ltf
from smc import B, H
B.clear(); B.update(harness.B1)
TFS = {'5m': (ltf.load('EURUSD', '5'), 5), '15m': (ltf.load('EURUSD', '15'), 15), '30m': (ltf.load('EURUSD', '30'), 30), '1H': (harness.D1['EURUSD'], 60)}
TPS = {'TP2': dict(tps=(1.5, 1.0, 1.5, 2.0)), 'TP3': dict(tps=(1.5, 1.0, 2.0, 3.0)), 'TP4': dict(tps=(1.5, 1.0, 2.5, 4.0)),
       'liqNear': dict(tpMode='Nearest HTF liquidity'), 'liq1.5R': dict(tpMode='First HTF liquidity ≥ min R:R')}
def ev(job):
    tf, P = job; b, m = TFS[tf]
    hs = [cisd2.run('EURUSD', b, P, a, c, m) for a, c in H]
    t = sorted(hs[0] + hs[1], key=lambda x: x['tx']); eq = pk = dd = 0
    for x in t: eq += x['R']; pk = max(pk, eq); dd = min(dd, eq - pk)
    return tf, P, dict(n=len(t), h1=sum(x['R'] for x in hs[0]), h2=sum(x['R'] for x in hs[1]), dd=dd, win=sum(x['R'] > 0 for x in t))
def jobsA(tfs):
    out = []
    for tf in tfs:
        for e, s, em, tp, be in itertools.product(list(cisd2.ENTRY_FAM), ['piv', 'ob', 'cross', 'fvg', 'ifvg', 'brk'], ['Limit', 'Market'], list(TPS), [False, True]):
            P = dict(entry=e, stop=s, entryMode=em, be=be, **TPS[tp]); P['_tp'] = tp
            out.append((tf, P))
    return out
if __name__ == '__main__':
    tfs = sys.argv[1].split(',')
    J = jobsA(tfs)
    with MP.Pool(2) as pool: R = pool.map(ev, J, chunksize=40)
    json.dump(R, open(f'/tmp/cisdA_{"_".join(tfs)}.json', 'w'))
    print(len(R), 'runs')
