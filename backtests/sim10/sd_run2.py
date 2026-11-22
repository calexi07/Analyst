# quality filters on 10y: which zone feature separates good from bad?
import sys, collections
sys.path.insert(0, '/home/claude/analyst/backtests/sim10')
import sd, sd_data
from core import COST
P = ['EURUSD', 'GBPUSD', 'XAUUSD', 'USDJPY', 'AUDUSD', 'USDCAD', 'EURJPY', 'GBPJPY']
DATA = {p: sd_data.ten_year(p) for p in P}
def st(o):
    R = [x[1] for x in o]; n = len(R)
    if not n: return '     0tr'
    y = collections.defaultdict(float)
    for t, r, z in o: y[t.year] += r
    return f"{n:5d}tr {sum(R)/n:+.3f}/tr y+{sum(v > 0 for v in y.values())}/{len(y)}"
for htf in ['4H', '1H']:
    ZZ = {p: sd.zones(DATA[p][1][htf]) for p in P}
    # one broad run per setup, then slice by zone features (filters applied after the fact = same trades)
    for lab, kw in [('limit at proximal, SL distal, TP3', dict(conf='none', entry='limit', sl='htf', tp=3.0)),
                    ('15m CHoCH, SL LTF leg, TP3', dict(conf='choch', entry='mkt', sl='ltf', tp=3.0)),
                    ('15m CHoCH, SL distal, TP2', dict(conf='choch', entry='mkt', sl='htf', tp=2.0))]:
        for dirn in ['trend', 'both']:
            o = []
            for p in P:
                l, hh, trend = DATA[p]
                o += sd.run(l, hh[htf], ZZ[p], trend if dirn == 'trend' else (lambda x: (1, -1)), COST[p], **kw)
            print(f"\n{htf} · {lab} · {dirn}: ALL {st(o)}")
            for name, f in [('BOS by departure', lambda z: z['bos']), ('no BOS', lambda z: not z['bos']),
                            ('strength >= 2 ATR', lambda z: z['strength'] >= 2), ('strength < 1.5', lambda z: z['strength'] < 1.5),
                            ('base 1-2 candles', lambda z: z['nbase'] <= 2), ('base 4-6', lambda z: z['nbase'] >= 4),
                            ('reversal DBR/RBD', lambda z: z['kind'] in ('DBR', 'RBD')), ('continuation RBR/DBD', lambda z: z['kind'] in ('RBR', 'DBD')),
                            ('narrow zone < 0.7 ATR', lambda z: z['width'] < 0.7), ('wide zone > 1.5 ATR', lambda z: z['width'] > 1.5),
                            ('BOS + strength>=2 + base<=2', lambda z: z['bos'] and z['strength'] >= 2 and z['nbase'] <= 2)]:
                print(f"   {name:30} {st([x for x in o if f(x[2])])}")
