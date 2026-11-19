import re
# take the overnight template structure (head styles, HUD, script engine) and swap the scenes
TIP=lambda s:f'<div data-in="@{s[0]}" class="card" style="font-size:36px;line-height:1.35;font-weight:600;border-color:rgba(217,163,91,.35)">💡 {s[1]}</div>'
def head(t,sub): return f'<div data-in="0.05"><div class="day" style="font-size:140px">{t}</div><div class="dsub">{sub}</div></div>'
def mover(c,a,b,col,note,at):
    return f'<div class="card" data-in="{at}" data-sfx="pop" style="display:flex;align-items:center;gap:24px;padding:26px 30px"><div class="num" style="font-size:64px;width:150px">{c}</div><div style="flex:1"><div class="num" style="font-size:58px;color:{col}">{a} → {b}</div><div style="font-size:26px;color:var(--sub);margin-top:6px">{note}</div></div></div>'
def ev(day,time,title,sub,at): return f'<div class="card" data-in="{at}" data-sfx="pop" style="display:flex;align-items:center;gap:24px;padding:22px 28px"><div style="width:190px"><div class="num" style="font-size:40px;color:var(--crema)">{day}</div><div style="font-size:24px;color:var(--sub)">{time}</div></div><div><div class="h" style="font-size:40px">{title}</div><div style="font-size:24px;color:var(--sub)">{sub}</div></div></div>'
S={}
S['mood']=head('RISK MOOD','How nervous are markets?')+'''
 <div class="card" data-in="@1" data-sfx="pop"><div class="lbl">OUR RISK GAUGE · −2 SCARED TO +2 CALM</div><div style="display:flex;align-items:baseline;gap:30px;margin-top:10px"><div class="num" style="font-size:120px;color:var(--bear)">−2</div><div class="num" style="font-size:70px;color:var(--sub)">→</div><div class="num" style="font-size:150px;color:var(--cream)" data-reveal="@1+1.4" data-sfx="hit">0</div></div><div style="font-size:28px;color:var(--sub)">last week → next week</div></div>
 <div style="display:grid;grid-template-columns:1fr 1fr;gap:22px">
  <div class="card" data-in="@2" data-sfx="pop"><div class="lbl">S&amp;P 500 · 4 WEEKS</div><div class="num" style="font-size:84px;margin:8px 0"><span data-sign data-count="0|-1.28|@2+0.3|1.4|2">0</span>%</div><div style="font-size:24px;color:var(--sub)">not a sell-off</div></div>
  <div class="card" data-in="@2+2.6" data-sfx="pop"><div class="lbl">VIX · FEAR INDEX</div><div class="num" style="font-size:84px;margin:8px 0"><span data-count="25.6|19.3|@2+2.9|1.4|1">25.6</span></div><div style="font-size:24px;color:var(--sub)">normal zone (15–25)</div></div>
 </div>'''+TIP((3,'Calm markets = safe havens (franc, yen, gold) lose their extra support.'))
S['dollar']=head('DOLLAR','Still number one · score +5')+'''
 <div class="card" data-in="@1" data-sfx="pop"><div class="lbl">US INFLATION · OCTOBER (MONTH)</div><div style="display:flex;align-items:baseline;gap:26px;margin-top:8px"><div class="num" style="font-size:130px;color:var(--bull)">+<span data-count="0|0.4|@1+0.4|1.2|1">0</span>%</div><div style="font-size:32px;color:var(--sub)">vs +0.3% expected</div></div><div data-in="@1+2.4" data-sfx="tick" style="margin-top:12px;padding:8px 14px;border-radius:12px;background:rgba(61,220,151,.14);color:#7FEAB8;font-weight:700;font-size:26px;display:inline-block">Core prices +0.3% vs +0.2%</div></div>
 <div class="card" data-in="@2" data-sfx="pop"><div class="lbl">DECEMBER FED HIKE · PRICED</div><div class="num" style="font-size:120px;color:var(--bull);margin-top:6px">~<span data-count="0|91|@2+0.3|1.4">0</span>%</div></div>'''+TIP((3,'Higher US rates make the dollar more attractive to hold.'))
S['winners']=head('WINNERS','Last week → next week')+mover('GBP','−3','+1','var(--bull)','risk drag gone · BoE may hike in Dec','@1')+mover('AUD','0','+3','var(--bull)','highest interest rate of the eight (4.85%)','@2')+mover('NZD','−3','+1','var(--bull)','dairy prices up ~5.6% in two auctions','@3')+TIP(('3+3','Calm markets reward currencies that pay more.'))
S['losers']=head('LOSERS','Last week → next week')+mover('CHF','0','−3','var(--bear)','pays 0% · no need to hide','@1')+mover('JPY','+2','0','var(--bear)','haven bonus gone · Tokyo still warns','@2')+mover('CAD','−6','−4','var(--crema)','still last · oil −13% in 4 weeks','@3')+TIP(('3+4','Cheaper oil hurts Canada: oil is its biggest export.'))
S['gold']=head('GOLD','Its own score turned negative')+'''
 <div class="card" data-in="@1" data-sfx="pop"><div class="lbl">GOLD FACTOR</div><div style="display:flex;align-items:baseline;gap:30px;margin-top:8px"><div class="num" style="font-size:120px;color:var(--bull)">+7</div><div class="num" style="font-size:70px;color:var(--sub)">→</div><div class="num" style="font-size:150px;color:var(--bear)" data-reveal="@1+0.8" data-sfx="hit">−3</div></div></div>
 <div class="card" data-in="@2" data-sfx="pop"><div class="lbl">US 10-YEAR REAL YIELD · 4 WEEKS</div><div class="num" style="font-size:110px;color:var(--bear);margin-top:6px"><span data-count="2.74|2.86|@2+0.4|1.6|2">2.74</span>%</div><div style="font-size:26px;color:var(--sub)">from 2.74% (16 Oct)</div></div>'''+TIP((3,'Gold pays no interest. Central banks still buying (China +26 tonnes in Oct).'))
