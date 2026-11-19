import json, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro
from spec import PAIRS
k = Kokoro("/home/claude/tts/kokoro-v1.0.onnx", "/home/claude/tts/voices-v1.0.bin")
SR=24000
SC={"hook":["Every US dollar pair, in one video.","Here's where each one stands this Friday morning."],
 "dollar":["First, the dollar itself.","Fed officials Mary Daly and John Williams said more rate hikes are likely.","The US ten-year yield hit about five point one percent, and a December hike looks almost certain.","That's why the dollar scores plus seven, at the top of our board."],
 "guide":["A quick guide before we start.","We score each currency from minus eighteen to plus eighteen.","The gap between two currencies gives the bias. Three points or more means a real lean."]}
for p in PAIRS: SC[p['id']]=p['vo']
SC["summary"]=["So, the big picture.","All seven currency pairs still lean towards the dollar, and gold stays bullish, but under pressure.","Nothing changed in our scores overnight."]
SC["today"]=["Today, watch two things.","Euro-area growth at ten GMT, and US producer prices at one thirty GMT.","A hot inflation reading would give the dollar even more fuel."]
SC["outro"]=["Follow FX Before Coffee.","Not a trade signal."]
GAP=0.5; meta={}
for name,phr in SC.items():
    parts=[];starts=[];lens=[];t=0.0
    for i,p in enumerate(phr):
        a,_=k.create(p,voice="af_heart",speed=0.95,lang="en-us")
        idx=np.where(np.abs(a)>0.01)[0];a=a[max(0,idx[0]-120):idx[-1]+900]
        starts.append(round(t,3));lens.append(round(len(a)/SR,3));parts.append(a);t+=len(a)/SR
        if i<len(phr)-1: parts.append(np.zeros(int(GAP*SR),dtype=a.dtype));t+=GAP
    sf.write(f"vo_{name}.wav",np.concatenate(parts),SR)
    words=[]
    for p,s,l in zip(phr,starts,lens):
        ws=p.split(); w8=[len(w)+2 for w in ws]; tot=sum(w8); c=s+0.05
        for w,wt in zip(ws,w8):
            d=(l-0.1)*wt/tot; words.append([w,round(c,3),round(c+d,3)]); c+=d
    meta[name]={"starts":starts,"len":round(t,3),"words":words}
json.dump(meta,open("vo.json","w"),indent=1); print(list(meta), round(sum(v['len'] for v in meta.values()),1))
