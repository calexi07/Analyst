import json, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro
k = Kokoro("/home/claude/tts/kokoro-v1.0.onnx", "/home/claude/tts/voices-v1.0.bin")
SR=24000
SC = {
 "hook":   ["Bulls versus bears, on the euro-dollar.", "Who's winning this week?"],
 "monday": ["Monday's weekly analysis: our model sided with the dollar.", "France's budget worries weighed on the euro, while strong US jobs kept the dollar on top."],
 "overnight": ["Now, today's check. Thursday morning.", "France's stress eased a little. Good for the euro, but not enough to flip the story.", "And a US rate hike in December now looks very likely."],
 "verdict":["So, the dollar still leads.", "Next tests: Friday's data, and France's budget debate."],
 "outro":  ["Follow Forex Fundamental Guide for tomorrow's check.", "Big picture, not a trade signal."],
}
GAP=0.22; meta={}
for name,phr in SC.items():
    parts=[]; starts=[]; t=0.0
    for i,p in enumerate(phr):
        a,sr=k.create(p, voice="af_heart", speed=1.06, lang="en-us")
        idx=np.where(np.abs(a)>0.01)[0]; a=a[max(0,idx[0]-240):idx[-1]+1200]
        starts.append(round(t,3)); parts.append(a); t+=len(a)/SR
        if i<len(phr)-1: parts.append(np.zeros(int(GAP*SR),dtype=a.dtype)); t+=GAP
    full=np.concatenate(parts); sf.write(f"v3/vo_{name}.wav", full, SR)
    meta[name]={"starts":starts,"len":round(len(full)/SR,3)}
json.dump(meta,open("v3/vo.json","w"),indent=1); print(meta, sum(m['len'] for m in meta.values()))
