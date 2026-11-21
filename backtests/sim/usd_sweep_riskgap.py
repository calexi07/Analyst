import sys, os, collections; sys.argv=['x']
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'usd_sweep_research.py')).read().replace("os.path.dirname(os.path.abspath(__file__))","os.path.dirname(os.path.abspath(__file__))").split("b0 = evalP")[0])
Q={**BASE}; t=sorted(sum([run(p,data[p],B,Q,H[0][0],H[1][1],usd) for p in USD],[]),key=lambda x:x['tx'])
for name,w in [('flat 1%',lambda x:1),('1.5% if |gap|>=8, else 1%',lambda x:1.5 if x['gap'] is not None and abs(x['gap'])>=8 else 1),('1.5% if |gap|>=8, 0.75% if <5',lambda x:1.5 if x['gap'] is not None and abs(x['gap'])>=8 else 0.75 if x['gap'] is None or abs(x['gap'])<5 else 1)]:
    eq=pk=dd=0; wk=collections.defaultdict(float); h1=h2=0
    for x in t:
        r=x['R']*w(x); eq+=r; pk=max(pk,eq); dd=min(dd,eq-pk); wk[x['wk'][1]]+=r
        if x['wk'][1]<=43: h1+=r
        else: h2+=r
    ws=[wk.get(k,0) for k in range(40,48)]
    print(f"{name:<32} {h1:+.1f}/{h2:+.1f} = {eq:+.1f}%  maxDD {dd:+.1f}%  2wk {[round(ws[i]+ws[i+1],1) for i in range(0,8,2)]}")
