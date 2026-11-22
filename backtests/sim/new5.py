# Five indicators rebuilt as signal generators (FX data has no volume: volume weights = 1, volume filters skipped):
#  vrb   VWAP Range Breakout (Zeiierman): breakouts, retests, inner-band arrows, X fakeouts; Smart Trend as context
#  trap  Smart Money Bull/Bear Trap Detector (BigBeluga): pivot (10) wick-through-and-close-back within 35 bars
#  asr   Auto Support & Resistance: clustered pivot levels; wick-through bounce or close-through break
#  lsrt  Liquidity Sweep Reversal & Targets (PhenLabs), Balanced profile, its own SL/TP/BE/time rules available
#  swc   Swing Clock (GBB): 2.5 ATR zigzag; new swing confirmed = signal; swing direction as context; median-extension target
# Each returns dict(sig, slp, tpx, ctx): sig = entry direction on that bar's close, slp/tpx = indicator stop/target (nan if none),
# ctx = context state (+1/-1/0) usable as filter or exit.
import sys, os, math, statistics as St
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smc import B, cost_of, pip_of
NAN = float('nan')
_c = {}
def _arr(b):
    return (np.array([x['o'] for x in b]), np.array([x['h'] for x in b]), np.array([x['l'] for x in b]), np.array([x['c'] for x in b]))
def _rma_atr(h, l, c, n):
    N = len(c); tr = np.empty(N); tr[0] = h[0] - l[0]; tr[1:] = np.maximum(h[1:], c[:-1]) - np.minimum(l[1:], c[:-1])
    a = np.full(N, np.nan)
    if N >= n:
        a[n - 1] = tr[:n].mean()
        for i in range(n, N): a[i] = (a[i - 1] * (n - 1) + tr[i]) / n
    return a
def _sma(x, n):
    o = np.full(len(x), np.nan); cs = np.cumsum(np.nan_to_num(x)); o[n - 1:] = (cs[n - 1:] - np.concatenate([[0], cs[:-n]])) / n; return o
def _out(N): return dict(sig=np.zeros(N, int), slp=np.full(N, np.nan), tpx=np.full(N, np.nan), ctx=np.zeros(N, int))

