import json, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro
k=Kokoro("/home/claude/tts/kokoro-v1.0.onnx","/home/claude/tts/voices-v1.0.bin"); SR=24000
SC={
"hook":["Next week in forex, in one minute.","The fear is gone, and that changes the whole board."],
"mood":["First, the mood.","Last week markets were scared. Now they're calm.","US stocks are only down about one percent in four weeks, and the fear index closed at nineteen point three.","When markets are calm, safe havens lose their support."],
"dollar":["The US dollar still leads, at plus five.","October inflation came in hot: plus zero point four percent in the month, against zero point three expected.","A December Fed hike now looks about ninety-one percent likely.","Some Fed officials even talk about a bigger move."],
"winners":["Who gained?","The British pound jumped from minus three to plus one.","The Australian dollar rose to plus three. It pays the highest interest rate of the eight.","And the New Zealand dollar climbed to plus one, helped by dairy prices."],
"losers":["Who lost?","The Swiss franc fell from zero to minus three. It pays zero percent, and nobody needs a hiding place right now.","The yen dropped to zero.","And the Canadian dollar is still last, at minus four, with oil down about thirteen percent in four weeks."],
"gold":["Gold's own score turned negative.","From plus seven to minus three.","US real yields rose, from two point seven four to two point eight six percent.","Gold pays no interest, so that hurts. Central banks are still buying, which is its main support."],
"board":["Here's the full board for next week.","Dollar on top, then the Aussie, the pound and the kiwi.","The euro and the franc at minus three, the Canadian dollar at the bottom."],
"pairs":["The widest gaps.","Dollar against the Canadian dollar, plus nine.","Dollar against the Swiss franc, plus eight.","And the euro against the dollar, minus eight."],
"week":["What to watch next week.","Monday, Canadian inflation.","Tuesday and Wednesday, UK jobs and UK inflation, plus the Fed minutes on Wednesday evening.","Thursday, Australian jobs. Friday, Japanese inflation."],
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
json.dump(meta,open("vo.json","w"),indent=1); print(list(meta), round(sum(v['len'] for v in meta.values()),1))
