# BE Swing exports: R per trade = Net PnL / (1% of equity before the trade). Usage: python3 analyze.py [glob]
import csv,re,glob,sys,collections,os
pat=sys.argv[1] if len(sys.argv)>1 else '*BE_Swing*.csv'
tr=[]
for f in sorted(glob.glob(os.path.join(os.path.dirname(__file__) or '.',pat))):
    if '4H-run' in f: continue
    T={}
    for r in csv.DictReader(open(f,encoding='utf-8-sig')): T.setdefault(int(r['Trade number']),{})[r['Type'].split()[0]]=r
    for n,d in T.items():
        if 'Exit' not in d or d['Exit']['Signal']=='Open': continue
        e,x=d['Entry'],d['Exit']; s=e['Signal']
        m=re.search(r'^(\w+) \| (\w+) \| bias ([\w-]+) (\S+) gap ([+-]?\d+) \| trend (\w+) \| wtd (\w+) \| sma20 (\w+) \| check ([^|]+) \| entry (\S+) \| SL ([\d.]+)p \| dir ([^|]+) \| (\w+)',s)
        if not m: print('skip',s); continue
        pair,side,bias,conv,gap,trend,wtd,sma,ck,en,sl,dmode,dow=m.groups()
        g=lambda k:float(next(v for kk,v in x.items() if kk.startswith(k)))
        pnl=g('Net PnL'); cum=g('Cumulative PnL'); mfe=float(next(v for kk,v in x.items() if kk.startswith('Favorable excursion') and not kk.endswith('%')))
        risk=(10000+cum-pnl)*0.01
        tr.append(dict(pair=pair,side=side,conv=conv,gap=int(gap),trend=trend,wtd=wtd,sma=sma,ck=ck.strip(),dmode=dmode.strip(),dow=dow,exit=x['Signal'],R=pnl/risk,mfe=mfe/risk,file=os.path.basename(f)))
def st(v):
    if not v: return 'n=0'
    w=sum(t['R']>0 for t in v); r=sum(t['R'] for t in v)
    return f"n={len(v):3} win={100*w/len(v):3.0f}% net={r:+6.1f}R exp={r/len(v):+.2f}R"
def rep(name,key):
    gg={}
    for t in tr: gg.setdefault(key(t),[]).append(t)
    print('\n'+name)
    for k in sorted(gg,key=str): print(f'  {str(k):<22}',st(gg[k]))
print('ALL',st(tr))
for n,k in [('Mode',lambda t:t['dmode']),('Pair',lambda t:t['pair']),('Exit',lambda t:t['exit']),('Week-to-date',lambda t:t['wtd']),('Trend',lambda t:t['trend']),('SMA20',lambda t:t['sma']),('Conviction',lambda t:t['conv']),('Check',lambda t:t['ck']),('Day',lambda t:t['dow'])]: rep(n,k)
