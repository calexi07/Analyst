import re
TIP=lambda a,t:f'<div data-in="{a}" class="card" style="font-size:34px;line-height:1.35;font-weight:600;border-color:rgba(217,163,91,.35)">💡 {t}</div>'
def ctx(t,s): return f'<div data-in="0.05"><div class="h" style="font-size:84px">{t}</div><div class="dsub">{s}</div></div>'
def opt(L,title,sub,at,col,extra='',res=None,rc=None,rid=''):
    r=f'<div class="num" style="font-size:96px;color:{rc};margin-top:10px" {rid}>{res}</div>' if res else ''
    return f'<div class="card" data-in="{at}" data-sfx="pop" style="display:flex;gap:22px;align-items:flex-start;padding:32px 30px;border-color:{col};border-width:3px"><div class="num" style="font-size:110px;color:{col};width:84px">{L}</div><div style="flex:1"><div class="h" style="font-size:58px">{title}</div><div style="font-size:31px;color:var(--sub);margin-top:6px;line-height:1.3">{sub}</div>{r}</div>{extra}</div>'
TIMER='''<div data-timer style="display:flex;align-items:center;gap:30px;justify-content:center;opacity:0">
 <svg width="250" height="250" viewBox="0 0 200 200"><circle cx="100" cy="100" r="80" stroke="rgba(234,219,196,.15)" stroke-width="14" fill="none"/><circle class="tring" cx="100" cy="100" r="80" stroke="#D9A35B" stroke-width="14" fill="none" stroke-linecap="round" stroke-dasharray="502.7" transform="rotate(-90 100 100)"/><text class="tnum" x="100" y="128" text-anchor="middle" font-family="SG" font-weight="700" font-size="92" fill="#EADBC4">3</text></svg>
 <div><div class="h" style="font-size:64px">💬 Comment</div><div class="h" style="font-size:64px;color:var(--crema)">A or B</div></div></div>'''
