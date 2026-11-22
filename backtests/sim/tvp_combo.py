import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from st_grid import ev, fmt, EUR, USD
print('== BE Swing (your settings): USD | EUR hold-out')
for n, P in [('base', {}), ('filter: TVP trend agrees', dict(tvf='trend')), ('filter: TVP trend not against', dict(tvf='notagainst')),
             ('filter: close beyond rolling POC', dict(tvf='poc')), ('filter: trend + beyond POC', dict(tvf='trend_poc')),
             ('filter: trend started <= 12 bars ago', dict(tvf='young')),
             ('exit: TVP trend flips', dict(tvx='flip')), ('trail: boundary band (always)', dict(tvx='band')), ('trail: boundary band after +1R', dict(tvx='band_1R'))]:
    print(f"  {n:<40} {fmt(ev(P))} | EUR {fmt(ev({**P, 'mingap': 5}, EUR))}", flush=True)
import cisd
from harness import go
print('== CISD (TP 3R, no BE)')
for n, P in [('base', dict(be=None)), ('filter: TVP trend agrees', dict(be=None, tvf='trend')), ('filter: TVP trend against', dict(be=None, tvf='counter'))]:
    print(f"  {n:<40} {go(lambda p, b, Q, s, e: cisd.run(p, b, {**Q, 'htf': 'D'}, s, e), P)}", flush=True)
