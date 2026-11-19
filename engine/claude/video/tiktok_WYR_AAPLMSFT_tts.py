import json, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro
k=Kokoro("/home/claude/tts/kokoro-v1.0.onnx","/home/claude/tts/voices-v1.0.bin"); SR=24000
SC={
"hook":["Would you rather..."],
"q1":["put one thousand dollars into Apple, or into Microsoft, ten years ago?","A, Apple. B, Microsoft.","Need more time? Pause the video and comment your answer."],
"r1":["Let's race them.","Microsoft turned one thousand dollars into about nine thousand seven hundred.","Apple kept going, to about fourteen thousand."],
"r2":["Same thousand dollars. One decision.","More than four thousand dollars apart.","And remember, the past doesn't promise the future."],
"outro":["Now that you know..."]}
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
