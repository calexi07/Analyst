# "Rolling Candle Profile with Buy/Sell Signals (Zeiierman)" — Price Pressure mode on the chart timeframe (defaults:
# EMA21 anchor, width 0.01, wick 0.85, dominance 0.25, min 7 coloured bands, spacing 6). Rebuilt bar by bar with numpy.
import sys, os, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smc import B, cost_of, pip_of
cl = lambda x, a, b: max(a, min(b, x))
_cache = {}
def signals(b, alen=21, dom=0.25, minb=7, gap=6, wickW=0.85, pxw=0.01):
    key = (id(b), alen, dom, minb, gap)
    if key in _cache: return _cache[key]
    n = len(b); o = np.array([x['o'] for x in b]); h = np.array([x['h'] for x in b]); l = np.array([x['l'] for x in b]); c = np.array([x['c'] for x in b])
    ema = np.zeros(n); k_ = 2 / (alen + 1); ema[0] = c[0]
    for i in range(1, n): ema[i] = ema[i - 1] + k_ * (c[i] - ema[i - 1])
    buy = np.zeros(n); sell = np.zeros(n); lrej = np.zeros(n); hrej = np.zeros(n); stall = np.zeros(n); tot = np.zeros(n)
    bC = np.zeros(n); sC = np.zeros(n); lC = np.zeros(n); hC = np.zeros(n); stC = np.zeros(n)
    for i in range(n):
        r = max(h[i] - l[i], 1e-9); pc = c[i - 1] if i else o[i]
        d = cl((c[i] - o[i]) / r, -1, 1); trv = cl((c[i] - pc) / r, -1.5, 1.5); loc = cl((2 * c[i] - h[i] - l[i]) / r, -1, 1)
        resp = cl(0.55 * trv + 0.25 * d + 0.20 * loc, -1.5, 1.5); f = abs(resp)
        prior = (c[i - 1] - c[i - 2]) if i >= 2 else 0.0
        cont = 1.45 if prior * resp > 0 else 0.55 if prior * resp < 0 else 1.0
        buy[i] = max(resp, 0) * (1 + f * 1.25) * cont * 2; sell[i] = max(-resp, 0) * (1 + f * 1.25) * cont * 2
        lw = max(0, min(o[i], c[i]) - l[i]) / r; hw = max(0, h[i] - max(o[i], c[i])) / r
        lrej[i] = lw * (0.35 + 1.2 * max(resp, 0)); hrej[i] = hw * (0.35 + 1.2 * max(-resp, 0)); stall[i] = (1 - cl(f, 0, 1)) * 0.2
        hl3 = (h[i] + l[i] + c[i]) / 3
        bC[i] = c[i] * 0.7 + h[i] * 0.3; sC[i] = c[i] * 0.7 + l[i] * 0.3
        lC[i] = (l[i] + min(o[i], c[i])) / 2 if lrej[i] > 0 else l[i]; hC[i] = (h[i] + max(o[i], c[i])) / 2 if hrej[i] > 0 else h[i]; stC[i] = hl3
        tot[i] = buy[i] + sell[i] + lrej[i] + hrej[i] + stall[i]
    base = np.zeros(n); k2 = 2 / 56; base[0] = tot[0]
    for i in range(1, n): base[i] = base[i - 1] + k2 * (tot[i] - base[i - 1])
    fs = np.where(tot > 0, np.minimum(1.0, np.maximum(base, 1e-6) * 20 / np.where(tot > 0, tot, 1)), 1.0)
    buy *= fs; sell *= fs; lrej *= fs; hrej *= fs; stall *= fs
    atr = np.array([x['atr'] if x['atr'] is not None else np.nan for x in b])
    age = 0.5 ** (np.arange(60) / 3)
    bw = (h - l) * pxw
    def ker(here, ctr, invW):   # here: (12,1) ctr,invW: (60,)
        q = 1 - np.abs(here - ctr) * invW
        return np.where(q <= 0, 0, q * q * (3 - 2 * q))
    sig = [0] * n; lastB = lastS = -10 ** 9; prevBA = prevSA = False
    for i in range(n):
        bl, bh = min(o[i], c[i]), max(o[i], c[i]); a = ema[i]
        edge = bl if a < bl else bh if a > bh else None
        ba = sa = False
        if i >= 62 and edge is not None and not np.isnan(atr[i]) and abs(edge - a) > 1e-9:
            dist = (edge - a) / 12; here = (a + dist * (np.arange(12) + 0.5))[:, None]
            ks = slice(i - 59, i + 1)          # k = 0..59 -> reversed order
            sl_ = np.arange(i, i - 60, -1)
            minW = abs(dist) * 1.15; minWW = abs(dist) * 1.0
            invW = 1 / np.maximum(np.maximum(bw[sl_], minW), 1e-12); invWW = 1 / np.maximum(np.maximum(bw[sl_] * 0.6, minWW), 1e-12)
            bf = (buy[sl_] * ker(here, bC[sl_], invW) * age).sum(1) + wickW * (lrej[sl_] * ker(here, lC[sl_], invWW) * age).sum(1)
            sf = (sell[sl_] * ker(here, sC[sl_], invW) * age).sum(1) + wickW * (hrej[sl_] * ker(here, hC[sl_], invWW) * age).sum(1)
            t = bf + sf
            imb = np.where(t > 0, np.clip((bf - sf) / np.where(t > 0, t, 1) * 3, -1, 1), 0)
            act = np.clip(t / (max(base[i], 1e-6) * 0.8), 0, 1)
            vis = (act >= 0.08) & (np.abs(imb) >= 0.14)
            vb = int(vis.sum()); pb = bf[vis].sum(); ps = sf[vis].sum()
            nb = int((vis & (imb > 0.03)).sum()); ns = int((vis & (imb < -0.03)).sum())
            hasP = vb >= minb and pb + ps > 0
            if hasP:
                bias = (pb - ps) / (pb + ps)
                rising = i > 0 and ema[i] > ema[i - 1]; falling = i > 0 and ema[i] < ema[i - 1]
                ba = c[i] > a and rising and bias >= dom and nb > ns
                sa = c[i] < a and falling and bias <= -dom and ns > nb
        if ba and not prevBA and i - lastB >= gap: sig[i] = 1; lastB = i
        if sa and not prevSA and i - lastS >= gap: sig[i] = -1; lastS = i
        prevBA, prevSA = ba, sa
    _cache[key] = (sig, ema)
    return sig, ema

