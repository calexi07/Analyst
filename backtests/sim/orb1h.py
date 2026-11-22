# London opening-range breakout on the 1H path, all 14 pairs: range = the 09:00-10:00 Bucharest candle, stop order beyond it
# in the bias direction from 10:00 until 13:00, stop at the other side (or the middle), exit at TP or after N hours.
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness
from smc import B, H, cost_of, pip_of
B.clear(); B.update(harness.B1)
def run(p, b, P, start, end):
    cost = cost_of(p) * pip_of(p); res = []; i = 0
    while i < len(b):
        x = b[i]
        if not (start <= x['t'] < end) or x['hr'] != P.get('h0', 9): i += 1; continue
        bi = B.get((p, x['wk']), ('-',))[0]; d = 1 if bi == 'U' else -1 if bi == 'D' else 0
        if d == 0 or x['dow'] > 4: i += 1; continue
        hi, lo = x['h'], x['l']; e = hi if d > 0 else lo; sl = (lo if d > 0 else hi) if P.get('sl', 'range') == 'range' else (hi + lo) / 2
        r = abs(e - sl); pos = None; j = i + 1
        while j < len(b) and b[j]['day'] == x['day'] and b[j]['hr'] < P.get('until', 13):
            y = b[j]
            if (y['h'] >= e) if d > 0 else (y['l'] <= e):
                ee = max(y['o'], e) if d > 0 else min(y['o'], e); rr = abs(ee - sl); pos = (j, ee, rr); break
            j += 1
        if pos:
            j, ee, rr = pos; tp = ee + d * P.get('tp', 2) * rr; px = None; k = j
            if (b[j]['l'] <= sl) if d > 0 else (b[j]['h'] >= sl): px = sl
            while px is None and k + 1 < len(b):
                k += 1; y = b[k]
                if (y['l'] <= sl) if d > 0 else (y['h'] >= sl): px = min(y['o'], sl) if d > 0 else max(y['o'], sl)
                elif (y['h'] >= tp) if d > 0 else (y['l'] <= tp): px = max(y['o'], tp) if d > 0 else min(y['o'], tp)
                elif k - j >= P.get('tmax', 4): px = y['c']
            if px is not None and rr > 0: res.append(dict(p=p, d=d, t=b[j]['t'], tx=b[k]['tc'], wk=x['wk'], R=d * (px - ee) / rr - cost / rr))
        i = j + 1 if pos else i + 1
    return res
if __name__ == '__main__':
    ALL = list(harness.D1)
    for P in [dict(tp=1.5), dict(tp=2), dict(tp=3), dict(tp=2, tmax=3), dict(tp=2, sl='mid'), dict(tp=2, tmax=6), dict(tp=2, h0=10, until=14), dict(tp=2, h0=8, until=12), dict(tp=2, h0=15, until=18)]:
        hs = [sum([run(p, harness.D1[p], P, a, c) for p in ALL], []) for a, c in H]
        t = hs[0] + hs[1]; pp = collections.defaultdict(float)
        for x in t: pp[x['p']] += x['R']
        tot = sum(x['R'] for x in t)
        print(f"{str(P):<40} {len(t)}tr {tot/len(t):+.2f}R/tr {sum(x['R'] for x in hs[0]):+.1f}/{sum(x['R'] for x in hs[1]):+.1f} = {tot:+.1f}R  pairs+ {sum(v>0 for v in pp.values())}/{len(pp)}  " + ' '.join(f"{k[:6]}{v:+.0f}" for k, v in sorted(pp.items(), key=lambda kv: -kv[1])))
