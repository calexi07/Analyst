import json
from spec import PAIRS
s=open('../v2/scenes.html').read()
a=s.index('<section class="sc" id="fed">'); b=s.index('<section class="sc" id="outro"')
def head(t,sub,fs=140): return f'<div data-in="0.05"><div class="day" style="font-size:{fs}px">{t}</div><div class="dsub">{sub}</div></div>'
def expl(txt,at): return f'<div data-in="{at}" class="card" style="font-size:34px;line-height:1.35;font-weight:600;border-color:rgba(217,163,91,.35)">💡 {txt}</div>'
def sgn(v): return f"+{v}" if v>0 else (f"−{-v}" if v<0 else "0")
def col(v): return 'var(--bull)' if v>0 else ('var(--bear)' if v<0 else 'var(--sub)')
N=f'''<section class="sc" id="dollar">
 {head("THE DOLLAR","Why it leads · Fri 13 Nov")}
 <div data-in="@1" data-sfx="pop" class="card"><div class="lbl">FED OFFICIALS</div><div class="h" style="font-size:50px;margin-top:10px">Daly &amp; Williams:<br>“more hikes likely”</div></div>
 <div style="display:grid;grid-template-columns:1fr 1fr;gap:22px">
  <div class="card" data-in="@2" data-sfx="pop"><div class="lbl">US 10-YEAR</div><div class="num" style="font-size:96px;color:var(--bull);margin:8px 0"><span data-count="4.98|5.10|@2+0.3|1.4|2">4.98</span>%</div></div>
  <div class="card" data-in="@2+2.2" data-sfx="pop"><div class="lbl">DEC FED HIKE</div><div class="num" style="font-size:60px;color:var(--bull);margin:18px 0">ALMOST<br>CERTAIN</div></div>
 </div>
 <div class="card" data-in="@3" data-sfx="hit" style="display:flex;align-items:baseline;gap:22px"><span class="lbl">USD SCORE</span><span class="num" style="font-size:110px;color:var(--bull)" data-sign data-count="0|7|@3+0.3|1">0</span></div>
</section>
<section class="sc" id="guide">
 {head("HOW TO READ","Our fundamental scores",130)}
 <div class="card" data-in="@1" data-sfx="pop"><div class="lbl">EACH CURRENCY</div><div style="display:flex;justify-content:space-between;align-items:baseline;margin-top:12px"><span class="num" style="font-size:80px;color:var(--bear)">−18</span><span class="num" style="font-size:50px;color:var(--sub)">0</span><span class="num" style="font-size:80px;color:var(--bull)">+18</span></div>
 <div style="height:12px;border-radius:6px;margin-top:14px;background:linear-gradient(90deg,var(--bear),rgba(234,219,196,.25) 50%,var(--bull))"></div></div>
 <div class="card" data-in="@2" data-sfx="pop" style="font-size:34px;line-height:1.5;font-weight:600">GAP = base score − quote score<br><span style="color:var(--bull)">+3 or more → bullish</span><br><span style="color:var(--bear)">−3 or less → bearish</span><br><span style="color:var(--sub)">in between → two-sided</span></div>
</section>
'''
for i,p in enumerate(PAIRS):
    (bc,bs),(qc,qs)=p['b'],p['q']; g=p['gap']
    pos=50-g/18*50 if p['id']!='xauusd' else 50-7/18*50
    bcol='#FF9AA2' if p['bias']=='bearish' else '#7FEBBE'; bbg='rgba(240,97,109,.16)' if p['bias']=='bearish' else 'rgba(61,220,151,.16)'
    lbl_b = 'GOLD (XAU)' if bc=='XAU' else bc
    N+=f'''<section class="sc" id="{p['id']}">
 <div data-in="0.05"><div class="day" style="font-size:150px">{p['pair']}</div><div class="dsub">{p['sub']} · pair {i+1} of 8</div></div>
 <div data-in="@1" data-sfx="tick" style="display:flex;align-items:center;gap:16px;flex-wrap:wrap"><span style="padding:12px 22px;border-radius:14px;background:{bbg};color:{bcol};font-family:SG;font-weight:700;font-size:36px">{p['bias'].upper()}</span><span style="font-size:32px;color:var(--sub)">{p['fav']} · {p['conv']}</span></div>
 <div class="card" data-in="@2" style="display:flex;flex-direction:column;gap:14px">
  <div style="display:flex;justify-content:space-between;align-items:baseline"><span><span class="lbl">{lbl_b}</span><br><span class="num" style="font-size:84px;color:{col(bs)}" data-sign data-count="0|{bs}|@2+0.2|0.8">0</span></span><span style="text-align:center"><span class="lbl">GAP</span><br><span class="num" style="font-size:84px;color:var(--crema)" data-sign data-count="0|{g}|@2+1.0|0.9">0</span></span><span style="text-align:right"><span class="lbl">{qc}</span><br><span class="num" style="font-size:84px;color:{col(qs)}" data-sign data-count="0|{qs}|@2+0.6|0.8">0</span></span></div>
  <div style="position:relative;height:46px"><div style="position:absolute;left:0;right:0;top:18px;height:10px;border-radius:5px;background:linear-gradient(90deg,rgba(234,219,196,.35),rgba(234,219,196,.12) 50%,rgba(234,219,196,.35))"></div><div style="position:absolute;top:0;width:46px;height:46px;margin-left:-23px;border-radius:50%;background:var(--crema);left:50%" data-move="{pos:.1f}|@2+1.0|1.0"></div></div>
 </div>
 <div class="card" data-in="@3" data-sfx="pop"><div class="lbl">OVERNIGHT</div><div class="h" style="font-size:44px;line-height:1.2;margin-top:10px">{p['news']}</div></div>
 {expl(p['tip'],'@4')}
</section>
'''
rows="".join(f'<div style="display:flex;justify-content:space-between;align-items:baseline;padding:6px 0;border-bottom:1px solid rgba(234,219,196,.08)"><span class="num" style="font-size:42px">{p["pair"]}</span><span style="font-size:28px;font-weight:700;color:{"#FF9AA2" if p["bias"]=="bearish" else "#7FEBBE"}">{p["bias"].upper()}</span><span class="num" style="font-size:42px;width:170px;text-align:right;color:var(--crema)">{"+4…+7" if p["id"]=="xauusd" else sgn(p["gap"])}</span></div>' for p in PAIRS)
N+=f'''<section class="sc" id="summary">
 {head("BIG PICTURE","All USD pairs · gaps",120)}
 <div class="card" data-in="@1" data-sfx="pop" style="padding:22px 30px">{rows}</div>
 <div class="h" style="font-size:56px" data-reveal="@2" data-sfx="hit">No score changes overnight.</div>
</section>
<section class="sc" id="today">
 {head("TODAY","What to watch · Fri 13 Nov")}
 <div class="card" data-in="@1" data-sfx="pop" style="display:flex;align-items:center;gap:26px"><div class="num" style="font-size:64px;color:var(--crema)">10:00</div><div><div class="h" style="font-size:44px">Euro-area GDP</div><div style="font-size:26px;color:var(--sub)">GMT · growth, 2nd estimate</div></div></div>
 <div class="card" data-in="@1+2.6" data-sfx="pop" style="display:flex;align-items:center;gap:26px"><div class="num" style="font-size:64px;color:var(--crema)">13:30</div><div><div class="h" style="font-size:44px">US producer prices</div><div style="font-size:26px;color:var(--sub)">GMT · October PPI</div></div></div>
 {expl("Hot inflation = more fuel for the dollar.","@2")}
</section>
'''
s=s[:a]+N+s[b:]
ids=['hook','dollar','guide']+[p['id'] for p in PAIRS]+['summary','today','outro']
import re
s=re.sub(r"const IDS=\[.*?\];","const IDS="+json.dumps(ids)+";",s,count=1)
chips={'dollar':'USD','guide':'GUIDE','summary':'ALL 8','today':'FRIDAY<br>13 NOV'}
for i,p in enumerate(PAIRS): chips[p['id']]=f'{i+1} / 8'
s=re.sub(r"const CHIPS=\{.*?\};","const CHIPS="+json.dumps(chips)+";",s,count=1)
s=re.sub(r"const FOLLOW=\[.*?\];","const FOLLOW=[['usdjpy',9.0,13.0,11.0]];",s,count=1)
s=s.replace("if(sc==='fed'&&t<TR)pa=eio(t/TR)","if(sc==='dollar'&&t<TR)pa=eio(t/TR)")
s=s.replace('<div id="pairT">FX CHECK</div>','<div id="pairT">USD PAIRS</div>')
s=re.sub(r"el\.style\.top=\(sc==='verdict'.*?:'1290px';","el.style.top=(sc==='hook')?'1290px':'1560px';",s)
# bars code references #bars which no longer exists -> guard
s=s.replace("document.getElementById('bars').innerHTML=","(document.getElementById('bars')||{}).innerHTML=")
s=s.replace("const ck=sc==='outro'?'today':sc;","const ck=sc==='outro'?'today':sc;")
# hook title
s=s.replace('font-size:200px;letter-spacing:-4px;line-height:1">OVERNIGHT</div>','font-size:170px;letter-spacing:-4px;line-height:1">USD PAIRS</div>')
s=s.replace('FX CHECK · FRI 13 NOV</div>\n </div>\n</section>','ALL 8 · FRI 13 NOV</div>\n </div>\n</section>',1)
open('scenes.html','w').write(s)
print(ids)
