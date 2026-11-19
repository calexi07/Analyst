import os, sys, json, shutil, re
from specs import E
SRC='../aapl'
base_build=open(f'{SRC}/build_scenes.py').read()
base_tts=open(f'{SRC}/tts.py').read()
cues=open(f'{SRC}/cues.js').read()
RACE_JS=r'''if(sc==='r1'&&document.getElementById('vA')){const VA=__VA__,VB=__VB__,RN=__RN__;const aw=VA>=VB;const vL=Math.min(VA,VB),vW=Math.max(VA,VB);
 const p1=eio((t-T(sc,'@1'))/2.6),p2=eio((t-T(sc,'@2'))/2.0);const lo=1000+(vL-1000)*p1;const hi=lo+(vW-vL)*p2;
 const va=aw?hi:lo,vb=aw?lo:hi;const f=v=>'$'+(Math.round(v/RN)*RN).toLocaleString('en-US');
 const A=document.getElementById('vA'),Bv=document.getElementById('vB');A.textContent=((aw?p2:p1)>=1?'≈ ':'')+f(va);Bv.textContent=((aw?p1:p2)>=1?'≈ ':'')+f(vb);
 document.getElementById('bA').style.height=(40+430*va/vW)+'px';document.getElementById('bB').style.height=(40+430*vb/vW)+'px';
 const done=p2>=1;const wb=document.getElementById(aw?'bA':'bB'),wv=aw?A:Bv;wb.style.background=done?'var(--bull)':(aw?'var(--cream)':'var(--crema)');wv.style.color=done?'var(--bull)':(aw?'var(--cream)':'var(--crema)')}
'''
def esc(s): return s.replace('\\','\\\\').replace('"""','\\"\\"\\"')
for s in E:
    if len(sys.argv)>1 and s['id'] not in sys.argv[1:]: continue
    d=s['id']; os.makedirs(d,exist_ok=True)
    for f in ('template.html','render.js','audio_beat.py'):
        shutil.copy(f'{SRC}/{f}',d)
    if not os.path.exists(f'{d}/node_modules'): os.symlink(os.path.abspath(f'{SRC}/node_modules'),f'{d}/node_modules')
    # tts
    sc={'hook':['Would you rather...'],'q1':[s['vo_q'],s['vo_ab'],'Need more time? Pause the video and comment your answer.'],'r1':s['vo_r1'],'r2':s['vo_r2'],'outro':['Now that you know...']}
    t=base_tts; a=t.index('SC={'); b=t.index('GAP=0.5')
    open(f'{d}/tts.py','w').write(t[:a]+'SC='+json.dumps(sc,ensure_ascii=False)+'\n'+t[b:])
    # scenes block
    if s['kind']=='race':
        r1=f'''RACE="""<div class="card" data-in="0.3" style="display:flex;gap:40px;justify-content:center;align-items:flex-end;height:760px;padding:30px 40px">
 <div style="display:flex;flex-direction:column;align-items:center;gap:14px;width:340px"><div class="num" id="vA" style="white-space:nowrap;font-size:60px;color:var(--cream)">$1,000</div><div id="bA" style="width:200px;border-radius:18px 18px 6px 6px;background:var(--cream);height:40px"></div><div class="h" style="font-size:40px;white-space:nowrap">{esc(s['ra'])}</div></div>
 <div style="display:flex;flex-direction:column;align-items:center;gap:14px;width:340px"><div class="num" id="vB" style="white-space:nowrap;font-size:60px;color:var(--crema)">$1,000</div><div id="bB" style="width:200px;border-radius:18px 18px 6px 6px;background:var(--crema);height:40px"></div><div class="h" style="font-size:40px;white-space:nowrap">{esc(s['rb'])}</div></div></div>"""
S['r1']=ctx('The race',"{esc(s['r1_sub'])}")+RACE'''
    else:
        r1=f'''S['r1']=ctx("{esc(s['r1_title'])}","{esc(s['r1_sub'])}")+opt('A',"{esc(s['A'][0])}","{esc(s['cA'])}",'@1',A)+opt('B',"{esc(s['B'][0])}","{esc(s['cB'])}",'@2',Bc)'''
    blk=f'''S['q1']=ctx("{esc(s['title'])}","{esc(s['sub'])}")+opt('A',"{esc(s['A'][0])}","{esc(s['A'][1])}",'@0+0.6',A)+opt('B',"{esc(s['B'][0])}","{esc(s['B'][1])}",'@0+1.4',Bc)+TIMER
{r1}
S['r2']=ctx("{esc(s['r2_title'])}","{esc(s['r2_sub'])}")+"""<div class="card" data-in="@0+0.4" data-sfx="pop" style="text-align:center"><div class="lbl">{esc(s['lbl'])}</div><div class="num" style="font-size:{'150' if len(s['big'])<9 else '110'}px;color:var(--bull);margin:10px 0"><span data-reveal="@1" data-sfx="hit">{esc(s['big'])}</span></div><div style="font-size:32px;color:var(--sub)">{esc(s['bigsub'])}</div></div>
 <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px"><div class="card" data-in="@1+1.6"><div class="lbl">{esc(s['mA'][0])}</div><div class="num" style="font-size:58px;margin-top:6px">{esc(s['mA'][1])}</div></div><div class="card" data-in="@1+2.0"><div class="lbl">{esc(s['mB'][0])}</div><div class="num" style="font-size:58px;margin-top:6px;color:var(--crema)">{esc(s['mB'][1])}</div></div></div>"""+TIP('@2',"{esc(s['tip'])}")
'''
    bb=base_build; a=bb.index("S['q1']="); b=bb.index("src=open('template.html')")
    bb=bb[:a]+blk+bb[b:]
    bb=bb.replace("const CHIPS={q1:'STOCKS',r1:'STOCKS',r2:'STOCKS'};",f"const CHIPS={{q1:'{s['chip']}',r1:'{s['chip']}',r2:'{s['chip']}'}};").replace('<div id="chip">STOCKS</div>',f'<div id="chip">{s["chip"]}</div>')
    open(f'{d}/build_scenes.py','w').write(bb)
    open(f'{d}/race.js','w').write(RACE_JS.replace('__VA__',str(s.get('VA',0))).replace('__VB__',str(s.get('VB',0))).replace('__RN__',str(s.get('rnd',10))) if s['kind']=='race' else '')
    open(f'{d}/cues.js','w').write(cues if s['kind']=='race' else '')
    print('prepared',d)
