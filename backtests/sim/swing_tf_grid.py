import sys, os, itertools, json, multiprocessing as MP, statistics as St, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness, ltf, swing_tf as S
from smc import H
B = harness.B1
PAIRS = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'USDCAD', 'AUDUSD', 'NZDUSD']
MODE = sys.argv[1]           # '1H' (all 7 USD pairs, 1H path) or '15m' (EURUSD, 5m path)
if MODE == '1H': DATA = {p: (S.prep(harness.D1[p]), None) for p in PAIRS}
else:
    PAIRS = ['EURUSD']; s15 = S.prep(ltf.load('EURUSD', '15')); p5 = S.prep(ltf.load('EURUSD', '5')); DATA = {'EURUSD': (s15, p5)}
def ev(P):
    hs = []
    for a, c in H:
        hs.append(sum([S.run(p, DATA[p][0], DATA[p][1] or DATA[p][0], B, P, a, c) for p in PAIRS], []))
    t = sorted(hs[0] + hs[1], key=lambda x: x['tx']); eq = pk = dd = 0
    for x in t: eq += x['R']; pk = max(pk, eq); dd = min(dd, eq - pk)
    pp = collections.defaultdict(float)
    for x in t: pp[x['pair']] += x['R']
    return P, dict(n=len(t), h1=sum(x['R'] for x in hs[0]), h2=sum(x['R'] for x in hs[1]), dd=dd, win=sum(x['R'] > 0 for x in t), pp=dict(pp))
if __name__ == '__main__':
    if len(sys.argv) > 2:
        print(ev(json.loads(sys.argv[2]))[1]); sys.exit()
    G = dict(entry=['C', 'A'], slk=[1.0, 1.5, 2.0, 3.0], tp=[2, 3, 4, 6], trk=[None, 1.0, 1.5, 2.5], trk2=[None, 'half'], cool=[4, 12, 24], maxdow=[2, 3], dirm=['both', 'bias'])
    J = []
    for v in itertools.product(*G.values()):
        P = dict(zip(G, v))
        if P['trk'] is None and P['trk2']: continue
        if P['trk2'] == 'half': P['trk2'] = P['trk'] / 2
        J.append(P)
    print(len(J), 'runs', flush=True)
    with MP.Pool(2) as pool: R = pool.map(ev, J, chunksize=20)
    json.dump(R, open(f'/tmp/swtf_{MODE}.json', 'w')); print('done')
