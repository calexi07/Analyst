import json, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro
k=Kokoro("/home/claude/tts/kokoro-v1.0.onnx","/home/claude/tts/voices-v1.0.bin"); SR=24000
SC={
"q1":["have held gold, or the US dollar, for one week?","It's Friday, November sixth. Gold just jumped five percent in a week, and markets are scared.","The dollar has the Fed talking about more rate hikes.","A, gold. B, the dollar. Comment your answer."],
"r1":["Here's what happened.","Gold fell about four point seven percent. Hot US inflation pushed yields up, and a metal that pays no interest suffered.","The dollar was the strongest currency of the week, up about one percent against the others."],
"q2":["Next one, for the chart people. Price just broke higher. Would you rather enter on the fair value gap, or on the order block?","A, the fair value gap: the empty space three candles leave behind in a fast move.","B, the order block: the last down candle before the big push up.","A, F V G. B, order block. Comment your pick."],
"r2":["There's no winner on every chart.","The fair value gap usually sits closer to price, so it often gets tested first. But it's thin, and price can slice straight through it.","The order block sits deeper. You wait longer and might miss the move, but many traders see it as the stronger zone.","When both line up, even better. And the fundamental bias tells you which direction to look in."],
"q3":["Last one. Would you rather have held the Swiss franc, or the New Zealand dollar, that same week?","The franc pays zero percent, but it's the classic safe haven when markets are scared.","The kiwi pays two point seven five percent, but the country just voted and the result isn't final.","A, the franc. B, the kiwi. Tell me in the comments."],
"r3":["The franc was the weakest currency of the week, down about one and a half percent. Markets calmed down, so nobody needed a hiding place.","The kiwi finished second, up about zero point seven percent. Markets liked the election result."],
"outro":["Follow FX Before Coffee. Not a trade signal.","Now that you know... would you rather"]}
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
