# 10-year check (2012-2022, ejtraderLabs 15m aggregated to 1H / 4H) of the best signals, no bias
import sys; sys.path.insert(0, '/home/claude/analyst/backtests/sim10')
from multi import trades
from core import load, COST
import collections
def agg(bars, mins):
    out = []
    for b in bars:
        k = b['t'].replace(minute=0, second=0, hour=b['t'].hour // (mins // 60) * (mins // 60))
        if out and out[-1]['t'] == k: y = out[-1]; y['h'] = max(y['h'], b['h']); y['l'] = min(y['l'], b['l']); y['c'] = b['c']
        else: out.append(dict(t=k, o=b['o'], h=b['h'], l=b['l'], c=b['c']))
    A = None
    for i, x in enumerate(out):
        tr = x['h'] - x['l'] if i == 0 else max(x['h'], out[i-1]['c']) - min(x['l'], out[i-1]['c'])
        A = tr if A is None else (A * 13 + tr) / 14; x['atr'] = A if i >= 13 else None
    return out
PAIRS = ['EURUSD','GBPUSD','XAUUSD','AUDUSD','USDCAD','USDCHF','USDJPY','EURGBP','EURJPY','EURCHF','GBPJPY','AUDJPY']
both = lambda x: (1, -1)
for tf, mins, mh in [('4H', 240, 30), ('1H', 60, 48)]:
    data = {p: agg(load(p)[0], mins) for p in PAIRS}
    for kd in ['us30_setup', 'sqz_zero', 'eob', 'bos']:
        o = []; byp = {}; byy = collections.defaultdict(float)
        for p in PAIRS:
            t = trades(data[p], kd, both, COST[p], 1.5, 3, mh); o += t; byp[p] = sum(r for _, r in t)
            for x in t: byy[x[0].year] += x[1]
        R = [r for _, r in o]
        print(f"{tf} {kd:11} 10y 12 instr: {len(R)}tr {sum(R):+.1f}R {sum(R)/len(R):+.3f}/tr · years+ {sum(v>0 for v in byy.values())}/{len(byy)} · pairs+ {sum(v>0 for v in byp.values())}/12 · best {max(byp, key=byp.get)} {max(byp.values()):+.0f}R")
