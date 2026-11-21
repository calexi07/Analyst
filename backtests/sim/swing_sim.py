# Replays the BE Swing rules on 4H OHLC exports (TradingView "Export chart data") so variants can be tested without re-running the Strategy Tester.
import csv,json,sys,os,itertools,math,datetime as D
from zoneinfo import ZoneInfo
NY=ZoneInfo('America/New_York')
def load(path):
    bars=[]
    for r in csv.DictReader(open(path)):
        t=D.datetime.fromisoformat(r['time']).astimezone(D.timezone.utc)
        bars.append(dict(t=t,o=float(r['open']),h=float(r['high']),l=float(r['low']),c=float(r['close'])))
    for b in bars:
        ny=(b['t']+D.timedelta(hours=7)).astimezone(NY); b['day']=ny.date(); b['dow']=ny.weekday()  # trading day, Mon=0
        b['tc']=b['t']+D.timedelta(hours=4)
    return bars
def daily(bars):
    days={}
    for b in bars:
        d=days.setdefault(b['day'],dict(o=b['o'],h=b['h'],l=b['l'],c=b['c']))
        d['h']=max(d['h'],b['h']); d['l']=min(d['l'],b['l']); d['c']=b['c']
    ks=sorted(days); atr={}; sma={}; trs=[]; cl=[]; prevc=None
    for i,k in enumerate(ks):
        d=days[k]
        # values known at the start of day k = from days before k
        atr[k]=sum(trs[-14:])/14 if len(trs)>=14 else None
        sma[k]={n:(sum(cl[-n:])/n if len(cl)>=n else None) for n in (20,50)}
        tr=d['h']-d['l'] if prevc is None else max(d['h'],prevc)-min(d['l'],prevc); trs.append(tr); cl.append(d['c']); prevc=d['c']
    return atr,sma
def bias_for(pair):
    h=json.load(open(os.path.join(os.path.dirname(__file__),'../../pine/history.json')))
    out={}
    for W in h['weeks']:
        x=W['pairs'].get(pair)
        if x: out[(W['y'],W['w'])]=(x['b'],x['c'])
    return out
def run(bars,atr,sma,bias,pair,dirm='bias',cf='wtd',k=1.0,tp=2.0,hold=4,trail=0,cool=24,start=None,noFri=True,pip=0.0001,cost_pips=1.0,trlen=50):
    res=[]; pos=None; lastx=None; wko=None; wk=None
    for i,b in enumerate(bars):
        iso=b['day'].isocalendar()[:2]
        if iso!=wk: wk=iso; wko=b['o']
        # manage open position intrabar (bar after entry onward)
        if pos and i>pos['i']:
            d=pos['d']; hitS = b['l']<=pos['sl'] if d>0 else b['h']>=pos['sl']; hitT = pos['tp'] is not None and (b['h']>=pos['tp'] if d>0 else b['l']<=pos['tp'])
            ex=None
            if hitS: ex=(pos['sl'],'SL')
            elif hitT: ex=(pos['tp'],'TP')
            else:
                last = b['dow']==4 and (i+1==len(bars) or bars[i+1]['day']!=b['day'])
                if last: ex=(b['c'],'Fri')
                elif (b['tc']-pos['t']).total_seconds()>=hold*86400: ex=(b['c'],'Time')
                elif trail:
                    ns=b['c']-d*trail*pos['atr']; pos['sl']=max(pos['sl'],ns) if d>0 else min(pos['sl'],ns)
            if ex:
                r=(ex[0]-pos['e'])*d/pos['risk'] - cost_pips*pip/pos['risk']
                res.append(dict(t=pos['t'],d=d,R=r,why=ex[1])); pos=None; lastx=b['tc']; continue
        if pos: continue
        if start and b['t']<start: continue
        if lastx and (b['tc']-lastx).total_seconds()<cool*3600: continue
        a=atr.get(b['day']); s=sma.get(b['day'],{}).get(trlen)
        if a is None: continue
        bb=bias.get(iso,('-','-'))[0]
        bd=1 if bb=='U' else -1 if bb=='D' else 0
        td=0 if s is None else (1 if b['c']>s else -1)
        dr=bd if dirm=='bias' else td if dirm=='trend' else (bd if bd==td else 0)
        if dr==0: continue
        if b['dow']>4 or (noFri and b['dow']==4): continue
        if cf=='wtd' and not ((b['c']-wko)*dr>0): continue
        e=b['c']; risk=k*a; pos=dict(i=i,t=b['tc'],d=dr,e=e,sl=e-dr*risk,tp=(e+dr*tp*risk) if tp else None,risk=risk,atr=a)
    return res
def summ(r):
    n=len(r); s=sum(x['R'] for x in r); w=sum(x['R']>0 for x in r)
    return n,s,(w/n if n else 0)
if __name__=='__main__':
    path,pair=sys.argv[1],sys.argv[2]
    bars=load(path); atr,sma=daily(bars); bias=bias_for(pair)
    start=D.datetime(2026,9,27,21,tzinfo=D.timezone.utc)
    base=run(bars,atr,sma,bias,pair,cf='none',start=start)
    print('replica of the export (bias, no confirmation, 1xATR, TP2, 4d):',summ(base))
    for t in base: print('  ',t['t'].strftime('%a %d %b %H:%M'),'short' if t['d']<0 else 'long',f"{t['R']:+.2f}",t['why'])
