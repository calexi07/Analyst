# Multi-timeframe Quasimodo on EURUSD: the QM's head (the swept extreme) must form inside a higher-timeframe point of interest.
# POIs (built from completed 1H / 4H candles only):
#   zone  fractal demand/supply: 2/2 pivot candle followed within 3 candles by a 1.5 ATR displacement; zone = wick to body;
#         live from its displacement candle until a close beyond its far edge (mitigated) - head must trade into it
#   fvg   unfilled fair value gap (gap between candle 1 high and candle 3 low) in the trade direction; head must trade into it
#   disc  head in the discount (long) / premium (short) half of the last 48 HTF candles' range
#   pdl   head swept yesterday's low (long) / high (short)
#   atr   regime: daily ATR(5) / ATR(20) above 1 (expanding) or below 1 (contracting), at the head
import sys, os, bisect, datetime as Dt
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qm, ltf
from smc import prep, B, H
import harness
from harness import B1, D4
B.clear(); B.update(B1)
h1 = harness.D1['EURUSD']; h4 = D4['EURUSD']   # harness.D1 is the real 1H (prep() is patched to 4H once smc_3y is imported)
def zones(hb, kind):
    out = []   # (dir, live_from, dead_at or None, top, bottom)
    n = len(hb)
    for k in range(2, n - 3):
        A = hb[k]['atr']
        if not A: continue
        if kind == 'zone':
            for s in (1, -1):
                piv = (hb[k]['l'] < min(hb[k - 1]['l'], hb[k - 2]['l'], hb[k + 1]['l'], hb[k + 2]['l'])) if s > 0 else (hb[k]['h'] > max(hb[k - 1]['h'], hb[k - 2]['h'], hb[k + 1]['h'], hb[k + 2]['h']))
                if not piv: continue
                j = next((j for j in range(k + 1, min(n, k + 4)) if (hb[j]['h'] - hb[k]['h'] if s > 0 else hb[k]['l'] - hb[j]['l']) >= 1.5 * A), None)
                if j is None: continue
                top, bot = (max(hb[k]['o'], hb[k]['c']), hb[k]['l']) if s > 0 else (hb[k]['h'], min(hb[k]['o'], hb[k]['c']))
                live = hb[max(j, k + 2)]['tc']
                dead = next((hb[q]['tc'] for q in range(max(j, k + 2) + 1, n) if (hb[q]['c'] < bot if s > 0 else hb[q]['c'] > top)), None)
                out.append((s, live, dead, top, bot))
        else:   # fvg between k-1 and k+1
            for s in (1, -1):
                if s > 0 and hb[k + 1]['l'] > hb[k - 1]['h']: top, bot = hb[k + 1]['l'], hb[k - 1]['h']
                elif s < 0 and hb[k + 1]['h'] < hb[k - 1]['l']: top, bot = hb[k - 1]['l'], hb[k + 1]['h']
                else: continue
                if top - bot < 0.1 * A: continue
                live = hb[k + 1]['tc']
                dead = next((hb[q]['tc'] for q in range(k + 2, n) if (hb[q]['l'] <= bot if s > 0 else hb[q]['h'] >= top)), None)
                out.append((s, live, dead, top, bot))
    return out
Z = {(tf, k): zones(hb, k) for tf, hb in (('1H', h1), ('4H', h4)) for k in ('zone', 'fvg')}
def in_zone(key, tol=0.0):
    zs = Z[key]
    def f(d, th, hp, now):
        for s, live, dead, top, bot in zs:
            if s != d or live > th or (dead is not None and dead <= th): continue
            if (hp <= top and hp >= bot - tol * (top - bot)) if d > 0 else (hp >= bot and hp <= top + tol * (top - bot)): return True
        return False
    return f
hT = [x['tc'] for x in h1]
def disc(n=48):
    def f(d, th, hp, now):
        j = bisect.bisect_right(hT, th) - 1
        if j < n: return False
        hi = max(x['h'] for x in h1[j - n + 1:j + 1]); lo = min(x['l'] for x in h1[j - n + 1:j + 1]); mid = (hi + lo) / 2
        return hp < mid if d > 0 else hp > mid
    return f
