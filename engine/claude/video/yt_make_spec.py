# yt_make_spec.py v1.1 (14 Nov 2026): screen data now comes from the episode spec when present
# (REGIME, STAMP, THEMES, COLD_ICONS, GUIDE_EX, RANK, TOP, TOP_POP, TWO, DAYS, SCEN, SUBS); W46 pilot values remain the fallback.
import json
import spec as SP
from spec import *
g=lambda n,d: getattr(SP,n,d)
ccy=[]
for c in CCY:
    d={k:c[k] for k in ('id','code','name','sym','col','ch','score','prev','f','vo','up','down','pairs')}
    d['gold']=c.get('gold',False); d['cards']={str(k):v for k,v in c['cards'].items()}; d['flip']=c.get('flip',5); ccy.append(d)
S=dict(week=WEEK,dates=DATES,order=ORDER,fn=list(FN.values()),gn=list(GN.values()),ccy=ccy,cold=INTRO['cold'],
 regime=g('REGIME',[('S&P 500 · 4 weeks',-5.56,'stocks falling',0,2,'%'),('VIX fear index',25.6,'above 25 = nervous',15,1,''),('Credit spreads · 4 weeks',37,'basis points wider',0,0,'bp')]),
 themes=g('THEMES',[('🏦','Fed may hike again'),('📉','France budget stress'),('🛢️','Oil −6% in 4 weeks')]),
 rank=g('RANK',[('USD',7),('JPY',2),('CHF',0),('AUD',0),('EUR',-3),('GBP',-3),('NZD',-3),('CAD',-6)]),
 top=g('TOP',[('USD/CAD',13),('EUR/USD',-10),('GBP/USD',-10),('NZD/USD',-10)]),two=g('TWO',['EUR/GBP','EUR/NZD','GBP/NZD','AUD/CHF']),
 days=g('DAYS',[('Mon 9 Nov',[('China CPI & PPI','time not verified','MEDIUM','0+1.5')]),
       ('Tue 10 Nov',[('US CPI','13:30 GMT','HIGH','1+0.5'),('BoJ opinions','Tokyo morning','MEDIUM','1+3.5'),('BoC minutes','time not verified','MEDIUM','1+4.5')]),
       ('Wed 11 Nov',[('OPEC oil report','time not verified','MEDIUM','2+0.2'),('US/Canada holiday','bond markets shut','LOW','2+0.4')]),
       ('Thu 12 Nov',[('UK Q3 GDP','07:00 GMT','HIGH','2+0.6')]),
       ('Fri 13 Nov',[('US PPI','13:30 GMT','MEDIUM','2+3.0'),('Euro-area GDP','10:00 GMT','MEDIUM','2+4.0'),('Ratings DE / IT','late','MEDIUM','2+4.6')])]),
 colors=dict(cold='#D9A35B',title='#D9A35B',big=g('BIG_COL','#F0616D'),guide='#D9A35B',rank='#D9A35B',week='#5B8DEF',outro='#E5322D',**{c['id']:c['col'] for c in CCY}),
 chips=dict(big='THE BIG PICTURE',guide='HOW TO READ',rank='RANKING',week='WEEK AHEAD',**{c['id']:(f"CH {c['ch']} · {c['code']}" if not c.get('gold') else 'BONUS · XAU') for c in CCY}),
 subs=g('SUBS',[('guide','@3+2.5'),('jpy','@3'),('rank','@3+3')]))
for k,n in (('stamp','STAMP'),('coldIcons','COLD_ICONS'),('guideEx','GUIDE_EX'),('scen','SCEN'),('topPop','TOP_POP')):
    v=g(n,None)
    if v is not None: S[k]=v
json.dump(S,open('spec.json','w'),ensure_ascii=False)
print('ok')