A='#EADBC4'; Bc='#D9A35B'
FVG='<svg width="190" height="190" viewBox="0 0 150 150"><rect x="10" y="62" width="130" height="30" fill="rgba(217,163,91,.3)"/><g stroke="#3DDC97" stroke-width="4"><line x1="30" y1="85" x2="30" y2="125"/><line x1="75" y1="30" x2="75" y2="130"/><line x1="120" y1="15" x2="120" y2="70"/></g><rect x="20" y="92" width="20" height="25" fill="#3DDC97"/><rect x="63" y="40" width="24" height="80" fill="#3DDC97"/><rect x="110" y="22" width="20" height="40" fill="#3DDC97"/></svg>'
OB='<svg width="190" height="190" viewBox="0 0 150 150"><rect x="14" y="78" width="40" height="52" fill="none" stroke="#D9A35B" stroke-width="4" stroke-dasharray="6 5"/><g stroke-width="4"><line x1="34" y1="75" x2="34" y2="135" stroke="#F0616D"/><line x1="80" y1="40" x2="80" y2="125" stroke="#3DDC97"/><line x1="122" y1="10" x2="122" y2="60" stroke="#3DDC97"/></g><rect x="24" y="85" width="20" height="38" fill="#F0616D"/><rect x="69" y="48" width="22" height="70" fill="#3DDC97"/><rect x="111" y="18" width="22" height="36" fill="#3DDC97"/></svg>'
S={}
S['q1']=ctx('Gold or dollars?','Fri 6 Nov 2026 · for the next week')+opt('A','Gold','just +5% in a week · markets scared','@1',A)+opt('B','US dollar','the Fed is talking about more hikes','@2',Bc)+TIMER
S['r1']=ctx('What happened','Week of 9–13 Nov 2026')+opt('A','Gold','hot US inflation pushed yields up','@1',A,res='<span data-sign data-count="0|-4.7|@1+0.4|1.2|1">0</span>%',rc='var(--bear)')+opt('B','US dollar','strongest currency of the week (vs the 7 others)','@2',Bc,res='<span data-sign data-count="0|1.1|@2+0.4|1.2|1">0</span>%',rc='var(--bull)')+TIP('@2+3','Gold pays no interest, so rising yields hurt it.')
S['q2']=ctx('FVG or Order Block?','Price just broke higher. Where do you enter?')+opt('A','Fair Value Gap','the gap 3 candles leave in a fast move','@1',A,FVG)+opt('B','Order Block','the last down candle before the push','@2',Bc,OB)+TIMER
S['r2']=ctx('No winner every time','How the two zones behave')+opt('A','FVG','closer → often tested first<br>thin → price can slice through','@1',A)+opt('B','Order Block','deeper → you may miss the move<br>often seen as the stronger zone','@2',Bc)+TIP('@3','Best: both line up. The fundamental bias tells you which direction to look in.')
S['q3']=ctx('Franc or kiwi?','Same week · 9–13 Nov 2026')+opt('A','Swiss franc','pays 0% · the classic safe haven','@1',A)+opt('B','New Zealand dollar','pays 2.75% · election result not final','@2',Bc)+TIMER
S['r3']=ctx('What happened','Strength vs the 7 other currencies')+opt('A','Swiss franc','weakest of the week · nobody needed a hiding place','@0',A,res='<span data-sign data-count="0|-1.45|@0+0.6|1.2|2">0</span>%',rc='var(--bear)')+opt('B','New Zealand dollar','2nd best · markets liked the election result','@1',Bc,res='<span data-sign data-count="0|0.72|@1+0.4|1.2|2">0</span>%',rc='var(--bull)')
src=open('template.html').read()
start=src.index('<section class="sc" id="hook"'); end=src.index('<section class="sc" id="outro"')
out=src[:start]+''.join(f'<section class="sc" id="{k}">\n {v}\n</section>\n' for k,v in S.items())+src[end:]
# outro: loop line
out=out.replace('<div style="font-size:28px;color:var(--sub);margin-top:24px" data-in="@1">Big picture only. Not a trade signal.</div>','<div style="font-size:28px;color:var(--sub);margin-top:10px" data-in="0.9">Big picture only. Not a trade signal.</div><div class="h" data-reveal="@1" style="font-size:66px;color:var(--crema);margin-top:30px;line-height:1.1">Now that you know…<br>would you rather?</div>')
out=out.replace('<div style="font-size:34px;color:var(--sub)" data-in="0.9">The big picture, every morning</div>','')
out=out.replace('../../node_modules','./node_modules')
out=out.replace("const IDS=['hook','fed','yields','euro','yen','oil','gold','verdict','today','outro'];","const IDS=['q1','r1','q2','r2','q3','r3','outro'];")
out=re.sub(r"const CHIPS=\{.*?\};","const CHIPS={q1:'1 / 3',r1:'1 / 3',q2:'2 / 3',r2:'2 / 3',q3:'3 / 3',r3:'3 / 3'};",out)
out=re.sub(r"const SC8=.*?;\ndocument.getElementById\('bars'\).innerHTML=.*?\n","",out,flags=re.S)
out=out.replace('<div id="pairT">FX CHECK</div>','<div id="pairT" style="font-size:96px">WOULD YOU<br>RATHER?</div>').replace('<div style="font-size:26px;color:var(--sub);letter-spacing:3px;font-weight:600;margin-top:6px">OVERNIGHT · FRI 13 NOV</div>','<div style="font-size:26px;color:var(--sub);letter-spacing:3px;font-weight:600;margin-top:6px">TRADING EDITION</div>').replace('<div id="chip">FRIDAY<br>MORNING</div>','<div id="chip">1 / 3</div>')
out=out.replace("const FOLLOW=[['euro',6.5,10.5,8.4]];","const FOLLOW=[['r2',2.0,6.0,3.9]];")
out=out.replace("sc==='fed'&&t<TR","false").replace("const ck=sc==='outro'?'today':sc;","const ck=sc==='outro'?'r3':sc;")
out=out.replace("(sc==='verdict'||sc==='outro'||sc==='today'||sc==='euro')?'1500px':'1290px'","'1500px'")
out=out.replace("const showPair=!(sc==='hook'||sc==='outro');","const showPair=sc!=='outro';")
out=out.replace("S.querySelectorAll('.bar')","S.querySelectorAll('.barX')")
out=out.replace("if(sc==='hook')drawHook(t);","""S.querySelectorAll('[data-timer]').forEach(el=>{const s=TIM[sc].lead+TIM[sc].len+0.2;const k=t-s;el.style.opacity=ease(k/0.3);el.style.transform='scale('+(0.9+0.1*ease(k/0.3))+')';const n=Math.max(1,Math.min(3,3-Math.floor(Math.max(0,k))));el.querySelector('.tnum').textContent=k>=3?'✓':n;el.querySelector('.tring').setAttribute('stroke-dashoffset',502.7*Math.min(1,Math.max(0,k)/3))});""")
out=out.replace("if(sc==='hook')out.push({t:0.15,type:'swell'},{t:0.3,type:'hit'});","if(sc[0]==='q'){const s=TIM[sc].lead+TIM[sc].len+0.2;out.push({t:s,type:'tick'},{t:s+1,type:'tick'},{t:s+2,type:'tick'},{t:s+3,type:'ding'})}if(sc==='outro')out.push({t:T('outro','@1'),type:'hit'});")
# hide the old outro swell/click-follow ding timing (keep), captions: hide during outro second line? keep
open('scenes.html','w').write(out); print('ok')
