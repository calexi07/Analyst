import json, os, collections, statistics as S
rows = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'usd_full.json')))
f = lambda r, k: f"{r[k]['n']:3}tr {r[k]['h1']:+5.1f}/{r[k]['h2']:+5.1f} dd{r[k]['dd']:+5.1f}"
print('== Best per entry (bias direction, both halves > 0, ranked by total) ==')
for en in sorted(set(r['entry'] for r in rows)):
    c = [r for r in rows if r['entry'] == en]
    best = max(c, key=lambda r: (min(r['bias']['h1'], r['bias']['h2']) > 0, r['bias']['R']))
    print(f"{en:6} cf={best['cf']:4} opens={best['opens']:4} {best['fri']:<30} bias {f(best,'bias')} = {best['bias']['R']:+5.1f}R | both {best['both']['R']:+5.1f}R | 3y trend {best['trend']['R']:+6.1f}R {best['trend']['y']}")
print('\n== Median effect (bias direction) ==')
for k in ['entry', 'cf', 'opens', 'fri']:
    g = collections.defaultdict(list); g2 = collections.defaultdict(list)
    for r in rows: g[r[k]].append(r['bias']['R']); g2[r[k]].append(r['trend']['R'])
    print(k, {a: (round(S.median(v), 1), round(S.median(g2[a]), 1)) for a, v in g.items()}, '(bias weeks, 3y trend)')
print('\n== Top 12 overall on bias weeks with both halves > 0 ==')
for r in sorted([r for r in rows if min(r['bias']['h1'], r['bias']['h2']) > 0], key=lambda r: -r['bias']['R'])[:12]:
    print(f"{r['entry']:6} cf={r['cf']:4} opens={r['opens']:4} {r['fri']:<30} bias {f(r,'bias')} = {r['bias']['R']:+5.1f}R | 3y trend {r['trend']['R']:+6.1f}R {r['trend']['y']} dd{r['trend']['dd']}")
print('\n== Top 8 on 3 years (trend), positive every year ==')
for r in sorted([r for r in rows if min(r['trend']['y']) > 0], key=lambda r: -r['trend']['R'])[:8]:
    print(f"{r['entry']:6} cf={r['cf']:4} opens={r['opens']:4} {r['fri']:<30} 3y {r['trend']['R']:+6.1f}R {r['trend']['y']} dd{r['trend']['dd']} | bias {f(r,'bias')} = {r['bias']['R']:+5.1f}R")
