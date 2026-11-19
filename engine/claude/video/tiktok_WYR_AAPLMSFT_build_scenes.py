import re
TIP=lambda a,t:f'<div data-in="{a}" class="card" style="font-size:34px;line-height:1.35;font-weight:600;border-color:rgba(217,163,91,.35)">💡 {t}</div>'
def ctx(t,s): return f'<div data-in="0.05"><div class="h" style="font-size:84px">{t}</div><div class="dsub">{s}</div></div>'
def opt(L,title,sub,at,col,extra='',res=None,rc=None,rid=''):
    r=f'<div class="num" style="font-size:96px;color:{rc};margin-top:10px" {rid}>{res}</div>' if res else ''
    return f'<div class="card" data-in="{at}" data-sfx="pop" style="display:flex;gap:22px;align-items:flex-start;padding:32px 30px;border-color:{col};border-width:3px"><div class="num" style="font-size:110px;color:{col};width:84px">{L}</div><div style="flex:1"><div class="h" style="font-size:58px">{title}</div><div style="font-size:31px;color:var(--sub);margin-top:6px;line-height:1.3">{sub}</div>{r}</div>{extra}</div>'
TIMER='''<div data-timer style="display:flex;align-items:center;gap:30px;justify-content:center;opacity:0">
 <svg width="250" height="250" viewBox="0 0 200 200"><circle cx="100" cy="100" r="80" stroke="rgba(234,219,196,.15)" stroke-width="14" fill="none"/><circle class="tring" cx="100" cy="100" r="80" stroke="#D9A35B" stroke-width="14" fill="none" stroke-linecap="round" stroke-dasharray="502.7" transform="rotate(-90 100 100)"/><text class="tnum" x="100" y="128" text-anchor="middle" font-family="SG" font-weight="700" font-size="92" fill="#EADBC4">3</text></svg>
 <div><div class="h" style="font-size:64px">💬 Comment</div><div class="h" style="font-size:64px;color:var(--crema)">A or B</div></div></div><div data-pausehint style="opacity:0;text-align:center;font-size:36px;font-weight:600;color:var(--cream);background:rgba(217,163,91,.16);border:2px solid rgba(217,163,91,.45);border-radius:18px;padding:16px 20px">⏸️ Need more time? <b>Pause</b> &amp; comment your answer 👇</div>'''
A='#EADBC4'; Bc='#D9A35B'
FVG='<svg width="190" height="190" viewBox="0 0 150 150"><rect x="10" y="62" width="130" height="30" fill="rgba(217,163,91,.3)"/><g stroke="#3DDC97" stroke-width="4"><line x1="30" y1="85" x2="30" y2="125"/><line x1="75" y1="30" x2="75" y2="130"/><line x1="120" y1="15" x2="120" y2="70"/></g><rect x="20" y="92" width="20" height="25" fill="#3DDC97"/><rect x="63" y="40" width="24" height="80" fill="#3DDC97"/><rect x="110" y="22" width="20" height="40" fill="#3DDC97"/></svg>'
OB='<svg width="190" height="190" viewBox="0 0 150 150"><rect x="14" y="78" width="40" height="52" fill="none" stroke="#D9A35B" stroke-width="4" stroke-dasharray="6 5"/><g stroke-width="4"><line x1="34" y1="75" x2="34" y2="135" stroke="#F0616D"/><line x1="80" y1="40" x2="80" y2="125" stroke="#3DDC97"/><line x1="122" y1="10" x2="122" y2="60" stroke="#3DDC97"/></g><rect x="24" y="85" width="20" height="38" fill="#F0616D"/><rect x="69" y="48" width="22" height="70" fill="#3DDC97"/><rect x="111" y="18" width="22" height="36" fill="#3DDC97"/></svg>'
S={}
S['hook']="""<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0;padding-bottom:300px">
 <div class="day pop" data-pop="0.05" style="font-size:230px;line-height:.95">WOULD</div>
 <div class="day pop" data-pop="0.32" style="font-size:230px;line-height:.95">YOU</div>
 <div class="day pop" data-pop="0.6" style="font-size:210px;line-height:.95;color:var(--crema)">RATHER?</div>
 <div class="pop" data-pop="1.0" style="margin-top:40px;padding:14px 30px;border-radius:16px;background:var(--cream);color:#120D0A;font-family:SG;font-weight:700;font-size:44px;letter-spacing:3px">TRADING EDITION</div></div>"""
