import sys; sys.path.insert(0,'backtests/sim')
exec(open('backtests/sim/usd_ideas.py').read().split('IDEAS = [')[0])
fmt = lambda s: f"{s['n']:3}tr {s['R']:+6.1f}R ({s['exp']:+.2f})"
C=[('Baseline',{}),
 ('Partial 1R+BE, TP3, Fri',{'partial':True,'tp':3,'hold':'fri'}),
 ('Partial + exh1.5',{'partial':True,'tp':3,'hold':'fri','exh':1.5}),
 ('both agree',{'dirm':'both'}),
 ('both + partial',{'dirm':'both','partial':True,'tp':3,'hold':'fri'}),
 ('both + partial + exh1.5',{'dirm':'both','partial':True,'tp':3,'hold':'fri','exh':1.5}),
 ('gap>=8 + partial',{'mingap':8,'partial':True,'tp':3,'hold':'fri'}),
]
for n,P in C:
    b=bias_run(P); t=trend_run({k:v for k,v in P.items() if k!='dirm' and k!='mingap'})
    print(f"{n:<26}| {fmt(b[0])} | {fmt(b[1])} | total {b[0]['R']+b[1]['R']:+.1f}R | trend-years "+' | '.join(fmt(x) for x in t))
# drawdown in R for bias baseline vs partial (chronological over all USD trades)
import itertools
for n,P in [C[0],C[1],C[4]]:
    tr=sorted(sum([run(p,data[p],B,P,H1[0],H2[1],usd) for p in USD],[]),key=lambda x:x['tx'])
    eq=0;pk=0;dd=0
    for x in tr: eq+=x['R'];pk=max(pk,eq);dd=min(dd,eq-pk)
    print(n,'maxDD',round(dd,1),'R')
print()
for n,P in [('both SMA50',{'dirm':'both','trlen':50}),('both SMA50 + partial',{'dirm':'both','trlen':50,'partial':True,'tp':3,'hold':'fri'})]:
    b=bias_run(P); print(n,fmt(b[0]),fmt(b[1]))
    tr=sorted(sum([run(p,data[p],B,P,H1[0],H2[1],usd) for p in USD],[]),key=lambda x:x['tx']); eq=pk=dd=0
    for x in tr: eq+=x['R'];pk=max(pk,eq);dd=min(dd,eq-pk)
    print('  maxDD',round(dd,1))
