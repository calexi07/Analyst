import json, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro
k=Kokoro("/home/claude/tts/kokoro-v1.0.onnx","/home/claude/tts/voices-v1.0.bin"); SR=24000
SC={"hook": ["Guess the chart."], "q1": ["Euro against Swiss franc, January 2015. For three years, Switzerland's central bank has defended a floor at one point twenty.", "Next day: up, or down? A, up. B, down.", "Need more time? Pause the video and comment your answer."], "r1": ["Here's what happened.", "On January fifteenth, the Swiss National Bank suddenly scrapped the floor.", "Euro-franc fell about fourteen percent in one day, and the franc spiked almost thirty percent within minutes."], "r2": ["The lesson?", "The calmest chart can hide the biggest risk.", "When a central bank holds a price in place, the chart can't tell you when it lets go. Fundamentals can warn you."], "outro": ["Now that you know..."]}
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
json.dump(meta,open("vo.json","w"),indent=1); print(round(sum(v['len'] for v in meta.values()),1))