DEF = dict(sl='atr', slk=1.0, tpR=3, trail=0, tract=0, opp=False, bias=True, hours=None, maxR=3, dom=0.25, minb=7, alen=21)
def run(p, b, P, start, end):
    P = {**DEF, **P}; cost = cost_of(p) * pip_of(p); sig, ema = signals(b, P['alen'], P['dom'], P['minb'])
    res = []; pos = None
    for i, x in enumerate(b):
        A = x['atr']
        if pos:
            d = pos['d']; px = None
            if (x['l'] <= pos['sl']) if d > 0 else (x['h'] >= pos['sl']): px = min(x['o'], pos['sl']) if d > 0 else max(x['o'], pos['sl']); why = 'SL'
            elif pos['tp'] and ((x['h'] >= pos['tp']) if d > 0 else (x['l'] <= pos['tp'])): px = max(x['o'], pos['tp']) if d > 0 else min(x['o'], pos['tp']); why = 'TP'
            elif P['opp'] and sig[i] == -d: px = x['c']; why = 'opp'
            if px is not None:
                res.append(dict(p=p, d=d, t=pos['t'], tx=x['tc'], wk=pos['wk'], R=d * (px - pos['e']) / pos['r'] - cost / pos['r'], why=why)); pos = None
            else:
                pos['best'] = max(pos['best'], d * ((x['h'] if d > 0 else x['l']) - pos['e']))
                if P['trail'] and pos['best'] >= P['tract'] * pos['r']:
                    k = P['trail'] if not P.get('t2') or pos['best'] < 2 * pos['r'] else P['t2']
                    ns = x['c'] - d * k * A; pos['sl'] = max(pos['sl'], ns) if d > 0 else min(pos['sl'], ns)
        if pos or A is None or not sig[i] or not (start <= x['t'] < end): continue
        d = sig[i]
        bi_ = B.get((p, x['wk']), ('-',))[0]; bd = 1 if bi_ == 'U' else -1 if bi_ == 'D' else 0
        if P['bias'] and bd != d: continue
        if P['hours'] and not (P['hours'][0] <= x['hr'] < P['hours'][1]): continue
        e = x['c']
        r = P['slk'] * A if P['sl'] == 'atr' else abs(e - ema[i]) + 0.2 * A if P['sl'] == 'anchor' else abs(e - (x['l'] if d > 0 else x['h'])) + 0.1 * A
        if not (0.3 * A <= r <= P['maxR'] * A): continue
        pos = dict(d=d, e=e, r=r, sl=e - d * r, tp=e + d * P['tpR'] * r if P['tpR'] else None, t=x['t'], wk=x['wk'], best=0)
    return res
if __name__ == '__main__':
    from harness import go
    V = [('default signals, SL 1 ATR, TP 3R', {}),
         ('  TP 2R', dict(tpR=2)), ('  TP 4R', dict(tpR=4)),
         ('  SL beyond EMA21 anchor, TP 3R', dict(sl='anchor')),
         ('  SL beyond signal candle, TP 3R', dict(sl='bar')),
         ('  SL 1.5 ATR, TP 3R', dict(slk=1.5)),
         ('  your exit: TP 4R, trail 0.75 -> 0.5 after 2R', dict(tpR=4, trail=0.75, t2=0.5)),
         ('  no TP, exit on opposite signal', dict(tpR=0, opp=True)),
         ('  TP 3R or opposite signal', dict(opp=True)),
         ('dominance 0.40', dict(dom=0.4)),
         ('min bands 10', dict(minb=10)),
         ('anchor EMA 50', dict(alen=50))]
    for n, P in V: print(f"{n:<46} {go(run, P)}", flush=True)
