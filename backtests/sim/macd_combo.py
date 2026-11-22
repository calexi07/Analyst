import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from st_grid import ev, fmt, EUR, USD
print('== BE Swing (your settings): USD | EUR hold-out')
for n, P in [('base', {}), ('filter: hist on trade side (MACD>signal)', dict(mcf='above')), ('filter: MACD on trade side of zero', dict(mcf='trend')),
             ('filter: both', dict(mcf='both')), ('filter: hist rising', dict(mcf='hrising')), ('filter: hist not fading', dict(mcf='notfade')),
             ('filter: trend side but hist against (pullback)', dict(mcf='pullback')),
             ('exit: cross against', dict(mcx='cross')), ('exit: cross after +1R', dict(mcx='cross_1R')), ('exit: cross after +2R', dict(mcx='cross_2R')),
             ('exit: 2 fading after +1R', dict(mcx='fade2_1R')), ('exit: cross after +1R, no TP', dict(mcx='cross_1R', tp=0)),
             ('exit: cross after +2R, no TP', dict(mcx='cross_2R', tp=0))]:
    print(f"  {n:<46} {fmt(ev(P))} | EUR {fmt(ev({**P, 'mingap': 5}, EUR))}", flush=True)
import cisd
from harness import go
print('== CISD (TP 3R, no BE)')
for n, P in [('base', dict(be=None)), ('filter: MACD > signal', dict(be=None, mcf='above')), ('filter: MACD < signal', dict(be=None, mcf='below')),
             ('filter: MACD trend side of zero', dict(be=None, mcf='trend')), ('filter: MACD counter side', dict(be=None, mcf='counter'))]:
    print(f"  {n:<46} {go(lambda p, b, Q, s, e: cisd.run(p, b, {**Q, 'htf': 'D'}, s, e), P)}", flush=True)
