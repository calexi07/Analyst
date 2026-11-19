import json, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro
k = Kokoro("/home/claude/tts/kokoro-v1.0.onnx", "/home/claude/tts/voices-v1.0.bin")
SR=24000
SC = {
 "hook":    ["Bulls versus bears, on euro dollar.", "Who's in control this week?"],
 "monday":  ["Monday. Our weekly analysis.", "The model sided with the dollar, with a strong lean.",
             "The euro was weighed down by France's budget worries. Investors were nervous about lending to France.",
             "The dollar had strong US jobs behind it, and a Fed still talking about raising rates."],
 "tuesday": ["Tuesday. US prices rose faster than expected.", "That made a December rate hike more likely, and gave the dollar extra support."],
 "thursday":["Thursday morning. Today's check.",
             "France's stress eased a little. Its extra cost to borrow, compared with Germany, dropped from one sixty-two to one forty-two.",
             "Good for the euro. But it's still in the red zone. Below one thirty would change the story.",
             "In America, traders now see about a ninety-one percent chance of a December rate hike."],
 "verdict": ["So, where does that leave euro dollar?", "The dollar still leads.",
             "If France keeps calming down, the gap could narrow a little. But the lean stays with the dollar.",
             "Next: Friday's data from Europe and the US. Then France's budget debate, from the twentieth."],
 "outro":   ["Follow FX Before Coffee for the next check, every morning.", "Big picture only. Not a trade signal."],
}
GAP=0.38; meta={}
for name,phr in SC.items():
    parts=[]; starts=[]; t=0.0
    for i,p in enumerate(phr):
        a,sr=k.create(p, voice="af_heart", speed=1.0, lang="en-us")
        idx=np.where(np.abs(a)>0.01)[0]; a=a[max(0,idx[0]-240):idx[-1]+1200]
        starts.append(round(t,3)); parts.append(a); t+=len(a)/SR
        if i<len(phr)-1: parts.append(np.zeros(int(GAP*SR),dtype=a.dtype)); t+=GAP
    full=np.concatenate(parts); sf.write(f"v4/vo_{name}.wav", full, SR)
    meta[name]={"starts":starts,"len":round(len(full)/SR,3)}
json.dump(meta,open("v4/vo.json","w"),indent=1); print(meta, sum(m['len'] for m in meta.values()))
