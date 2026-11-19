import json, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro
k = Kokoro("/home/claude/tts/kokoro-v1.0.onnx", "/home/claude/tts/voices-v1.0.bin")
SR=24000
SC = {
 "hook":    ["The dollar just got stronger,", "and the euro can't keep up."],
 "monday":  ["Monday, our model favoured the dollar.", "France's budget worries weighed on the euro, while strong US jobs lifted the dollar."],
 "thursday":["Thursday morning, France's stress eased a little.", "But it's still in the red zone.", "And after Tuesday's hot US inflation, traders see about a ninety-one percent chance of a December rate hike."],
 "verdict": ["So, the dollar still leads.", "Watch Friday's data, and France's budget debate from the twentieth."],
 "outro":   ["Follow FX Before Coffee for tomorrow's check.", "Not a trade signal."],
}
GAP=0.25; meta={}
for name,phr in SC.items():
    parts=[];starts=[];lens=[];t=0.0
    for i,p in enumerate(phr):
        a,_=k.create(p,voice="af_heart",speed=1.08,lang="en-us")
        idx=np.where(np.abs(a)>0.01)[0];a=a[max(0,idx[0]-120):idx[-1]+900]
        starts.append(round(t,3));lens.append(round(len(a)/SR,3));parts.append(a);t+=len(a)/SR
        if i<len(phr)-1: parts.append(np.zeros(int(GAP*SR),dtype=a.dtype));t+=GAP
    full=np.concatenate(parts);sf.write(f"short/vo_{name}.wav",full,SR)
    # word timings (proportional to characters)
    words=[]
    for p,s,l in zip(phr,starts,lens):
        ws=p.split(); w8=[len(w)+2 for w in ws]; tot=sum(w8); c=s+0.05
        for w,wt in zip(ws,w8):
            d=(l-0.1)*wt/tot; words.append([w,round(c,3),round(c+d,3)]); c+=d
    meta[name]={"starts":starts,"len":round(len(full)/SR,3),"words":words}
json.dump(meta,open("short/vo.json","w"),indent=1); print({k2:v['len'] for k2,v in meta.items()}, sum(v['len'] for v in meta.values()))