# daily bars from 1H
days = {}
for x in h1: days.setdefault(x['day'], []).append(x)
dk = sorted(days); dH = {d: max(x['h'] for x in days[d]) for d in dk}; dL = {d: min(x['l'] for x in days[d]) for d in dk}
dC = {d: days[d][-1]['c'] for d in dk}
def pdl():
    def f(d, th, hp, now):
        ny = (th + Dt.timedelta(hours=7)).astimezone(ltf.NY).date()
        i = bisect.bisect_left(dk, ny)
        if i < 1: return False
        y = dk[i - 1]
        return hp < dL[y] if d > 0 else hp > dH[y]
    return f
tr = {}
for i, d in enumerate(dk):
    tr[d] = dH[d] - dL[d] if i == 0 else max(dH[d], dC[dk[i - 1]]) - min(dL[d], dC[dk[i - 1]])
def atrreg(expand=True):
    def f(d, th, hp, now):
        ny = (th + Dt.timedelta(hours=7)).astimezone(ltf.NY).date(); i = bisect.bisect_left(dk, ny)
        if i < 21: return False
        a5 = np.mean([tr[q] for q in dk[i - 5:i]]); a20 = np.mean([tr[q] for q in dk[i - 20:i]])
        return (a5 > a20) == expand
    return f
def anyof(*fs): return lambda *a: any(g(*a) for g in fs)
DATA = {'15m': ltf.load('EURUSD', '15'), '5m': ltf.load('EURUSD', '5')}
BASE = {'15m': dict(L=3, entry='half', tpR=3, slb=0.1, hours=(6, 22), maxR=6, cancel1R=False),
        '5m': dict(L=2, entry='break', tpR=4, slb=0.1, hours=(6, 22), maxR=6, cancel1R=False)}
def ev(tf, P):
    hs = [qm.run('EURUSD', DATA[tf], P, a, c) for a, c in H]
    t = sorted(hs[0] + hs[1], key=lambda x: x['tx']); eq = pk = dd = 0
    for x in t: eq += x['R']; pk = max(pk, eq); dd = min(dd, eq - pk)
    n = max(1, len(t))
    return f"{len(t):3}tr {len(t)/8:.1f}/wk win {sum(x['R'] > 0 for x in t)/n:.0%} {eq/n:+.2f}R/tr | {sum(x['R'] for x in hs[0]):+5.1f}/{sum(x['R'] for x in hs[1]):+5.1f} = {eq:+5.1f}R dd {dd:+4.1f}"
V = [('no POI (current BE QM)', None), ('1H demand/supply zone', in_zone(('1H', 'zone'), 0.5)), ('4H demand/supply zone', in_zone(('4H', 'zone'), 0.5)),
     ('1H unfilled FVG', in_zone(('1H', 'fvg'), 0.5)), ('4H unfilled FVG', in_zone(('4H', 'fvg'), 0.5)),
     ('1H zone or FVG, or 4H zone or FVG', anyof(in_zone(('1H', 'zone'), 0.5), in_zone(('4H', 'zone'), 0.5), in_zone(('1H', 'fvg'), 0.5), in_zone(('4H', 'fvg'), 0.5))),
     ('discount/premium of last 48 x 1H', disc(48)), ('head swept yesterday low/high', pdl()),
     ('daily ATR expanding', atrreg(True)), ('daily ATR contracting', atrreg(False)),
     ('discount + any zone/FVG', lambda *a: disc(48)(*a) and anyof(in_zone(('1H', 'zone'), 0.5), in_zone(('4H', 'zone'), 0.5), in_zone(('1H', 'fvg'), 0.5), in_zone(('4H', 'fvg'), 0.5))(*a))]
for tf in ('15m', '5m'):
    print(f"== {tf} ({'pivot 3, half-way limit, TP 3R' if tf == '15m' else 'pivot 2, break entry, TP 4R'})")
    for n, f in V:
        print(f"  {n:<36} bias: {ev(tf, {**BASE[tf], 'poi': f})}   || no bias: {ev(tf, {**BASE[tf], 'poi': f, 'bias': False})}", flush=True)
