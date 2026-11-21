import csv,glob,re,collections
def load(f):
    T={}
    for r in csv.DictReader(open(f,encoding='utf-8-sig')): T.setdefault(int(r['Trade number']),{})[r['Type'].split()[0]]=r
    rows=[]
    for n,d in sorted(T.items()):
        e,x=d['Entry'],d['Exit']
        g=lambda k:float(next(v for kk,v in x.items() if kk.startswith(k)))
        pnl=g('Net PnL'); cum=g('Cumulative PnL'); rows.append(dict(et=e['Date and time'],xt=x['Date and time'],why=x['Signal'],R=pnl/((10000+cum-pnl)*0.01)))
    tr=collections.OrderedDict()
    for r in rows: t=tr.setdefault(r['et'],dict(et=r['et'],xt=r['xt'],R=0,why=[])); t['R']+=r['R']; t['xt']=max(t['xt'],r['xt']); t['why'].append(r['why'])
    return list(tr.values())
for tf in ['60','240']:
    allt=[]; print(f'\n=== {tf}')
    for f in sorted(glob.glob(f'BE_Swing_S_*_{tf}.csv')):
        p=f.split('_')[3]; t=load(f); allt+= [dict(x,pair=p) for x in t]
        print(f"{p}: {len(t)} trades {sum(x['R'] for x in t):+.1f}R  wins {sum(x['R']>0.05 for x in t)} BE {sum(abs(x['R'])<=0.05 for x in t)} losses {sum(x['R']<-0.05 for x in t)}")
    allt.sort(key=lambda x:x['xt']); eq=pk=dd=0
    for x in allt: eq+=x['R'];pk=max(pk,eq);dd=min(dd,eq-pk)
    import datetime as D
    wk=collections.OrderedDict()
    for x in allt: k=D.date.fromisoformat(x['xt'][:10]).isocalendar()[1]; wk[k]=wk.get(k,0)+x['R']
    print('TOTAL',len(allt),'trades',round(sum(x['R'] for x in allt),1),'R  maxDD',round(dd,1),' weeks',{f'W{k}':round(v,1) for k,v in wk.items()})