S['q1']=ctx('$1,000 · 10 years ago','Bought end of Nov 2016 · held to 13 Nov 2026')+opt('A','Apple','the iPhone company','@0+0.6',A)+opt('B','Microsoft','Windows, Office, cloud','@0+1.4',Bc)+TIMER
RACE="""<div class="card" data-in="0.3" style="display:flex;gap:40px;justify-content:center;align-items:flex-end;height:760px;padding:30px 40px">
 <div style="display:flex;flex-direction:column;align-items:center;gap:14px;width:300px"><div class="num" id="vA" style="white-space:nowrap;font-size:60px;color:var(--cream)">$1,000</div><div id="bA" style="width:200px;border-radius:18px 18px 6px 6px;background:var(--cream);height:40px"></div><div class="h" style="font-size:44px">A · Apple</div></div>
 <div style="display:flex;flex-direction:column;align-items:center;gap:14px;width:300px"><div class="num" id="vB" style="white-space:nowrap;font-size:60px;color:var(--crema)">$1,000</div><div id="bB" style="width:200px;border-radius:18px 18px 6px 6px;background:var(--crema);height:40px"></div><div class="h" style="font-size:44px">B · Microsoft</div></div></div>"""
S['r1']=ctx('The race','$1,000 each · dividends reinvested')+RACE
S['r2']=ctx('One decision','Same $1,000 · same 10 years')+"""<div class="card" data-in="@0+0.4" data-sfx="pop" style="text-align:center"><div class="lbl">APPLE VS MICROSOFT</div><div class="num" style="font-size:150px;color:var(--bull);margin:10px 0"><span data-reveal="@1" data-sfx="hit">≈ $4,300</span></div><div style="font-size:32px;color:var(--sub)">apart</div></div>
 <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px"><div class="card" data-in="@1+1.6"><div class="lbl">APPLE</div><div class="num" style="font-size:64px;margin-top:6px">≈ 14×</div></div><div class="card" data-in="@1+2.0"><div class="lbl">MICROSOFT</div><div class="num" style="font-size:64px;margin-top:6px;color:var(--crema)">≈ 9.7×</div></div></div>"""+TIP('@2','Prices adjusted for splits &amp; dividends. Past results don’t promise future ones.')
