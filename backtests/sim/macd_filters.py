# BE MACD (1H, bias, any cross, SL 1.5 ATR, TP 3R): entry filters and exit tweaks, 14 pairs W40-W47, halves
import harness, numpy as np, bisect
from smc import H, cost_of, pip_of
from macd import macd
from zoneinfo import ZoneInfo
BUC = ZoneInfo('Europe/Bucharest')
def ema(a, n):
    o = np.empty(len(a)); k = 2 / (n + 1); o[0] = a[0]
    for i in range(1, len(a)): o[i] = o[i-1] + k * (a[i] - o[i-1])
    return o
def adx(b, n=14):
    N = len(b); pdm = np.zeros(N); ndm = np.zeros(N); tr = np.zeros(N)
    for i in range(1, N):
        up = b[i]['h'] - b[i-1]['h']; dn = b[i-1]['l'] - b[i]['l']
        pdm[i] = up if up > dn and up > 0 else 0; ndm[i] = dn if dn > up and dn > 0 else 0
        tr[i] = max(b[i]['h'], b[i-1]['c']) - min(b[i]['l'], b[i-1]['c'])
    def rma(a):
        o = np.zeros(N); v = a[1:n+1].mean() if N > n else 0
        for i in range(N): v = v if i <= n else (v * (n - 1) + a[i]) / n; o[i] = v
        return o
    atr_ = rma(tr); pdi = 100 * rma(pdm) / np.where(atr_ == 0, 1, atr_); ndi = 100 * rma(ndm) / np.where(atr_ == 0, 1, atr_)
    dx = 100 * np.abs(pdi - ndi) / np.where(pdi + ndi == 0, 1, pdi + ndi); return rma(dx)
PRE = {}
for p in harness.ALL:
    b = harness.D1[p]; c = np.array([x['c'] for x in b]); m, sg, hs = macd(b)
    b4 = harness.D4[p]; m4, s4, h4 = macd(b4); t4 = [x['tc'] if 'tc' in x else x['t'] for x in b4]
    PRE[p] = dict(m=m, hs=hs, e200=ema(c, 200), e50=ema(c, 50), adx=adx(b), h4=h4, t4=t4)
def run(flt=None, be=None, part=None, conv=None, tp=3.0, k=1.5):
    out = []
    for p in harness.ALL:
        b = harness.D1[p]; P = PRE[p]; hs = P['hs']; cost = cost_of(p) * pip_of(p); i = 30
        while i < len(b) - 1:
            x = b[i]; i += 1
            if not any(s <= x['t'] < e for s, e in H) or np.isnan(hs[i-2]): continue
            r_ = harness.B1.get((p, x['wk']))
            if not r_ or r_[0] not in 'UD': continue
            if conv and r_[1] not in conv: continue
            d = 1 if r_[0] == 'U' else -1; j = i - 1
            if not (hs[j] * d > 0 and hs[j-1] * d <= 0): continue
            h = x['t'].astimezone(BUC).hour
            if not (6 <= h < 22) or not x['atr']: continue
            if flt == 'ema200' and (x['c'] - P['e200'][j]) * d <= 0: continue
            if flt == 'ema50' and (x['c'] - P['e50'][j]) * d <= 0: continue
            if flt == 'zero_trend' and P['m'][j] * d <= 0: continue
            if flt == 'zero_pullback' and P['m'][j] * d >= 0: continue
            if flt == 'adx20' and P['adx'][j] < 20: continue
            if flt == 'adx_low' and P['adx'][j] >= 25: continue
            if flt in ('h4', 'h4_against'):
                q = bisect.bisect_right(P['t4'], x['t']) - 1
                if q < 1 or np.isnan(P['h4'][q]): continue
                if flt == 'h4' and P['h4'][q] * d <= 0: continue
                if flt == 'h4_against' and P['h4'][q] * d > 0: continue
            if flt == 'london_ny' and not (9 <= h < 19): continue
            e = x['c']; r = k * x['atr']; sl = e - d * r; tg = e + d * tp * r; res = None; half = 0; stop = sl
            for q in range(i, len(b)):
                y = b[q]
                if (y['l'] <= stop) if d > 0 else (y['h'] >= stop): res = half * part[1] + (1 - half) * d * (stop - e) / r if part else d * (stop - e) / r; break
                if part and not half and ((y['h'] >= e + d * part[0] * r) if d > 0 else (y['l'] <= e + d * part[0] * r)):
                    half = 0.5; stop = e
                if (y['h'] >= tg) if d > 0 else (y['l'] <= tg): res = (half * part[0] + (1 - half) * tp) if part else tp; break
                if be and ((y['h'] >= e + d * be * r) if d > 0 else (y['l'] <= e + d * be * r)): stop = e if d > 0 and stop < e or d < 0 and stop > e else stop
            if res is None: res = d * (b[-1]['c'] - e) / r
            out.append((x['t'], p, res - cost / r)); i = q + 1
    return out
def st(o, lab):
    R = [z[2] for z in o]; n = len(R); h1 = sum(z[2] for z in o if z[0] < H[0][1]); eu = [z[2] for z in o if z[1] == 'EURUSD']
    print(f"{lab:44} {n:4d}tr {sum(R):+6.1f}R {sum(R)/max(1,n):+.2f}/tr win {sum(r>0 for r in R)/max(1,n):.0%} halves {h1:+5.1f}/{sum(R)-h1:+5.1f} | EURUSD {len(eu)}tr {sum(eu):+.1f}R")
st(run(), "BASE (any cross, 1.5 ATR, TP 3R)")
for f in ['ema200', 'ema50', 'zero_trend', 'zero_pullback', 'adx20', 'adx_low', 'h4', 'h4_against', 'london_ny']:
    st(run(f), f"filter {f}")
st(run(conv=('h', 'm')), "conviction medium/high")
st(run(conv=('h',)), "conviction high")
for be in [1.0, 1.5, 2.0]: st(run(be=be), f"break-even after +{be}R")
for pr in [(1.5, 0), (2.0, 0)]: st(run(part=pr), f"half at +{pr[0]}R, rest SL→entry, TP3")
for tp in [2.0, 4.0, 5.0]: st(run(tp=tp), f"TP {tp}R")
st(run(k=2.0), "SL 2.0 ATR")
print('--- EMA length neighbourhood')
for n in [100, 150, 200, 250, 300]:
    for p in harness.ALL:
        c = np.array([x['c'] for x in harness.D1[p]]); PRE[p]['e200'] = ema(c, n)
    st(run('ema200'), f"filter EMA{n} (1H)")
    if n == 200:
        for tp in [4.0, 5.0]: st(run('ema200', tp=tp), f"EMA200 + TP {tp}R")
