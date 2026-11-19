import re,json
P=["EURUSD","GBPUSD","USDJPY","USDCHF","USDCAD","AUDUSD","NZDUSD","EURGBP","EURJPY","EURCHF","EURAUD","EURNZD","EURCAD","GBPJPY","GBPCHF","GBPAUD","GBPNZD","GBPCAD","AUDJPY","AUDCHF","AUDNZD","AUDCAD","NZDJPY","NZDCHF","NZDCAD","CADJPY","CADCHF","CHFJPY","XAUUSD"]
FL={'✅':'✓ green','🟡':'✓ green','👀':'! amber','⚠️':'! amber','❌':'✗ red','⚪':'– grey'}
def arr(h,name):
    k=h.index(name); v,_=json.JSONDecoder().raw_decode(h[k+len(name):]); return v
num=lambda x:int(x.replace('−','-').replace('+',''))
def build(notes, meta, ccy):
    pairs=[]
    for pair,note in zip(P,notes):
        status=re.search(r'\[quote\]\[b\](.+?)\[/b\]',note).group(1)
        hook=re.search(r'\[/b\]\n\n\[b\](.+?)\[/b\]',note); hook=hook.group(1) if hook else ''
        bias=re.search(r'Week bias: (\w[\w-]*)',note).group(1).lower()
        m=re.search(r"Published gap ([+−-]?\d+) → today's read ([^\[\n]+)",note)
        pg=num(m.group(1)); read=m.group(2).strip()
        tg=re.match(r'([+−-]?\d+)',read); tg=num(tg.group(1)) if tg else None
        flag=next((v for k,v in FL.items() if status.startswith(k)),'')
        pairs.append(dict(pair=pair,status=status,bias=bias,published_gap=pg,today_gap=tg,read=read,flag=flag,hook=hook,note=note))
    return dict(format='daily-observer-check',version=1,**meta,currencies=ccy,pairs=pairs)