def vrb(b, kind):
    o, h, l, c = _arr(b); N = len(c); R = _out(N); hl3 = (h + l + c) / 3
    base = _sma(hl3, 3); eq = _sma(hl3, 20); res = hl3 - eq; dev = np.sqrt(np.maximum(0, _sma(res * res, 100)))
    width = np.maximum(dev * 4.0, np.maximum(np.abs(h - base), np.abs(l - base)) + 1e-9)
    seed = _sma(hl3, 34) * 34
    atr = _rma_atr(h, l, c, 14); aS = _rma_atr(h, l, c, 56); aM = _sma(np.nan_to_num(atr), 120)
    aD = np.array([np.std(atr[max(0, i - 119):i + 1]) if i >= 133 else np.nan for i in range(N)])
    trVW = _sma(hl3, 200)
    mid = hi = lo = hiM = loM = np.nan; sPV = sV = np.nan
    HI = np.full(N, np.nan); LO = np.full(N, np.nan); MID = np.full(N, np.nan); RV = np.full(N, np.nan)
    tHi = tLo = np.nan; dr = 0; dprev = 0; rPV = rV = np.nan; up = dn = 0; trend = 0
    brDir = 0; brLvl = np.nan; brBar = 0
    for i in range(N):
        ready = i >= 100 and not np.isnan(width[i]) and not np.isnan(base[i])
        brUp = i >= 2 and not np.isnan(HI[i - 1]) and l[i] > HI[i - 1] and (np.isnan(HI[i - 2]) or l[i - 1] <= HI[i - 2])
        brDn = i >= 2 and not np.isnan(LO[i - 1]) and h[i] < LO[i - 1] and (np.isnan(LO[i - 2]) or h[i - 1] >= LO[i - 2])
        new = ready and (np.isnan(mid) or brUp or brDn)
        steady = not new and not np.isnan(mid) and i >= 1 and MID[i - 1] == mid
        if new:
            mid = base[i]; hi = mid + width[i]; lo = mid - width[i]; hiM = (mid + hi) / 2; loM = (mid + lo) / 2; sPV = seed[i]; sV = 34.0
        elif not np.isnan(sPV): sPV += hl3[i]; sV += 1
        HI[i], LO[i], MID[i] = hi, lo, mid; RV[i] = sPV / sV if not np.isnan(sPV) else np.nan
        # smart trend
        if not np.isnan(trVW[i]) and not np.isnan(aD[i]) and not np.isnan(aS[i]):
            z = (atr[i] - aM[i]) / aD[i] if aD[i] > 0 else 0.0; vr = atr[i] / aS[i] if aS[i] > 0 else 1.0
            x = 4 * (vr - 1) + 0.75 * max(-3, min(3, z)); step = atr[i] * 1.5 * (0.5 + 1.5 / (1 + math.exp(-x)))
            if np.isnan(tHi): tHi = trVW[i]; tLo = trVW[i] - step; dr = 1
            else:
                eu = trVW[i] > tHi + step; ed = trVW[i] < tLo - step; nd = 1 if eu else -1 if ed else dr
                if eu or ed:
                    ref = tHi if nd == 1 else tLo; st = max(1, int(abs(trVW[i] - ref) // step))
                    if nd == 1: tLo = tHi + (st - 1) * step; tHi = tHi + st * step
                    else: tHi = tLo - (st - 1) * step; tLo = tLo - st * step
                    dr = nd
            flip = dprev != 0 and dr != dprev
            if flip or np.isnan(rPV): rPV = hl3[i]; rV = 1.0
            else: rPV += hl3[i]; rV += 1
            rev = rPV / rV; rv = RV[i]
            ua = dr == 1 and c[i] > rv and c[i] > rev + atr[i] * 0.05; da = dr == -1 and c[i] < rv and c[i] < rev - atr[i] * 0.05
            up = up + 1 if ua else 0; dn = dn + 1 if da else 0
            if flip: trend = 0
            if up >= 2: trend = 1
            elif dn >= 2: trend = -1
            elif trend == 1 and (dr != 1 or c[i] < rev - atr[i] * 0.15): trend = 0
            elif trend == -1 and (dr != -1 or c[i] > rev + atr[i] * 0.15): trend = 0
            dprev = dr
        R['ctx'][i] = trend
        if i < 2 or np.isnan(atr[i]): continue
        A = atr[i]; s = 0
        # retests (after a breakout)
        ret = 0
        if brUp or brDn: brDir = 1 if brUp else -1; brLvl = HI[i - 1] if brUp else LO[i - 1]; brBar = i
        elif brDir != 0:
            if i - brBar > 12: brDir = 0
            else:
                tol = A * 0.15
                if brDir == 1 and brLvl - tol <= l[i] <= brLvl + tol and c[i] > brLvl and c[i] > o[i]: ret = 1
                if brDir == -1 and brLvl - tol <= h[i] <= brLvl + tol and c[i] < brLvl and c[i] < o[i]: ret = -1
                if ret: brDir = 0
        if kind == 'breakout' and (brUp or brDn):
            s = 1 if brUp else -1; R['slp'][i] = (HI[i - 1] if brUp else LO[i - 1]) - s * 0.2 * A
        elif kind == 'retest' and ret:
            s = ret; R['slp'][i] = (l[i] if s > 0 else h[i]) - s * 0.1 * A
        elif kind in ('arrow', 'fake') and steady:
            if kind == 'arrow':
                if l[i] > loM and l[i - 1] <= loM: s = 1
                elif h[i] < hiM and h[i - 1] >= hiM: s = -1
            else:
                if l[i] > lo and l[i - 1] <= lo: s = 1          # failed lower excursion
                elif h[i] < hi and h[i - 1] >= hi: s = -1
            if s: R['slp'][i] = (min(l[i - 3:i + 1].min(), lo) if s > 0 else max(h[i - 3:i + 1].max(), hi)) - s * 0.2 * A; R['tpx'][i] = hi if s > 0 else lo
        R['sig'][i] = s
    return R

def trap(b, kind, L=10, zlen=35):
    o, h, l, c = _arr(b); N = len(c); R = _out(N); atr = _rma_atr(h, l, c, 14); act = []
    for i in range(N):
        if i >= 2 * L:
            k = i - L
            if h[k] == h[k - L:i + 1].max() and h[k] > h[k - L:k].max(): act.append([h[k], k, True])
            if l[k] == l[k - L:i + 1].min() and l[k] < l[k - L:k].min(): act.append([l[k], k, False])
        s = 0; keep = []
        for lv in act:
            age = i - lv[1]
            if age > zlen: continue
            if lv[2] and h[i] > lv[0] and c[i] < lv[0]:
                if kind == 'all' or age <= zlen / 3: s = -1; R['slp'][i] = h[i]
                continue
            if not lv[2] and l[i] < lv[0] and c[i] > lv[0]:
                if kind == 'all' or age <= zlen / 3: s = 1; R['slp'][i] = l[i]
                continue
            keep.append(lv)
        act = keep
        if s and not np.isnan(atr[i]): R['sig'][i] = s; R['slp'][i] -= s * 0.1 * atr[i]
    return R

def asr(b, kind, rb=10, prd=284, cl=10.0, strength=2):
    o, h, l, c = _arr(b); N = len(c); R = _out(N); atr = _rma_atr(h, l, c, 14)
    piv = []; levels = []
    for i in range(N):
        prev = levels
        newp = False
        if i >= 2 * rb:
            k = i - rb
            if h[k] == h[k - rb:i + 1].max() and h[k] > h[k - rb:k].max(): piv.append((i, h[k])); newp = True
            if l[k] == l[k - rb:i + 1].min() and l[k] < l[k - rb:k].min(): piv.append((i, l[k])); newp = True
        if newp and i >= 300:
            cw = (h[i - 299:i + 1].max() - l[i - 299:i + 1].min()) * cl / 100
            P = [pv for pv in reversed(piv) if pv[0] >= i - prd][:40]; used = [False] * len(P); lv = []
            for x, (_, px) in enumerate(P):
                if used[x]: continue
                hit = [j for j, (_, q) in enumerate(P) if not used[j] and px - cw <= q <= px + cw]
                if len(hit) >= strength:
                    for j in hit: used[j] = True
                    lv.append(px)
            levels = lv
        if i < 1 or np.isnan(atr[i]) or not prev: continue
        A = atr[i]; s = 0
        for lvl in prev:
            if kind == 'bounce':
                if l[i] < lvl < c[i]: s = 1; R['slp'][i] = l[i] - 0.1 * A
                elif h[i] > lvl > c[i]: s = -1; R['slp'][i] = h[i] + 0.1 * A
            else:
                if c[i] > lvl >= c[i - 1]: s = 1; R['slp'][i] = lvl - 0.3 * A
                elif c[i] < lvl <= c[i - 1]: s = -1; R['slp'][i] = lvl + 0.3 * A
            if s: break
        if s:
            beyond = [q for q in prev if s * (q - c[i]) > 0]
            if beyond: R['tpx'][i] = min(beyond, key=lambda q: abs(q - c[i]))
            R['sig'][i] = s
    return R

def lsrt(b, kind, L=10):
    o, h, l, c = _arr(b); N = len(c); R = _out(N); atr = _rma_atr(h, l, c, 14); ssl = []; bsl = []
    for i in range(N):
        A = atr[i] if not np.isnan(atr[i]) else max(h[i] - l[i], 1e-9); span = max(h[i] - l[i], 1e-12)
        act = min(max(span / A / 2, 0), 1)
        bAbs = (0.5 * (c[i] - l[i]) / span + 0.35 * act + 0.15 * (1 if c[i] >= o[i] else 0.65)) * 100
        sAbs = (0.5 * (h[i] - c[i]) / span + 0.35 * act + 0.15 * (1 if c[i] <= o[i] else 0.65)) * 100
        bull = bear = None; ns = []
        for p in ssl:
            if c[i] < p[1] or l[i] < p[0] - 2 * A: continue
            if l[i] < p[0] and c[i] >= p[0]:
                if bull is None or p[0] < bull[0]: bull = p
                continue
            ns.append(p)
        ssl = ns; nb = []
        for p in bsl:
            if c[i] > p[1] or h[i] > p[0] + 2 * A: continue
            if h[i] > p[0] and c[i] <= p[0]:
                if bear is None or p[0] > bear[0]: bear = p
                continue
            nb.append(p)
        bsl = nb
        if bull and bear: bull = bear = None
        if i >= 2 * L:
            k = i - L; z = A * 0.35
            if h[k] == h[k - L:i + 1].max() and h[k] > h[k - L:k].max():
                out_ = h[k] + z * 0.65
                if not (c[k + 1:i + 1] > out_).any(): bsl.append((h[k], out_)); bsl = bsl[-8:]
            if l[k] == l[k - L:i + 1].min() and l[k] < l[k - L:k].min():
                out_ = l[k] - z * 0.65
                if not (c[k + 1:i + 1] < out_).any(): ssl.append((l[k], out_)); ssl = ssl[-8:]
        if np.isnan(atr[i]) or i < 5: continue
        mv5 = (c[i] - c[i - 5]) / A
        if bull and (l[i] and (bull[0] - l[i]) / A <= 1.5) and (kind == 'all' or bAbs >= 55) and not (mv5 < -3.6 and c[i] < o[i]):
            R['sig'][i] = 1; R['slp'][i] = min(l[i], bull[1]) - 0.2 * A
            mags = [p[0] for p in bsl]; R['tpx'][i] = min(mags) if mags else np.nan
        elif bear and (h[i] - bear[0]) / A <= 1.5 and (kind == 'all' or sAbs >= 55) and not (mv5 > 3.6 and c[i] > o[i]):
            R['sig'][i] = -1; R['slp'][i] = max(h[i], bear[1]) + 0.2 * A
            mags = [p[0] for p in ssl]; R['tpx'][i] = max(mags) if mags else np.nan
    return R

def swc(b, kind, K=2.5):
    o, h, l, c = _arr(b); N = len(c); R = _out(N); atr = _rma_atr(h, l, c, 14)
    started = False; d = 1; p0 = pe = deep = atr0 = atre = np.nan; ext = {1: [], -1: []}; sid = 0
    for i in range(N):
        if np.isnan(atr[i]): continue
        if not started: started = True; d = 1; p0 = l[i]; pe = h[i]; deep = c[i]; atr0 = atre = atr[i]; continue
        hi_, lo_, cl_ = (h[i], l[i], c[i]) if d > 0 else (-l[i], -h[i], -c[i])
        peU, deepU = pe * d, deep * d
        if hi_ > peU: peU = hi_; atre = atr[i]; deepU = cl_
        else: deepU = min(deepU, lo_)
        pe, deep = peU * d, deepU * d
        if peU - deepU >= K * atre:
            sid += 1
            if sid > 2: ext[d].append(d * (pe - p0) / atr0)
            nd = -d; p0n = pe; atr0 = atre; pe = deep; deep = c[i]; atre = atr[i]; d = nd; p0 = p0n
            R['sig'][i] = d; R['slp'][i] = p0 - d * 0.1 * atr[i]
            past = ext[d][-60:]
            if len(past) >= 10: R['tpx'][i] = p0 + d * St.median(past) * atr0
        R['ctx'][i] = d
    return R

KINDS = {'vrb': ['breakout', 'retest', 'arrow', 'fake'], 'trap': ['all', 'fresh'], 'asr': ['bounce', 'break'],
         'lsrt': ['balanced', 'all'], 'swc': ['new']}
FN = dict(vrb=vrb, trap=trap, asr=asr, lsrt=lsrt, swc=swc)
def get(name, kind, b):
    key = (name, kind, id(b), len(b))
    if key not in _c: _c[key] = FN[name](b, kind)
    return _c[key]

DEF = dict(ind='vrb', kind='breakout', sl='atr', slk=1.0, tpR=3, tp='R', trail=0, t2=0, be=None, tmax=0, cx=False, bias=True, hours=None, native=False)
def run(p, b, P, start, end):
    P = {**DEF, **P}; cost = cost_of(p) * pip_of(p); S = get(P['ind'], P['kind'], b)
    if P['native']: P.update(sl='ind', tp='mag', be=1, tmax=60)
    res = []; pos = None
    for i in range(1, len(b)):
        x = b[i]; A = x['atr']
        if pos:
            d = pos['d']; px = None
            if (x['l'] <= pos['sl']) if d > 0 else (x['h'] >= pos['sl']): px = min(x['o'], pos['sl']) if d > 0 else max(x['o'], pos['sl']); why = 'SL'
            elif pos['tp'] and ((x['h'] >= pos['tp']) if d > 0 else (x['l'] <= pos['tp'])): px = max(x['o'], pos['tp']) if d > 0 else min(x['o'], pos['tp']); why = 'TP'
            elif P['cx'] and S['ctx'][i] == -d: px = x['c']; why = 'ctx'
            elif P['tmax'] and i - pos['i'] >= P['tmax']: px = x['c']; why = 'time'
            elif S['sig'][i] == -d and pos['bias_ok'] is False: px = x['c']; why = 'flip'
            if px is not None:
                res.append(dict(p=p, d=d, t=pos['t'], tx=x['tc'], wk=pos['wk'], R=d * (px - pos['e']) / pos['r'] - cost / pos['r'], why=why)); pos = None
            else:
                pos['best'] = max(pos['best'], d * ((x['h'] if d > 0 else x['l']) - pos['e']))
                if P['be'] is not None and pos['best'] >= P['be'] * pos['r'] and d * (pos['sl'] - pos['e']) < 0: pos['sl'] = pos['e']
                if P['trail'] and pos['best'] >= 0:
                    k = P['t2'] if P['t2'] and pos['best'] >= 2 * pos['r'] else P['trail']
                    ns = x['c'] - d * k * A; pos['sl'] = max(pos['sl'], ns) if d > 0 else min(pos['sl'], ns)
        s = S['sig'][i]
        if pos or A is None or not s or not (start <= x['t'] < end): continue
        bi_ = B.get((p, x['wk']), ('-',))[0]; bd = 1 if bi_ == 'U' else -1 if bi_ == 'D' else 0
        if P['bias'] and bd != s: continue
        if P['hours'] and not (P['hours'][0] <= x['hr'] < P['hours'][1]): continue
        e = x['c']
        if P['sl'] == 'ind' and not np.isnan(S['slp'][i]): r = abs(e - S['slp'][i])
        else: r = P['slk'] * A
        r = min(max(r, 0.35 * A), 3 * A) if P['sl'] == 'ind' else r
        if r <= 0 or s * (e - (e - s * r)) <= 0: continue
        tp = e + s * P['tpR'] * r if P['tpR'] else None
        if P['tp'] in ('ind', 'mag') and not np.isnan(S['tpx'][i]):
            dR = s * (S['tpx'][i] - e) / r
            if (P['tp'] == 'ind' and dR >= 1) or (P['tp'] == 'mag' and 2.2 <= dR <= 4.5): tp = S['tpx'][i]
        pos = dict(i=i, d=s, e=e, r=r, sl=e - s * r, tp=tp, t=x['t'], wk=x['wk'], best=0, bias_ok=True)
    return res

def ctx_state(name, b):
    """Context for filters/exits: vrb smart trend, swc swing direction; others: last signal direction (held 12 bars)."""
    if name in ('vrb', 'swc'): return get(name, KINDS[name][0], b)['ctx']
    sig = get(name, KINDS[name][0], b)['sig']; out = np.zeros(len(sig), int); last = 0; age = 99
    for i, s in enumerate(sig):
        if s: last, age = s, 0
        else: age += 1
        out[i] = last if age <= 12 else 0
    return out

if __name__ == '__main__':
    from harness import go
    X = [('SL1 TP3', dict()), ('SL1.5 TP3', dict(slk=1.5)), ('ind SL, TP3', dict(sl='ind')), ('ind SL, TP2', dict(sl='ind', tpR=2)),
         ('ind SL, ind target', dict(sl='ind', tp='ind')), ('your exit', dict(tpR=4, trail=0.75, t2=0.5))]
    only = sys.argv[1:] or list(KINDS)
    for name in only:
        for k in KINDS[name]:
            print(f"== {name}: {k}", flush=True)
            xs = X + ([('native LSRT rules', dict(native=True))] if name == 'lsrt' else []) + \
                 ([('exit on context flip', dict(tpR=0, sl='ind', cx=True))] if name in ('vrb', 'swc') else [])
            for xn, P in xs: print(f"  {xn:<22} {go(run, {'ind': name, 'kind': k, **P})}", flush=True)