S['board']='''<div data-in="0.05"><div class="day" style="font-size:130px">THE BOARD</div><div class="dsub">Week 47 · scores from −18 to +18</div></div>
 <div class="card" data-in="@0+0.8" style="display:flex;flex-direction:column;gap:12px;padding:26px 30px" id="bars"></div>'''
S['pairs']=head('WIDEST GAPS','Fundamental lean, not a signal')+''.join(
 f'<div class="card" data-in="{at}" data-sfx="pop" style="display:flex;align-items:center;justify-content:space-between;padding:26px 32px"><div><div class="num" style="font-size:62px">{p}</div><div style="font-size:26px;color:var(--sub);margin-top:6px">{s}</div></div><div class="num" style="font-size:90px;color:{c}">{g}</div></div>'
 for p,s,g,c,at in [('USD/CAD','bullish · low conviction','+9','var(--bull)','@1'),('USD/CHF','bullish · medium conviction','+8','var(--bull)','@2'),('EUR/USD','bearish · medium conviction','−8','var(--bear)','@3')])
S['week']=head('NEXT WEEK','16–20 Nov · times in GMT')+ev('MON','13:30','Canada CPI','inflation · CAD','@1')+ev('TUE–WED','07:00','UK jobs &amp; UK CPI','GBP · plus US retail sales Tue 13:30','@2')+ev('WED','19:00','Fed minutes','USD · notes from the October meeting','@2+3.2')+ev('THU / FRI','00:30 Thu','Australia jobs · Japan CPI','AUD · JPY','@3')
src=open('template.html').read()
start=src.index('<section class="sc" id="fed">'); end=src.index('<section class="sc" id="outro"')
body=''.join(f'<section class="sc" id="{k}">\n {v}\n</section>\n' for k,v in S.items())
out=src[:start]+body+src[end:]
out=out.replace('../../node_modules','./node_modules')
out=out.replace("const IDS=['hook','fed','yields','euro','yen','oil','gold','verdict','today','outro'];","const IDS=['hook','mood','dollar','winners','losers','gold','board','pairs','week','outro'];")
out=re.sub(r"const CHIPS=\{.*?\};","const CHIPS={mood:'ALL 8',dollar:'USD',winners:'GBP AUD<br>NZD',losers:'CHF JPY<br>CAD',gold:'XAU',board:'WEEK 47',pairs:'TOP 3',week:'16–20<br>NOV'};",out)
out=out.replace("const SC8=[['USD',7],['JPY',2],['CHF',0],['AUD',0],['EUR',-3],['GBP',-3],['NZD',-3],['CAD',-6]];","const SC8=[['USD',5],['AUD',3],['GBP',1],['NZD',1],['JPY',0],['EUR',-3],['CHF',-3],['CAD',-4]];")
out=out.replace("T(sc,'@2')-i*0.12","T(sc,'@1')-i*0.12").replace("Math.abs(v)/8*50*p","Math.abs(v)/6*50*p")
# hook text
out=out.replace('>OVERNIGHT</div>','>NEXT WEEK</div>').replace('FX CHECK · FRI 13 NOV','FX WEEK AHEAD · 16–20 NOV')
out=out.replace("fillText('Index at a 19-month high',190,top+108)","fillText('Still on top · +5',190,top+108)").replace("emblem(c,120,bot-70,'€','#F0616D')","emblem(c,120,bot-70,'₣','#F0616D')")
out=out.replace("fillText('THE REST',232,bot-74)","fillText('THE FRANC',232,bot-74)").replace("fillText('Waiting for a reason',190,bot-34)","fillText('Lost its shelter · −3',190,bot-34)")
out=out.replace('<div id="pairT">FX CHECK</div>','<div id="pairT">WEEK 47</div>').replace('OVERNIGHT · FRI 13 NOV</div>','WEEK AHEAD · 16–20 NOV</div>').replace('<div id="chip">FRIDAY<br>MORNING</div>','<div id="chip">ALL 8</div>')
out=out.replace("const FOLLOW=[['euro',6.5,10.5,8.4]];","const FOLLOW=[['winners',6.5,10.5,8.4]];")
out=out.replace("sc==='fed'&&t<TR","sc==='mood'&&t<TR").replace("const ck=sc==='outro'?'today':sc;","const ck=sc==='outro'?'week':sc;")
out=out.replace("(sc==='verdict'||sc==='outro'||sc==='today'||sc==='euro')?'1500px':'1290px'","(sc==='board'||sc==='outro'||sc==='week'||sc==='winners'||sc==='losers'||sc==='pairs')?'1560px':'1290px'")
out=out.replace('The big picture, every morning','The big picture, every week')
open('scenes.html','w').write(out)
print('ok', 'verdict' in out)
