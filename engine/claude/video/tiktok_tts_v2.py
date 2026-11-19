import json, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro
k = Kokoro("/home/claude/tts/kokoro-v1.0.onnx", "/home/claude/tts/voices-v1.0.bin")
VOICE="af_heart"; SR=24000
SC = {
 "hook":   ["France just caught a break.", "So, is the euro finally fighting back?", "Or is the dollar still the boss?"],
 "recap":  ["Let's rewind to Monday.",
            "Our model compared the euro and the dollar, and leaned clearly toward the dollar.",
            "The euro was carrying a heavy backpack. France's budget problems, which make investors nervous about lending to France.",
            "The dollar had the opposite story. Lots of new jobs in America, and a central bank still talking about raising rates. And higher rates tend to pull money into a currency.",
            "Then, on Tuesday, American prices rose faster than expected. That made a rate rise even more likely. Good news for the dollar."],
 "changed":["So, what happened overnight?",
            "France got some relief. The extra cost France pays to borrow, compared with Germany, dropped from its recent high. Think of it as the market's stress meter going down.",
            "That helps the euro. But the meter is still in the red zone. It would need to fall further to really change the story.",
            "Meanwhile, in America, traders now see roughly a nine in ten chance that rates go up in December."],
 "today":  ["So, who's winning?", "The dollar is still well ahead.", "If France keeps calming down, the euro could close the gap a little.", "But for now, the story still favours the dollar."],
 "next":   ["What's next?", "On Friday, we get Europe's growth numbers, and a fresh look at American prices.", "Then, on the twentieth, France's Senate starts debating the budget."],
 "outro":  ["Bottom line: the dollar keeps the upper hand, for now.", "Follow Cristian Trading, and we'll walk you through the next chapter tomorrow.", "Remember, this is the big-picture story, not a trade signal."],
}
GAP=0.28
meta={}
for name,phr in SC.items():
    parts=[]; starts=[]; t=0.0
    for i,p in enumerate(phr):
        a,sr=k.create(p, voice=VOICE, speed=0.98, lang="en-us")
        # trim leading/trailing near-silence
        idx=np.where(np.abs(a)>0.01)[0]; a=a[max(0,idx[0]-240):idx[-1]+1200]
        starts.append(round(t,3)); parts.append(a); t+=len(a)/SR
        if i<len(phr)-1:
            parts.append(np.zeros(int(GAP*SR),dtype=a.dtype)); t+=GAP
    full=np.concatenate(parts); sf.write(f"v2/vo_{name}.wav", full, SR)
    meta[name]={"starts":starts,"len":round(len(full)/SR,3)}
json.dump(meta,open("v2/vo.json","w"),indent=1); print(meta)
