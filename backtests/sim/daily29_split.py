import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'daily29.py')).read().replace("os.path.dirname(os.path.abspath(__file__))","os.path.dirname(os.path.abspath(__file__))").split("print('=== 4.5")[0])
USDP=['EURUSD','GBPUSD','AUDUSD','NZDUSD','USDJPY','USDCHF','USDCAD','XAUUSD']
bias = lambda p, wk, i0: {'U': 1, 'D': -1}.get(BIAS.get((wk, p)), 0)
inb = lambda wk: wk[0] == 2026 and 40 <= wk[1] <= 47
for grp,name in [(USDP,'USD pairs'),([p for p in PAIRS if p not in USDP],'crosses')]:
    for rule in ('hold','wtd','pull'):
        tr=[x for x in run(bias,rule,inb) if x[1] in grp]; rep(f'{name}: bias + {rule}',tr)
# per week, all pairs bias hold
tr=run(bias,'hold',inb); wk=collections.defaultdict(list)
for w,p,r in tr: wk[w[1]].append(r)
print({k:round(sum(v),1) for k,v in sorted(wk.items())})
pp=collections.defaultdict(float); cc=collections.defaultdict(float)
for w,p,r in run(bias,'hold',inb):
    pp[p]+=r
    if p not in USDP:
        d={'U':1,'D':-1}[BIAS[(w,p)]]
print(sorted(((round(v,1),k) for k,v in pp.items())))
