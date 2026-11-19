import json,re,math,html,sys
sys.path.insert(0,'/home/claude/w46/tv')
from pair_stories import S
V=json.load(open('kit/vol_W46.json'))
D=json.load(open('p2/dobs-2026-W46-final.json'))
e=html.escape
TIMES={'US CPI (October)':('Tue 10 Nov','15:30'),'BoJ Summary of Opinions (October meeting)':('Tue 10 Nov','01:50'),
'China CPI and PPI (October)':('Mon 9 Nov',None),'China trade balance (October)':('Tue 10 Nov',None),'BoC Summary of Deliberations':('Tue 10 Nov',None),
'OPEC monthly oil market report':('Wed 11 Nov',None),'UK Q3 GDP (first estimate)':('Thu 12 Nov','09:00'),'Euro-area Q3 GDP (second estimate)':('Fri 13 Nov','12:00'),
'US PPI (October)':('Fri 13 Nov','15:30'),'Rating reviews: Fitch Germany, S&P Italy':('Fri 13 Nov','late, after the close'),'IEA oil market report':('Fri 13 Nov',None)}
SHORT={'US CPI (October)':'US CPI','BoJ Summary of Opinions (October meeting)':'BoJ opinions','China CPI and PPI (October)':'China CPI','China trade balance (October)':'China trade',
'BoC Summary of Deliberations':'BoC minutes','OPEC monthly oil market report':'OPEC report','UK Q3 GDP (first estimate)':'UK GDP','Euro-area Q3 GDP (second estimate)':'EU GDP',
'US PPI (October)':'US PPI','Rating reviews: Fitch Germany, S&P Italy':'Ratings DE/IT','IEA oil market report':'IEA report'}
def dec(p): return 2 if p=='XAUUSD' else (3 if p.endswith('JPY') else 5)
# legend pool: different wording per pair, numbers filled in by JS on copy
LEG=[
["🔵 Week starts here: Friday's close, where the week begins.","🟦 Typical week: a normal week for {p}.","⬛ Big-news week: how far it can stretch when headlines hit.","{s} Bias side: the half the fundamental bias favours. A direction, not a target."],
["🔵 Week starts here = last Friday's close.","🟦 Typical week = where {p} usually spends a week.","⬛ Big-news week = the wider zone for surprise weeks.","{s} Bias side = where the fundamentals lean, not a price goal."],
["🔵 Week starts here: the anchor, Friday's close.","🟦 Typical week: how far {p} usually travels in five days.","⬛ Big-news week: the stretch reached only on big news.","{s} Bias side: the half of the box the fundamentals point to. No target implied."],
["🔵 Week starts here: Friday's close.","🟦 Typical week: a quiet, ordinary week for {p}.","⬛ Big-news week: a week with real surprises.","{s} Bias side: which way the fundamental lean points. Not a trade level."],
]
HEAD=["🗺️ HOW TO READ THE CHART","🗺️ READING THE BOXES","🗺️ CHART LEGEND","🗺️ WHAT'S DRAWN ON THE CHART"]
KW={'EUR':('💶',['euro','french','ecb','paris','spread','senate']),'USD':('💵',['dollar','us ','fed','american']),'GBP':('💷',['pound','uk ','boe','sterling']),
 'JPY':('💴',['yen','boj','tokyo','japan','carry']),'CHF':('🏔️',['franc','snb','swiss']),'CAD':('🛢️',['loonie','cad','oil','canada','crude','tariff']),
 'AUD':('🦘',['aussie','rba','china','iron']),'NZD':('🥝',['kiwi','dairy','coalition','new zealand']),'XAU':('🥇',['gold','etf','real yields','haven'])}
def emo(text,b,q):
    t=text.lower()
    if b=='XAU' and ('us ' in t or 'inflation' in t): return '💵'
    for c in (b,q):
        if any(w in t for w in KW[c][1]): return KW[c][0]
    return '✨'
