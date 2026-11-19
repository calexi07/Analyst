import re
TIP=lambda a,t:f'<div data-in="{a}" class="card" style="font-size:36px;line-height:1.35;font-weight:600;border-color:rgba(217,163,91,.35)">💡 {t}</div>'
def head(t,sub,fs=140): return f'<div data-in="0.05"><div class="day" style="font-size:{fs}px">{t}</div><div class="dsub">{sub}</div></div>'
def row(ic,t,s,at): return f'<div class="card" data-in="{at}" data-sfx="pop" style="display:flex;align-items:center;gap:24px;padding:22px 28px"><div style="font-size:60px;width:80px;text-align:center">{ic}</div><div><div class="h" style="font-size:44px">{t}</div><div style="font-size:24px;color:var(--sub)">{s}</div></div></div>'
S={}
S['what']=head('WHAT IS IT?','Fundamental analysis in one line')+'<div style="display:grid;grid-template-columns:1fr 1fr;gap:18px">'+''.join(f'<div class="card" data-in="{a}" data-sfx="pop" style="padding:26px"><div style="font-size:60px">{i}</div><div class="h" style="font-size:40px;margin-top:8px">{t}</div></div>' for i,t,a in [('🏦','Interest rates','@2'),('📈','Inflation','@2+1.0'),('👷','Jobs &amp; growth','@2+2.0'),('🏛️','Politics','@2+3.0')])+'</div>'+TIP('@3','A currency = a share in a country’s economy.')
S['rates']=head('RATES','Money follows the yield')+'''<div style="display:grid;grid-template-columns:1fr 1fr;gap:22px">
 <div class="card" data-in="@2" data-sfx="pop"><div class="lbl">CURRENCY A</div><div class="num" style="font-size:120px;color:var(--bull);margin-top:8px"><span data-count="0|4|@2+0.3|1.2">0</span>%</div><div style="font-size:26px;color:var(--sub)">pays interest</div></div>
 <div class="card" data-in="@2+1.2" data-sfx="pop"><div class="lbl">CURRENCY B</div><div class="num" style="font-size:120px;color:var(--bear);margin-top:8px">0%</div><div style="font-size:26px;color:var(--sub)">pays nothing</div></div></div>
 <div class="h" style="font-size:64px;text-align:center" data-reveal="@2+3.5" data-sfx="hit">Money → A</div>'''+TIP('@3','Every central bank meeting can change this.')
S['surprise']=head('SURPRISES','Only the unexpected moves price')+'''
 <div class="card" data-in="@2" data-sfx="pop"><div class="lbl">PRICED IN</div><div class="h" style="font-size:44px;margin-top:8px">What everyone expects is already in the price</div></div>
 <div class="card" data-in="@3" data-sfx="pop"><div class="lbl">EXAMPLE · US INFLATION, OCTOBER 2026</div><div style="display:flex;gap:40px;align-items:baseline;margin-top:10px"><div><div style="font-size:26px;color:var(--sub)">forecast</div><div class="num" style="font-size:90px">+0.3%</div></div><div><div style="font-size:26px;color:var(--sub)">actual</div><div class="num" style="font-size:90px;color:var(--bull)" data-reveal="@3+1.6" data-sfx="hit">+0.4%</div></div></div><div data-in="@3+3.5" data-sfx="tick" style="margin-top:12px;padding:8px 14px;border-radius:12px;background:rgba(61,220,151,.14);color:#7FEAB8;font-weight:700;font-size:26px;display:inline-block">Surprise → stronger dollar</div></div>'''
S['mood']=head('RISK MOOD','Fear vs calm')+'''<div style="display:grid;grid-template-columns:1fr 1fr;gap:22px">
 <div class="card" data-in="@1" data-sfx="pop" style="border-color:rgba(240,97,109,.4)"><div class="lbl">😨 SCARED</div><div class="h" style="font-size:42px;margin-top:10px;line-height:1.3">Swiss franc<br>Yen<br>Gold</div><div style="font-size:24px;color:var(--sub);margin-top:8px">safe havens</div></div>
 <div class="card" data-in="@2" data-sfx="pop" style="border-color:rgba(61,220,151,.4)"><div class="lbl">😌 CALM</div><div class="h" style="font-size:42px;margin-top:10px;line-height:1.3">Aussie dollar<br>Kiwi dollar</div><div style="font-size:24px;color:var(--sub);margin-top:8px">higher yield</div></div></div>'''+TIP('@3','Same news, different mood, different reaction.')
