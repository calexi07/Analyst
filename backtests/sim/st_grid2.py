import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from st_grid import ev, fmt, EUR, USD
import itertools
base = ev({})
both = []
for tf, per, m, tp in itertools.product(['4h', '1h'], [7, 10, 14], [1.0, 1.5, 2.0, 3.0], [4, 0]):
    for trm, stat in [('st', 0), ('st_after', 1), ('st_after', 2), ('tighter', 0)]:
        P = dict(trm=trm, stat=stat, sttf=tf, stp=per, stm=m, tp=tp); r = ev(P)
        if r['h1'] > base['h1'] and r['h2'] > base['h2']: both.append((P, r))
print('beats both halves:', [(P, fmt(r)) for P, r in both])
print('EUR base', fmt(ev({'mingap': 5}, EUR)))
for P in [dict(trm='st_after', stat=1, sttf='4h', stp=10, stm=1.0, tp=0), dict(trm='st_after', stat=2, sttf='4h', stp=10, stm=1.0, tp=0),
          dict(trm='st_after', stat=2, sttf='4h', stp=10, stm=1.0, tp=4), dict(slm='tighter', stp=10, stm=2.0)] + [P for P, _ in both]:
    print(P, 'EUR', fmt(ev({**P, 'mingap': 5}, EUR)))
