import json, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro
k = Kokoro("/home/claude/tts/kokoro-v1.0.onnx", "/home/claude/tts/voices-v1.0.bin")
SR=24000
SC = {
 "hook":   ["Here's what moved currency markets overnight,", "and what it means for today."],
 "fed":    ["First, the US Federal Reserve.", "Two senior officials, Mary Daly and John Williams, both said more rate hikes are likely.", "Their reason: inflation is still too high."],
 "yields": ["Markets listened.", "The US ten-year yield climbed to about five point one percent.", "And a December rate hike is now seen as almost certain.", "Higher rates usually make the dollar more attractive."],
 "euro":   ["In Europe, the gap between French and German borrowing costs widened again,", "to about one hundred forty-seven basis points.", "It shows investors are still nervous about France's budget, and that weighs on the euro."],
 "yen":    ["In Asia, the dollar touched one hundred sixty yen.", "That's the level where Japan stepped in to support its currency before.", "So Tokyo warned again against one-sided moves."],
 "oil":    ["Oil jumped more than three percent, to almost ninety-six dollars,", "after reported attacks on Saudi energy sites and tankers in the Gulf.", "Higher oil helps the Canadian dollar, but one day doesn't change the trend."],
 "gold":   ["Gold fell about six percent in three days,", "to its lowest level since October twenty twenty-five.", "When US yields rise, a metal that pays no interest looks less attractive."],
 "verdict":["So, did anything change in our model?", "No. Our scores stayed the same.", "The US dollar still leads at plus seven, and the Canadian dollar is last at minus six."],
 "today":  ["Today, watch two things.", "Euro-area growth data at ten GMT, and US producer prices at one thirty GMT.", "A hot inflation reading would add more fuel to the dollar."],
 "outro":  ["Follow FX Before Coffee.", "Not a trade signal."],
}
GAP=0.5; meta={}
for name,phr in SC.items():
    parts=[];starts=[];lens=[];t=0.0
    for i,p in enumerate(phr):
        a,_=k.create(p,voice="af_heart",speed=0.95,lang="en-us")
        idx=np.where(np.abs(a)>0.01)[0];a=a[max(0,idx[0]-120):idx[-1]+900]
        starts.append(round(t,3));lens.append(round(len(a)/SR,3));parts.append(a);t+=len(a)/SR
        if i<len(phr)-1: parts.append(np.zeros(int(GAP*SR),dtype=a.dtype));t+=GAP
    full=np.concatenate(parts);sf.write(f"vo_{name}.wav",full,SR)
    words=[]
    for p,s,l in zip(phr,starts,lens):
        ws=p.split(); w8=[len(w)+2 for w in ws]; tot=sum(w8); c=s+0.05
        for w,wt in zip(ws,w8):
            d=(l-0.1)*wt/tot; words.append([w,round(c,3),round(c+d,3)]); c+=d
    meta[name]={"starts":starts,"len":round(len(full)/SR,3),"words":words}
json.dump(meta,open("vo.json","w"),indent=1); print({k2:v['len'] for k2,v in meta.items()}, sum(v['len'] for v in meta.values()))
