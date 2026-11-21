import sys,collections; sys.path.insert(0,'backtests/sim')
exec(open('backtests/sim/usd_entries.py').read().replace("os.path.dirname(os.path.abspath(__file__))","'backtests/sim'").split("E = [")[0])
for n,P in [('SWP none',dict(entry='SWP',cf='none')),('WO',dict(entry='WO')),('D wtd',dict(entry='D')),('A wtd',dict(entry='A'))]:
    Q={**EX,**P,'dirm':'both'}; t=sum([run(p,data[p],B,Q,H[0][0],H[1][1],usd) for p in USD],[])
    pp=collections.defaultdict(float); wk=collections.defaultdict(float)
    for x in t: pp[x['pair']]+=x['R']; wk[x['wk'][1]]+=x['R']
    print(n,'pairs',{k:round(v,1) for k,v in pp.items()},'weeks',{k:round(v,1) for k,v in sorted(wk.items())})
    Q2={**Q,'dirm':'bias'}; t2=sum([run(p,data[p],B,Q2,H[0][0],H[1][1],usd) for p in USD],[]); print('   bias-only',len(t2),round(sum(x['R'] for x in t2),1))
for lab,Q in [('SWP bias-only',{**EX,'entry':'SWP','cf':'none','dirm':'bias'}),('SWP bias-only + wtd',{**EX,'entry':'SWP','cf':'wtd','dirm':'bias'})]:
    t=sum([run(p,data[p],B,Q,H[0][0],H[1][1],usd) for p in USD],[]); wk=collections.defaultdict(float)
    for x in t: wk[x['wk'][1]]+=x['R']
    eq=pk=m=0
    for x in sorted(t,key=lambda x:x['tx']): eq+=x['R'];pk=max(pk,eq);m=min(m,eq-pk)
    w=[round(wk.get(k,0),1) for k in range(40,48)]
    print(lab,len(t),'R',round(sum(w),1),'weeks',w,'2wk',[round(w[i]+w[i+1],1) for i in range(0,8,2)],'maxDD',round(m,1),'win',round(sum(x['R']>0 for x in t)/len(t),2))