src=open('template.html').read()
start=src.index('<section class="sc" id="hook"'); end=src.index('<section class="sc" id="outro"')
out=src[:start]+''.join(f'<section class="sc" id="{k}">\n {v}\n</section>\n' for k,v in S.items())+src[end:]
# outro: loop line
out=out.replace('<div style="font-size:28px;color:var(--sub);margin-top:24px" data-in="@1">Big picture only. Not a trade signal.</div>','<div style="font-size:28px;color:var(--sub);margin-top:10px" data-in="0.9">Big picture only. Not a trade signal.</div><div class="h" data-reveal="@1" style="font-size:66px;color:var(--crema);margin-top:30px;line-height:1.1">Now that you know…<br>would you rather?</div>')
out=out.replace('<div style="font-size:34px;color:var(--sub)" data-in="0.9">The big picture, every morning</div>','')
out=out.replace('../../node_modules','./node_modules')
out=out.replace("const IDS=['hook','fed','yields','euro','yen','oil','gold','verdict','today','outro'];","const IDS=['hook','q1','r1','r2','outro'];")
out=re.sub(r"const CHIPS=\{.*?\};","const CHIPS={q1:'STOCKS',r1:'STOCKS',r2:'STOCKS'};",out)
out=re.sub(r"const SC8=.*?;\ndocument.getElementById\('bars'\).innerHTML=.*?\n","",out,flags=re.S)
out=out.replace('<div id="pairT">FX CHECK</div>','<div id="pairT" style="font-size:96px">WOULD YOU<br>RATHER?</div>').replace('<div style="font-size:26px;color:var(--sub);letter-spacing:3px;font-weight:600;margin-top:6px">OVERNIGHT · FRI 13 NOV</div>','<div style="font-size:26px;color:var(--sub);letter-spacing:3px;font-weight:600;margin-top:6px">TRADING EDITION</div>').replace('<div id="chip">FRIDAY<br>MORNING</div>','<div id="chip">STOCKS</div>')
out=out.replace("const FOLLOW=[['euro',6.5,10.5,8.4]];","const FOLLOW=[];")
out=out.replace("sc==='fed'&&t<TR","false").replace("const ck=sc==='outro'?'today':sc;","const ck=sc==='outro'?'r2':sc;")
out=out.replace("(sc==='verdict'||sc==='outro'||sc==='today'||sc==='euro')?'1500px':'1290px'","'1500px'")
out=out.replace("const showPair=!(sc==='hook'||sc==='outro');","const showPair=sc!=='outro';")
out=out.replace("S.querySelectorAll('.bar')","S.querySelectorAll('.barX')")
out=out.replace("if(sc==='hook')drawHook(t);","""S.querySelectorAll('[data-timer]').forEach(el=>{const s=TIM[sc].lead+TIM[sc].len+0.2;const k=t-s;el.style.opacity=ease(k/0.3);el.style.transform='scale('+(0.9+0.1*ease(k/0.3))+')';const n=Math.max(1,Math.min(3,3-Math.floor(Math.max(0,k))));el.querySelector('.tnum').textContent=k>=3?'✓':n;el.querySelector('.tring').setAttribute('stroke-dashoffset',502.7*Math.min(1,Math.max(0,k)/3))});""")
out=out.replace("if(sc==='hook')out.push({t:0.15,type:'swell'},{t:0.3,type:'hit'});","if(sc[0]==='q'){const s=TIM[sc].lead+TIM[sc].len+0.2;out.push({t:s,type:'tick'},{t:s+1,type:'tick'},{t:s+2,type:'tick'},{t:s+3,type:'ding'})}if(sc==='outro')out.push({t:T('outro','@1'),type:'hit'});")
# hide the old outro swell/click-follow ding timing (keep), captions: hide during outro second line? keep
out=out.replace("S.querySelectorAll('[data-timer]')",open('race.js').read()+"S.querySelectorAll('[data-timer]')",1)
out=out.replace("if(sc[0]==='q'){",open('cues.js').read()+"if(sc[0]==='q'){",1)
out=out.replace("const showPair=sc!=='outro';","const showPair=sc!=='outro'&&sc!=='hook';")
out=out.replace("S.querySelectorAll('[data-timer]')","S.querySelectorAll('[data-pop]').forEach(el=>{const p=cl((t-(+el.dataset.pop))/0.38);const k=1.70158*1.6;const e=p<=0?0:1+(k+1)*Math.pow(p-1,3)+k*Math.pow(p-1,2);el.style.opacity=cl(p*3);el.style.transform='scale('+(0.2+0.8*e)+') rotate('+((1-cl(p))*-6)+'deg)';el.style.filter='blur('+(1-cl(p*1.5))*12+'px)'});if(sc==='hook'){const g=1+0.03*Math.sin(t*9)*Math.exp(-Math.max(0,t-0.9)*2);S.firstElementChild.style.transform='scale('+g+')'}S.querySelectorAll('[data-timer]')",1)
out=out.replace("if(sc[0]==='q'){","if(sc==='hook'){out.push({t:0.0,type:'swell'});[0.05,0.32,0.6].forEach(x=>out.push({t:x,type:'hit'}));out.push({t:1.0,type:'pop'})}if(sc[0]==='q'){",1)
out=out.replace("if(sc==='hook'){el.style.fontSize","if(sc==='hook'){el.innerHTML='';return;el.style.fontSize",1)
oa=out.index('<section class="sc" id="outro"'); ob=out.index('</section>',oa)+len('</section>')
out=out[:oa]+"""<section class="sc" id="outro" style="justify-content:center;align-items:center;padding:200px 130px 420px 130px"><div style="display:flex;flex-direction:column;align-items:center;gap:26px;text-align:center"><div class="day pop" data-pop="0.4" style="font-size:124px;line-height:.95;white-space:nowrap">NOW THAT</div><div class="day pop" data-pop="0.75" style="font-size:124px;line-height:.95;white-space:nowrap;color:var(--crema)">YOU KNOW…</div><div style="font-size:26px;color:var(--sub);margin-top:30px" data-in="1.2">Not a trade signal.</div><div id="obtn" style="display:none"><span id="otxt"></span></div></div></section>"""+out[ob:]
out=out.replace("if(sc==='outro')out.push({t:0.2,type:'swell'},{t:T('outro','@0')+2.6,type:'click'},{t:T('outro','@0')+2.65,type:'ding'});","if(sc==='outro')out.push({t:0.4,type:'hit'},{t:0.75,type:'hit'});")
out=out.replace("if(sc==='outro')out.push({t:T('outro','@1'),type:'hit'});","")
out=out.replace("if(sc==='outro'){const tap=","if(false){const tap=")
out=out.replace("S.querySelectorAll('[data-timer]')","S.querySelectorAll('[data-pausehint]').forEach(el=>{const s=TIM[sc].lead+TIM[sc].starts[2]-0.1;el.style.opacity=ease((t-s)/0.4)});S.querySelectorAll('[data-timer]')",1)
open('scenes.html','w').write(out); print('ok')