pairs=D['pairs']; kits=[]
for k,p in enumerate(pairs):
    pr=p['pair']; c,sg=V['data'][pr]; d=dec(pr); s=sg/100
    lv=lambda n: round(c*math.exp(n*s),d)
    side={'bearish':'lower half (bearish lean)','bullish':'upper half (bullish lean)'}.get(p['bias'],'none — two-sided, shade nothing')
    pins=[]
    for ct in p['catalysts']:
        if ct['event'] in TIMES:
            day,t=TIMES[ct['event']]; pins.append(dict(day=day,time=t,label=SHORT[ct['event']],event=ct['event']))
    b_,q_=pr[:3],pr[3:]
    fl=S[pr]['flip']
    def pick(c):
        for f in fl:
            t=f.lower()
            if any(w in t for w in KW[c][1]) and not (c!='USD' and b_=='XAU' and False): return f
        return None
    fb,fq=pick(b_),pick(q_)
    if fb==fq or fb is None or fq is None:
        rest=[f for f in fl if f not in (fb,fq)]
        fb=fb or (rest.pop(0) if rest else fl[0]); fq=fq if (fq and fq!=fb) else (rest.pop(0) if rest else fl[1])
    f0,f1=fb,fq
    twist='⚡ PLOT TWIST WATCH ⚡\n\n'+emo(f0,b_,q_)+' '+f0+'\n\n'+emo(f1,b_,q_)+' '+f1+'\n\n'+(['🤝 Until one of these happens, it stays a stand-off.','🤝 No clear winner until one of these shows up.'][k%2] if p['bias']=='two-sided' else ['👀 Until then, the story stays on track.','👀 Until one of these shows up, the bias holds.','👀 No twist yet? Then the plot stays the same.','👀 Watch these. Everything else is noise.'][k%4])
    kits.append(dict(pair=pr,close=round(c,d),sigma=sg,dec=d,bias=p['bias'],side=side,pins=pins,twist=twist,leg=LEG[k%len(LEG)],head=HEAD[k%len(HEAD)]))
json.dump(kits,open('kit/kits_W46.json','w'),ensure_ascii=False,indent=1)
def kit_html(i,x):
    pin="".join(f"<li><b>{e(z['label'])}</b> · {e(z['day'])}{(' '+e(z['time'])+('' if 'late' in z['time'] else ' Bucharest')) if z['time'] else ' (time not verified)'}</li>" for z in x['pins']) or "<li>No scheduled catalyst this week</li>"
    bear=x['bias']=='bearish'; bull=x['bias']=='bullish'
    mk={'bearish':('#E53935','Bearish','Red'),'bullish':('#43A047','Bullish','Green')}.get(x['bias'],('#9E9E9E','Two-sided','Grey'))
    marker=f'<tr><td><span class="sw" style="background:{mk[0]};width:3px"></span>Week marker</td><td colspan="2" style="text-align:center">Mon 9 Nov open</td><td>{mk[2]} vertical line, text "Week 46 · {mk[1]}"</td></tr>'
    if bear: story=f'<tr><td><span class="sw" style="background:#E53935;opacity:.55"></span>Bias side</td><td class="k2a"></td><td class="k0b"></td><td>Red-pink fill, red label</td></tr>'
    elif bull: story=f'<tr><td><span class="sw" style="background:#43A047;opacity:.55"></span>Bias side</td><td class="k0c"></td><td class="k2b"></td><td>Green fill, green label</td></tr>'
    else: story='<tr><td colspan="4" class="hint">Two-sided pair: no bias side to shade.</td></tr>'
    return f'''<div class="kit" data-k="{i}"><div class="lbl">🗺️ Chart kit · draw these on TradingView</div>
<div class="kr">Friday close <input class="kc" type="number" step="any" value="{x['close']}" oninput="kit({i})"> <span class="hint">reference; type your chart's Friday close</span></div>
<div class="hint">Rectangle → double-click → <b>Coordinates</b>: #1 = bottom price, #2 = top price. Bars: Mon 9 Nov → Fri 13 Nov (5 daily candles).</div>
<table class="kt"><tr><th>Drawing</th><th>#1 (bottom)</th><th>#2 (top)</th><th>Style</th></tr>
<tr><td><span class="sw" style="background:#2962FF;height:3px"></span>Week starts here</td><td colspan="2" class="k0" style="text-align:center"></td><td>Blue line, extend right</td></tr>
{marker}
<tr><td><span class="sw" style="background:#C5CAE9;border:1.5px solid #1A3A8F"></span>Typical week</td><td class="k1a"></td><td class="k1b"></td><td>Dark blue border, light blue fill, blue label</td></tr>
<tr><td><span class="sw" style="border:1.5px dashed #111;background:#fff"></span>Big-news week</td><td class="k2a"></td><td class="k2b"></td><td>Black dashed lines, no fill, black label</td></tr>
{story}</table>
<div class="lbl">📌 News pins (4H)</div><ul class="kp">{pin}</ul>
<div class="lbl">💡 Plot-twist note</div><div class="kn">{e(x['twist']).replace(chr(10),"<br>")}</div>
<div class="btns"><button onclick="cpk({i},this)">Copy chart guide (article)</button><button onclick="cpk({i},this,1)">Copy legend (chart text box)</button><button onclick="cpn({i},this)">Copy note text</button></div>
<div class="hint">Typical week = the move {e(x['pair'])} stayed within in about 2 of 3 weeks over the last 26 weeks (±{x['sigma']}% from Friday's close); big-news week = twice that. Not a target and not a signal.</div></div>'''
CSS='''.kit{background:#10161f;border:1px solid #23415c;border-radius:8px;padding:8px 10px;margin:6px 0 10px;font-size:13.5px}.kit input.kc{width:110px;padding:4px 6px;margin:4px 4px;font-size:13px;display:inline-block}.kt{width:100%;border-collapse:collapse;margin:4px 0}.kt th{font-size:11.5px;color:var(--sub);text-align:left;font-weight:600;padding:3px 4px}.kt td{padding:4px;border-bottom:1px solid #1e2632;vertical-align:middle}.kt td:nth-child(2),.kt td:nth-child(3){font-variant-numeric:tabular-nums;font-weight:600;white-space:nowrap}.kt td:last-child{font-size:12px;color:var(--sub)}.sw{display:inline-block;width:14px;height:10px;margin-right:6px;vertical-align:middle;border-radius:2px}.kp{margin:2px 0;padding-left:18px}.kn{color:#cfd3d8;font-style:italic}.flag{font-size:12.5px;color:var(--sub);margin-top:6px}'''
JS='''const KIT=__KIT__;
function kv(i){const x=KIT[i];const el=document.querySelector('.kit[data-k="'+i+'"]');const c=parseFloat(el.querySelector('.kc').value);const s=x.sigma/100;const f=n=>(c*Math.exp(n*s)).toFixed(x.dec);return {el,c:isFinite(c)?c.toFixed(x.dec):'?',t1:f(-1),t2:f(1),b1:f(-2),b2:f(2)}}
function kit(i){const v=kv(i);v.el.querySelector('.k0').textContent=v.c;const q=(c,t)=>v.el.querySelectorAll(c).forEach(n=>n.textContent=t);q('.k1a',v.t1);q('.k1b',v.t2);q('.k2a',v.b1);q('.k2b',v.b2);q('.k0b',v.c);q('.k0c',v.c)}
function cpk(i,b,plain){const v=kv(i),x=KIT[i];const L=x.leg.map(s=>s.replace('{p}',x.pair).replace('{s}',x.bias==='bearish'?'🟥':'🟩'));const lines=x.bias==='two-sided'?L.filter(s=>!s.includes('Bias side')):L;const t=plain?(x.head+'\\n\\n'+lines.join('\\n')):('[b]'+x.head+'[/b]\\n[list]\\n'+lines.map(s=>'[*]'+s).join('\\n')+'\\n[/list]');cpt(t,b)}
function cpn(i,b){cpt(KIT[i].twist,b)}
function cpt(t,b){if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(t).then(()=>done(b,'Copied ✓'),()=>fallback(t,b));else fallback(t,b)}
KIT.forEach((_,i)=>kit(i));'''
h=open('tv/TradingView_Ideas_Week46_v3.html').read()
order=[x['pair'] for x in kits]
for i,x in enumerate(kits):
    a=h.index(f'<section class="card" data-pair="{x["pair"]}" id="{x["pair"]}">')
    m=h.index('<details>',a)
    h=h[:m]+kit_html(i,x)+'\n '+h[m:]
