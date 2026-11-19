import json, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro
k=Kokoro("/home/claude/tts/kokoro-v1.0.onnx","/home/claude/tts/voices-v1.0.bin"); SR=24000
SC={
"hook":["Charts show you where price went.","Fundamentals tell you why."],
"what":["So what is fundamental analysis?","A currency is a share in a country's economy.","We look at four things: interest rates, inflation, jobs and growth, and politics.","When those change, the value of the currency changes too."],
"rates":["Interest rates matter most.","Big money goes where it gets paid more.","If one currency pays four percent and another pays zero, investors prefer the first one.","That's why traders watch every central bank meeting."],
"surprise":["But here's the key.","Markets already price what they expect.","Only the surprise moves the price.","In October, US inflation was forecast at zero point three percent, and came in at zero point four. That small surprise lifted the dollar."],
"mood":["Then there's the mood.","When investors are scared, money runs to safe havens: the Swiss franc, the yen and gold.","When they're calm, it goes to currencies that pay more, like the Australian dollar.","The same news can mean different things in a different mood."],
"tug":["Every forex pair is a tug of war.","You're never buying just one economy, you're comparing two.","So we score both sides, and the gap between them shows which way the fundamentals lean."],
"proof":["Does it work?","In our model's week forty-six, all seven dollar pairs moved the way the fundamentals pointed.","But the franc pairs failed, because the market's mood changed after our forecast.","One week proves nothing. We track it for twenty-six weeks before judging."],
"limits":["What fundamentals are not.","They're not a timing tool, and not a trade signal.","Fundamentals give you the direction of pressure. The chart tells you when.","And risk management decides how much."],
"recap":["So remember three things.","Rates move money.","Surprises move prices.","And mood can flip the story."],
"outro":["Follow FX Before Coffee.","Not a trade signal."]}
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
