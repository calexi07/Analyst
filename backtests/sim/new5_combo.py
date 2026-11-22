import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from st_grid import ev, fmt, EUR, USD
import cisd
from harness import go
print('== BE Swing (your settings): USD | EUR hold-out')
print(f"  {'base':<40} {fmt(ev({}))} | EUR {fmt(ev({'mingap': 5}, EUR))}")
for nm, lab in [('vrb', 'VWAP Range smart trend'), ('swc', 'Swing Clock swing dir'), ('trap', 'trap signal last 12 bars'),
                ('lsrt', 'LSRT signal last 12 bars'), ('asr', 'S/R bounce last 12 bars')]:
    for n, P in [(f'filter {lab} agrees', dict(xf=(nm, 'agree'))), (f'filter {lab} not against', dict(xf=(nm, 'notagainst'))),
                 (f'exit when {lab} turns against', dict(xx=nm))]:
        print(f"  {n:<52} {fmt(ev(P))} | EUR {fmt(ev({**P, 'mingap': 5}, EUR))}", flush=True)
print('== CISD (TP 3R, no BE)')
print('  base', go(lambda p, b, Q, s, e: cisd.run(p, b, {**Q, 'htf': 'D'}, s, e), dict(be=None)))
for nm in ['vrb', 'swc', 'trap', 'lsrt', 'asr']:
    for m in ['agree', 'against']:
        print(f"  {nm} {m:<8}", go(lambda p, b, Q, s, e: cisd.run(p, b, {**Q, 'htf': 'D'}, s, e), dict(be=None, xf=(nm, m))), flush=True)
