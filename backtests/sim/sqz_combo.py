# Squeeze Momentum as filter / exit for BE Swing (8 USD pairs + EUR crosses |gap|>=5 hold-out) and as filter for CISD.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from st_grid import ev, fmt, EUR, USD
print('== BE Swing (your settings), USD pairs | EUR crosses hold-out')
for n, P in [('base', {}), ('filter: momentum on trade side', dict(sqf='pos')), ('filter: momentum rising', dict(sqf='rising')),
             ('filter: on side and rising', dict(sqf='both')), ('filter: not fading', dict(sqf='notfade')),
             ('filter: against but turning (pullback)', dict(sqf='neg_rising')), ('filter: no squeeze on', dict(sqf='nosqz')),
             ('filter: squeeze on', dict(sqf='sqzon')), ('filter: fired <= 6 bars', dict(sqf='fired')),
             ('exit: 2 fading 4H bars', dict(sqx='fade2')), ('exit: 2 fading after +1R', dict(sqx='fade2_1R')),
             ('exit: fading after +2R', dict(sqx='fade_2R')), ('exit: momentum flips side', dict(sqx='zero')),
             ('exit: 2 fading after +1R, no TP', dict(sqx='fade2_1R', tp=0)), ('rising filter + fade2 after 1R', dict(sqf='rising', sqx='fade2_1R'))]:
    print(f"  {n:<40} {fmt(ev(P))} | EUR {fmt(ev({**P, 'mingap': 5}, EUR))}", flush=True)
import cisd
from harness import go
print('== CISD (TP 3R, no BE)')
for n, P in [('base', dict(be=None)), ('filter: momentum > 0', dict(be=None, sqf='pos')), ('filter: momentum rising', dict(be=None, sqf='rising')),
             ('filter: momentum < 0 (still against)', dict(be=None, sqf='neg'))]:
    print(f"  {n:<40} {go(lambda p, b, Q, s, e: cisd.run(p, b, {**Q, 'htf': 'D'}, s, e), P)}", flush=True)
