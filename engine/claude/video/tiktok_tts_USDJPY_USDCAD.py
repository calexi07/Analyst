import json, sys, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro
k = Kokoro("/home/claude/tts/kokoro-v1.0.onnx", "/home/claude/tts/voices-v1.0.bin")
SR=24000
OUTRO=["Follow FX Before Coffee for the next check, every morning.", "Big picture only. Not a trade signal."]
ALL={
"jpy":{
 "hook":["Bulls versus bears, on dollar yen.", "Who's in control this week?"],
 "monday":["Monday. Our weekly analysis.", "The model sided with the dollar, with a medium lean.",
   "The dollar had strong US jobs behind it, and a Fed still talking about raising rates.",
   "The yen had its own shields. In nervous markets, money hides in the yen. And Tokyo had warned it could step in to support it."],
 "tuesday":["Tuesday. Two twists.", "US prices rose faster than expected. Good for the dollar.",
   "But the Bank of Japan's meeting notes also hinted at a rate hike in December. Good for the yen."],
 "thursday":["Thursday morning. Today's check.",
   "Japan's top currency official warned that the yen's moves have been excessively rapid. A reminder of the interventions this summer.",
   "In America, traders now see about a ninety-one percent chance of a December rate hike."],
 "verdict":["So, where does that leave dollar yen?", "The dollar still leads. But this one is under watch.",
   "If markets bet harder on a Japanese rate hike in December, the dollar's edge could almost disappear.",
   "Next: US producer prices on Friday. Then Japan's growth numbers, next week."],
 "outro":OUTRO},
"cad":{
 "hook":["Bulls versus bears: the US dollar against the Canadian dollar.", "Who's in control this week?"],
 "monday":["Monday. Our weekly analysis.", "The model sided with the US dollar. And this is the widest gap on our whole board.",
   "The US dollar had strong jobs behind it, and a Fed still talking about raising rates.",
   "Canada had everything going wrong at once. Oil, its key export, was down about six percent in a month. Canada lost jobs when economists expected gains. And the US tariff threat was still there."],
 "tuesday":["Tuesday. US prices rose faster than expected.", "That made a December rate hike more likely, and gave the US dollar extra support."],
 "thursday":["Thursday morning. Today's check.",
   "Oil kept sliding. Prices dipped again overnight, and an industry estimate showed US crude stocks rising by about nine million barrels.",
   "More supply and weaker oil is not what Canada needs.",
   "In America, traders now see about a ninety-one percent chance of a December rate hike."],
 "verdict":["So, where does that leave the Canadian dollar?", "The US dollar still leads, by a wide margin.",
   "Canada needs oil to bounce back, or a trade deal with the US, to change the story.",
   "Next: US producer prices, and a fresh oil market report, on Friday."],
 "outro":OUTRO}}
for key,SC in ALL.items():
  meta={}
  for name,phr in SC.items():
    parts=[];starts=[];t=0.0
    for i,p in enumerate(phr):
        a,_=k.create(p,voice="af_heart",speed=1.0,lang="en-us")
        idx=np.where(np.abs(a)>0.01)[0];a=a[max(0,idx[0]-240):idx[-1]+1200]
        starts.append(round(t,3));parts.append(a);t+=len(a)/SR
        if i<len(phr)-1: parts.append(np.zeros(int(0.38*SR),dtype=a.dtype));t+=0.38
    full=np.concatenate(parts);sf.write(f"{key}/vo_{name}.wav",full,SR);meta[name]={"starts":starts,"len":round(len(full)/SR,3)}
  json.dump(meta,open(f"{key}/vo.json","w"),indent=1);print(key,{k2:v['len'] for k2,v in meta.items()},sum(v['len'] for v in meta.values()))
