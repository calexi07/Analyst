import json, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro
from spec import phrases
SPK={'EUR/USD':'euro-dollar','GBP/USD':'pound-dollar','USD/CAD':'dollar-C A D','EUR/JPY':'euro-yen','EUR/CAD':'euro-C A D','GBP/JPY':'pound-yen','GBP/CAD':'pound-C A D','USD/JPY':'dollar-yen','CAD/JPY':'C A D-yen','USD/CHF':'dollar-franc','CAD/CHF':'C A D-franc','AUD/USD':'Aussie-dollar','AUD/CAD':'Aussie-C A D','AUD/NZD':'Aussie-kiwi','NZD/USD':'kiwi-dollar','NZD/JPY':'kiwi-yen','EUR/GBP':'euro-pound','EUR/NZD':'euro-kiwi','GBP/NZD':'pound-kiwi','AUD/CHF':'Aussie-franc','EUR/AUD':'euro-Aussie','EUR/CHF':'euro-franc','GBP/CHF':'pound-franc','GBP/AUD':'pound-Aussie','AUD/JPY':'Aussie-yen','NZD/CAD':'kiwi-C A D','NZD/CHF':'kiwi-franc','CHF/JPY':'franc-yen','XAU/USD':'gold-dollar'}
def sp(p):
    for a,b in SPK.items(): p=p.replace(a,b)
    return p
k = Kokoro("/home/claude/tts/kokoro-v1.0.onnx", "/home/claude/tts/voices-v1.0.bin")
SR=24000; GAP=0.55; meta={}
for name,phr in phrases():
    parts=[];starts=[];lens=[];t=0.0
    for i,p in enumerate(phr):
        a,_=k.create(sp(p),voice="af_heart",speed=0.95,lang="en-us")
        idx=np.where(np.abs(a)>0.01)[0];a=a[max(0,idx[0]-120):idx[-1]+900]
        starts.append(round(t,3));lens.append(round(len(a)/SR,3));parts.append(a);t+=len(a)/SR
        if i<len(phr)-1: parts.append(np.zeros(int(GAP*SR),dtype=a.dtype));t+=GAP
    sf.write(f"vo_{name}.wav",np.concatenate(parts),SR)
    words=[]
    for p,s,l in zip(phr,starts,lens):
        ws=p.split(); w8=[len(w)+2 for w in ws]; tot=sum(w8); c=s+0.05
        for w,wt in zip(ws,w8):
            d=(l-0.1)*wt/tot; words.append([w,round(c,3),round(c+d,3)]); c+=d
    meta[name]={"starts":starts,"lens":lens,"len":round(t,3),"words":words}
    print(name,round(t,1),flush=True)
json.dump(meta,open("vo.json","w"),indent=1); print('TOTAL',round(sum(v['len'] for v in meta.values()),1))
