# Does price "react" at the MAs more than anywhere else? 10y, 12 instruments, 4H and 1H.
# For bars in a trend stack: P(+1 ATR in the trend direction before −1 ATR) when the bar touched the MA vs when it did not.
import sys; sys.path.insert(0, '/home/claude/analyst/backtests/sim10'); sys.path.insert(0, '/home/claude/analyst/backtests/sim')
from multi import ema, rma
from multi_10y import agg, PAIRS
from core import load
def first(b, i, d, k=1.0, mh=60):
    e = b[i]['c']; a = b[i]['atr']; up = e + d * k * a; dn = e - d * k * a
    for j in range(i + 1, min(len(b), i + mh)):
        y = b[j]; hu = (y['h'] >= up) if d > 0 else (y['l'] <= up); hd = (y['l'] <= dn) if d > 0 else (y['h'] >= dn)
        if hd: return 0
        if hu: return 1
    return None
for tf, m in [('4H', 240), ('1H', 60)]:
    agg_ = {'touch EMA50': [0, 0], 'touch SMMA50': [0, 0], 'touch SMMA100': [0, 0], 'no touch (all other trend bars)': [0, 0]}
    for p in PAIRS:
        b = agg(load(p)[0], m); C = [x['c'] for x in b]; e50 = ema(C, 50); s50 = rma(C, 50); s100 = rma(C, 100)
        for i in range(110, len(b) - 1):
            x = b[i]
            if s100[i] is None or not x['atr']: continue
            d = 1 if e50[i] > s50[i] > s100[i] else -1 if e50[i] < s50[i] < s100[i] else 0
            if not d: continue
            tch = lambda lv: (x['l'] <= lv <= x['h'])
            key = 'touch EMA50' if tch(e50[i]) else 'touch SMMA50' if tch(s50[i]) else 'touch SMMA100' if tch(s100[i]) else 'no touch (all other trend bars)'
            r = first(b, i, d)
            if r is None: continue
            agg_[key][0] += r; agg_[key][1] += 1
    print(f"{tf}: " + " · ".join(f"{k}: {v[0]/v[1]:.1%} of {v[1]}" for k, v in agg_.items()))
