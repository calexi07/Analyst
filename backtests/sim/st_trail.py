# Supertrend line (on 4H) as the trailing stop of BE Swing (entry C on the 1H path, hours 06-22, user's settings).
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mtf_c import *
PAIRS = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'USDCAD', 'AUDUSD', 'NZDUSD', 'XAUUSD']
B = bias_table(); D4 = {p: prep4(p) for p in PAIRS}; D1 = {p: load1h(p) for p in PAIRS}
def ev(P):
    hs = [sum([run_c(p, D4[p], D1[p], B, {**P, 'hours': (6, 22)}, a, c) for p in PAIRS], []) for a, c in H]
    t = sorted(hs[0] + hs[1], key=lambda x: x['tx']); eq = pk = dd = 0
    for x in t: eq += x['R']; pk = max(pk, eq); dd = min(dd, eq - pk)
    why = collections.Counter(x['why'] for x in t)
    return f"{len(t):3}tr win {sum(x['R'] > 0 for x in t) / max(1, len(t)):.0%} {sum(x['R'] for x in hs[0]):+5.1f}/{sum(x['R'] for x in hs[1]):+5.1f} = {eq:+5.1f}R dd {dd:+.1f}  {dict(why)}"
for n, P in [('your settings: TP 4R, trail 0.75 ATR -> 0.5 after 2R', {}),
             ('ST 10/3 line instead of ATR trail, TP 4R', dict(trm='st')),
             ('ST 10/3 line, no TP', dict(trm='st', tp=0)),
             ('ST 10/2 line, TP 4R', dict(trm='st', stm=2.0)),
             ('ST 10/2 line, no TP', dict(trm='st', stm=2.0, tp=0)),
             ('ST 10/1.5 line, TP 4R', dict(trm='st', stm=1.5)),
             ('tighter of ATR trail and ST 10/3, TP 4R', dict(trm='tighter')),
             ('tighter of ATR trail and ST 10/2, TP 4R', dict(trm='tighter', stm=2.0)),
             ('ATR trail until +1R, then ST 10/2, TP 4R', dict(trm='st_after', stm=2.0, stat=1.0)),
             ('ATR trail until +2R, then ST 10/2, no TP', dict(trm='st_after', stm=2.0, stat=2.0, tp=0))]:
    print(f"{n:<46} {ev(P)}")
