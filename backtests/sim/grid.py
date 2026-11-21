# Runs the BE Swing variant grid on every backtests/ohlc/FOREXCOM_<PAIR>_240.csv. Usage: python3 backtests/sim/grid.py
import sys,os,glob,itertools,statistics as S,datetime as D
sys.path.insert(0,os.path.dirname(__file__)); from swing_sim import *
start=D.datetime(2026,9,27,21,tzinfo=D.timezone.utc)
files=sorted(glob.glob(os.path.join(os.path.dirname(__file__),'../ohlc/FOREXCOM_*_240.csv')))
G=list(itertools.product(['bias','trend'],['none','wtd'],[0.75,1.0,1.5],[0,1.5,2,3],[2,3,4],[0,1.5]))
tot={g:[0,0] for g in G}
for f in files:
    pair=os.path.basename(f).split('_')[1]; pip=0.01 if 'JPY' in pair else 0.1 if 'XAU' in pair else 0.0001
    bars=load(f); atr,sma=daily(bars); bias=bias_for(pair)
    per={}
    for g in G:
        r=run(bars,atr,sma,bias,pair,dirm=g[0],cf=g[1],k=g[2],tp=g[3],hold=g[4],trail=g[5],start=start,trlen=20,pip=pip,cost_pips=3 if 'XAU' in pair else 1)
        n,s,w=summ(r); per[g]=(n,s); tot[g][0]+=n; tot[g][1]+=s
    d=(G[0][0])
    base=('bias','none',1.0,2,4,0); tb=('trend','none',1.0,2,4,0)
    bv=[per[g][1] for g in G if g[0]=='bias']; tv=[per[g][1] for g in G if g[0]=='trend']
    print(f"{pair}: default bias {per[base][1]:+.1f}R ({per[base][0]} tr) | trend {per[tb][1]:+.1f}R | bias variants >0 {sum(x>0 for x in bv)}/{len(bv)} median {S.median(bv):+.1f} | trend >0 {sum(x>0 for x in tv)}/{len(tv)} median {S.median(tv):+.1f}")
print('\nALL PAIRS')
for dm in ['bias','trend']:
    v=[tot[g][1] for g in G if g[0]==dm]; print(f" {dm}: variants >0 {sum(x>0 for x in v)}/{len(v)} median {S.median(v):+.1f}R")
for lab,idx,vals in [('confirm',1,['none','wtd']),('SL ATR',2,[0.75,1.0,1.5]),('TP',3,[0,1.5,2,3]),('hold d',4,[2,3,4]),('trail',5,[0,1.5])]:
    print(f" bias by {lab}:",{v:round(S.median([tot[g][1] for g in G if g[idx]==v and g[0]=='bias']),1) for v in vals})