S['tug']=head('A PAIR','= a tug of war')+'''
 <div class="card" data-in="@1" data-sfx="pop" style="display:flex;align-items:center;justify-content:space-between;padding:34px 36px"><div style="text-align:center"><div class="num" style="font-size:80px">EUR</div><div class="num" style="font-size:56px;color:var(--bear);margin-top:6px">−3</div></div><div style="font-size:70px">⇄</div><div style="text-align:center"><div class="num" style="font-size:80px">USD</div><div class="num" style="font-size:56px;color:var(--bull);margin-top:6px">+5</div></div></div>
 <div class="card" data-in="@2" data-sfx="pop"><div class="lbl">GAP = BASE − QUOTE</div><div class="num" style="font-size:110px;color:var(--bear);margin-top:6px">−8</div><div style="font-size:26px;color:var(--sub)">fundamentals lean to the dollar (our Week 47 scores)</div></div>'''
S['proof']=head('DOES IT WORK?','Our model · Week 46 (9–13 Nov)',104)+'''
 <div class="card" data-in="@1" data-sfx="pop"><div class="lbl">US DOLLAR PAIRS</div><div class="num" style="font-size:120px;color:var(--bull);margin-top:6px"><span data-count="0|7|@1+0.4|1.2">0</span> / 7</div><div style="font-size:26px;color:var(--sub)">moved the way fundamentals pointed</div></div>
 <div class="card" data-in="@2" data-sfx="pop"><div class="lbl">SWISS FRANC PAIRS</div><div class="num" style="font-size:80px;color:var(--bear);margin-top:6px">missed</div><div style="font-size:26px;color:var(--sub)">the mood changed after the forecast</div></div>'''+TIP('@3','One week proves nothing. We judge after 26 weeks.')
S['limits']=head('WHAT IT ISN’T','Know the job of each tool',120)+row('🧭','Fundamentals','the direction of pressure','@2')+row('📊','Chart','the timing','@2+2.6')+row('🛡️','Risk management','how much','@3')+TIP('@1','Not a timing tool. Not a trade signal.')
S['recap']=head('REMEMBER','Three things')+row('1','Rates move money','','@1')+row('2','Surprises move prices','','@2')+row('3','Mood can flip the story','','@3')
src=open('template.html').read()
start=src.index('<section class="sc" id="fed">'); end=src.index('<section class="sc" id="outro"')
out=src[:start]+''.join(f'<section class="sc" id="{k}">\n {v}\n</section>\n' for k,v in S.items())+src[end:]
out=out.replace('../../node_modules','./node_modules')
out=out.replace("const IDS=['hook','fed','yields','euro','yen','oil','gold','verdict','today','outro'];","const IDS=['hook','what','rates','surprise','mood','tug','proof','limits','recap','outro'];")
out=re.sub(r"const CHIPS=\{.*?\};","const CHIPS={what:'BASICS',rates:'LESSON 1',surprise:'LESSON 2',mood:'LESSON 3',tug:'LESSON 4',proof:'OUR MODEL',limits:'LIMITS',recap:'RECAP'};",out)
out=re.sub(r"const SC8=.*?;\ndocument.getElementById\('bars'\).innerHTML=.*?\n","",out,flags=re.S)
out=out.replace('>OVERNIGHT</div>','>WHY</div>').replace('FX CHECK · FRI 13 NOV','FUNDAMENTALS MATTER IN FOREX')
out=out.replace("fillText('DOLLAR',232,top+68)","fillText('FUNDAMENTALS',232,top+68)").replace("fillText('Index at a 19-month high',190,top+108)","fillText('tell you why',190,top+108)")
out=out.replace("emblem(c,120,bot-70,'€','#F0616D')","emblem(c,120,bot-70,'?','#F0616D')").replace("fillText('THE REST',232,bot-74)","fillText('CHARTS ALONE',232,bot-74)").replace("fillText('Waiting for a reason',190,bot-34)","fillText('show only where',190,bot-34)")
out=out.replace('<div id="pairT">FX CHECK</div>','<div id="pairT">FX 101</div>').replace('OVERNIGHT · FRI 13 NOV</div>','FUNDAMENTAL ANALYSIS</div>').replace('<div id="chip">FRIDAY<br>MORNING</div>','<div id="chip">BASICS</div>')
out=out.replace("const FOLLOW=[['euro',6.5,10.5,8.4]];","const FOLLOW=[['rates',6.5,10.5,8.4]];")
out=out.replace("sc==='fed'&&t<TR","sc==='what'&&t<TR").replace("const ck=sc==='outro'?'today':sc;","const ck=sc==='outro'?'recap':sc;")
out=out.replace("(sc==='verdict'||sc==='outro'||sc==='today'||sc==='euro')?'1500px':'1290px'","'1480px'")
out=out.replace("S.querySelectorAll('.bar')","S.querySelectorAll('.barX')")
out=out.replace('The big picture, every morning','The big picture, every week')
open('scenes.html','w').write(out); print('ok')
