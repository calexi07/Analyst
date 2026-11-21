import csv,re,collections,glob,sys
tr=[]
for f in sorted(glob.glob(__import__('os').path.join(__import__('os').path.dirname(__file__) or '.', '*BE_Setups*.csv'))):
    rows=list(csv.DictReader(open(f,encoding='utf-8-sig')))
    T={}
    for r in rows: T.setdefault(int(r['Trade number']),{})[r['Type'].split()[0]]=r
    for n,d in T.items():
        if 'Exit' not in d or d['Exit']['Signal']=='Open': continue
        e,x=d['Entry'],d['Exit']; s=e['Signal']
        m=re.search(r'^(\w+) \| \w+ \| bias [\w-]+ (\w+) gap ([+-]?\d+) \| check ([^|]+) \| sweep (\d\d):\d\d (\w+(?: York)?) \| SL ([\d.]+)p \| POC after ([\d.]+)h',s)
        pair,conv,gap,ck,hh,sess,sl,poc=m.groups()
        pnl=float(next(v for k,v in x.items() if k.startswith('Net PnL')))
        tr.append(dict(pair=pair,conv=conv,gap=int(gap),ck=ck.strip(),hh=int(hh),sess=sess,sl=float(sl),poc=float(poc),R=2.0 if pnl>0 else -1.0,mfe=float(next(v for k,v in x.items() if k.startswith('Favorable excursion') and not k.endswith('%')))/100))
def st(v): 
    w=sum(t['R']>0 for t in v); r=sum(t['R'] for t in v); sp=sum((3 if t['pair']=='XAUUSD' else 1)/t['sl'] for t in v)
    return f"n={len(v):3} win={100*w/max(len(v),1):3.0f}% net={r:+5.0f}R  spread1p={r-sp:+5.1f}R  exp={r/max(len(v),1):+.2f}R"
def rep(name,key):
    g=collections.OrderedDict()
    for t in sorted(tr,key=lambda t:str(key(t))): g.setdefault(key(t),[]).append(t)
    print(f'\n{name}')
    for k,v in g.items(): print(f'  {k:<12} {st(v)}')
print('ALL', st(tr))
rep('Pair',lambda t:t['pair'])
rep('Session',lambda t:t['sess'])
rep('SL',lambda t:'a <5' if t['sl']<5 else 'b 5-10' if t['sl']<=10 else 'c 10-20' if t['sl']<=20 else 'd >20')
rep('Conviction',lambda t:t['conv'])
rep('POC',lambda t:'a <1h' if t['poc']<1 else 'b 1-2h' if t['poc']<2 else 'c >=2h')
L=[t for t in tr if t['R']<0]; print('\nlosers',len(L),'reached 1R:',sum(t['mfe']>=1 for t in L),' 0.5R:',sum(t['mfe']>=0.5 for t in L))
for name,f in [('POC<2h',lambda t:t['poc']<2),('POC<2h & SL<=20',lambda t:t['poc']<2 and t['sl']<=20),('POC<2h & SL 5-20',lambda t:t['poc']<2 and 5<=t['sl']<=20),('not NY',lambda t:t['sess']!='New York'),('POC<2h & not NY',lambda t:t['poc']<2 and t['sess']!='New York')]:
    v=[t for t in tr if f(t)]; print(f'{name:<20}',st(v))

# extra cuts
rep('|gap|',lambda t:'a 3-4' if abs(t.get('gap',0))<=4 else 'b 5-7' if abs(t.get('gap',0))<=7 else 'c 8+')
rep('JPY cross',lambda t:'JPY' if 'JPY' in t['pair'] else 'other')
rep('Check (since 11 Nov)',lambda t:t['ck'])
v=[t for t in tr if t['sess']=='London']; print('\nLondon by pair'); 
for p in sorted(set(t['pair'] for t in v)):
    w=[t for t in v if t['pair']==p]; print(' ',p,len(w),sum(t['R'] for t in w))

print('\nCombos')
post=[t for t in tr if t['ck']!='none']
okck=lambda t:t['ck'].startswith('Confirmed')
for name,f,src in [('post-11Nov all',lambda t:True,post),('post: check Confirmed*',okck,post),('post: watch/pressure/invalid',lambda t:not okck(t),post),
                   ('no JPY',lambda t:'JPY' not in t['pair'],tr),('no JPY & no NY',lambda t:'JPY' not in t['pair'] and t['sess']!='New York',tr),
                   ('post: Confirmed & no JPY',lambda t:okck(t) and 'JPY' not in t['pair'],post)]:
    v=[t for t in src if f(t)]; print(f'  {name:<30}',st(v))