FL={'✅':'✓ green flag','🟡':'✓ green flag','👀':'! amber flag','⚠️':'! amber flag','❌':'✗ red flag','⚪':'– grey flag (two-sided)'}
def addflag(mm):
    sec=mm.group(0); tag=re.search(r'class="tag [a-z]+">([^<]*)',sec).group(1)
    fl=next((v for k,v in FL.items() if tag.startswith(k)),None)
    if not fl or 'class="flag"' in sec: return sec
    return sec.replace('<div class="btns">',f'<div class="flag">🚩 Chart flag for this check: <b>{fl}</b> on the 4H candle of the check</div>\n <div class="btns">',1)
i=h.index('<div id="dy"'); j=h.index('<script>',i)
dy=re.sub(r'<section class="card" data-pair="[A-Z]+">.*?</section>',addflag,h[i:j],flags=re.S)
h=h[:i]+dy+h[j:]
h=h.replace('</style>',CSS+'</style>',1)
k=h.rindex('</script>'); h=h[:k]+JS.replace('__KIT__',json.dumps(kits,ensure_ascii=False).replace('</','<\\/'))+'\n'+h[k:]
open('tv/TradingView_Ideas_Week46_v4.html','w').write(h)
js=h[h.rindex('<script>')+8:h.rindex('</script>')]; open('/tmp/c4.js','w').write(js)
print(h.count('class="kit"'),h.count('class="flag"'))
