import sys,glob,os,datetime as D,statistics as S,itertools
sys.path.insert(0,'backtests/sim'); from swing_sim import *
start=D.datetime(2026,10,11,21,tzinfo=D.timezone.utc)
data={}
for f in sorted(glob.glob('backtests/ohlc/*_240.csv')):
    p=os.path.basename(f).split('_')[1]; b=load(f); a,s=daily(b); data[p]=(b,a,s,bias_for(p))
def tot(dm,cf,k=1.0,tp=2,hold=4,tr=0):
    out={}
    for p,(b,a,s,bi) in data.items():
        r=run(b,a,s,bi,p,dirm=dm,cf=cf,k=k,tp=tp,hold=hold,trail=tr,start=start,trlen=20,pip=0.01 if 'JPY' in p else 0.0001)
        out[p]=summ(r)
    return out
for dm in ['bias','trend','both']:
  for cf in ['none','wtd']:
    o=tot(dm,cf); n=sum(v[0] for v in o.values()); s=sum(v[1] for v in o.values())
    print(f'{dm:5} {cf:4} n={n:3} net={s:+5.1f}R exp={s/max(n,1):+.2f}  ',' '.join(f"{p}:{v[1]:+.1f}" for p,v in o.items()))
# robustness: medians across 72 param combos for each dm/cf
for dm in ['bias','trend','both']:
  for cf in ['none','wtd']:
    v=[]
    for k,tp,h,tr in itertools.product([0.75,1,1.5],[0,1.5,2,3],[2,3,4],[0,1.5]):
        o=tot(dm,cf,k,tp,h,tr); v.append(sum(x[1] for x in o.values()))
    print(dm,cf,'median',round(S.median(v),1),'>0',sum(x>0 for x in v),'/',len(v))
