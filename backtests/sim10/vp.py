# Volume profile from tick volume (10y 15m, 12 instruments): daily profile (broker day ≈ Bucharest day).
# Each 15m bar spreads its volume evenly over the price bins its range covers; bin = 1/40 of the day's average range (ADR14).
# Profile levels per day: POC (max-volume bin), Value Area 70% grown out from the POC (VAH / VAL).
# Ideas tested on the NEXT day: (1) 80% rule, (2) rejection at yesterday's VAH/VAL, (3) naked POC as a magnet,
# (4) trend pullback to yesterday's VAH/VAL (acceptance retest), (5) trend pullback to yesterday's POC.
import sys, collections, math
sys.path.insert(0, '/home/claude/analyst/backtests/sim10')
from absorb import loadv

def profiles(b):
    days = collections.OrderedDict()
    for i, x in enumerate(b): days.setdefault(x['t'].date(), []).append(i)
    ks = [k for k in days if k.weekday() < 5 and len(days[k]) >= 60]
    rngs = []; out = collections.OrderedDict()
    for k in ks:
        ix = days[k]; hi = max(b[i]['h'] for i in ix); lo = min(b[i]['l'] for i in ix)
        adr = sum(rngs[-14:]) / len(rngs[-14:]) if rngs else hi - lo
        rngs.append(hi - lo)
        step = max(adr / 40, 1e-9); n = int((hi - lo) / step) + 1; vol = [0.0] * n
        for i in ix:
            x = b[i]; a = int((x['l'] - lo) / step); z = int((x['h'] - lo) / step); z = min(z, n - 1)
            share = x['v'] / (z - a + 1)
            for q in range(a, z + 1): vol[q] += share
        poc = max(range(n), key=lambda q: vol[q]); tot = sum(vol); lo_i = hi_i = poc; acc = vol[poc]
        while acc < 0.7 * tot and (lo_i > 0 or hi_i < n - 1):
            up = vol[hi_i + 1] if hi_i < n - 1 else -1; dn = vol[lo_i - 1] if lo_i > 0 else -1
            if up >= dn: hi_i += 1; acc += up
            else: lo_i -= 1; acc += dn
        out[k] = dict(ix=ix, poc=lo + (poc + 0.5) * step, vah=lo + (hi_i + 1) * step, val=lo + lo_i * step,
                      hi=hi, lo=lo, o=b[ix[0]]['o'], c=b[ix[-1]]['c'], adr=adr)
    return out

def manage(b, j0, jend, d, e, s, t, cost):
    r = abs(e - s)
    for j in range(j0, jend + 1):
        y = b[j]
        if (y['l'] <= s) if d > 0 else (y['h'] >= s): return -1.0 - cost / r
        if t is not None and ((y['h'] >= t) if d > 0 else (y['l'] <= t)): return abs(t - e) / r - cost / r
    return d * (b[jend]['c'] - e) / r - cost / r

def run(b, P, idea, cost, dirf=None, w=(480, 1200), tp=None, buf=0.1):
    ks = list(P); out = []
    for a, k in zip(ks, ks[1:]):
        y, T = P[a], P[k]; ix = T['ix']; end = ix[-1]
        D_ = dirf(k) if dirf else (1, -1)
        if not D_: continue
        A = y['adr']
        if idea == '80':
            o = T['o']; side = 1 if o > y['vah'] else -1 if o < y['val'] else 0
            if not side: continue
            inside = 0; ext = o
            for q, i in enumerate(ix):
                x = b[i]; ext = max(ext, x['h']) if side > 0 else min(ext, x['l'])
                m = x['t'].hour * 60 + x['t'].minute
                if m >= w[1]: break
                ins = y['val'] < x['c'] < y['vah']; inside = inside + 1 if ins else 0
                if inside >= 4:          # two 30m periods = four 15m closes inside the value area
                    d = -side
                    if d not in D_: break
                    e = x['c']; s = ext + side * buf * A; t = y['val'] if d < 0 else y['vah']
                    if tp: t = e + d * tp * abs(e - s)
                    if abs(e - s) <= 0 or (t - e) * d <= 0: break
                    out.append((x['t'], manage(b, i + 1, end, d, e, s, t, cost))); break
        elif idea in ('reject', 'accept'):
            done = False; poke = {1: None, -1: None}
            for i in ix:
                x = b[i]; m = x['t'].hour * 60 + x['t'].minute
                if m >= w[1]: break
                if m < w[0]: continue
                for side, lvl in ((1, y['vah']), (-1, y['val'])):
                    if idea == 'reject':
                        if (x['h'] > lvl) if side > 0 else (x['l'] < lvl):
                            poke[side] = max(poke[side] or x['h'], x['h']) if side > 0 else min(poke[side] or x['l'], x['l'])
                        if poke[side] is not None and ((x['c'] < lvl) if side > 0 else (x['c'] > lvl)) and (x['t'].minute == 45):   # 1H close back inside
                            d = -side
                            if d not in D_: poke[side] = None; continue
                            e = x['c']; s = poke[side] + side * buf * A; t = y['poc'] if not tp else e + d * tp * abs(e - s)
                            if (t - e) * d <= 0 or abs(e - s) <= 0: poke[side] = None; continue
                            out.append((x['t'], manage(b, i + 1, end, d, e, s, t, cost))); done = True; break
                    else:   # acceptance retest: price opened/was beyond the edge, comes back to touch it from outside
                        d = side
                        if d not in D_: continue
                        if (T['o'] - lvl) * side > 0.2 * A and ((x['l'] <= lvl) if side > 0 else (x['h'] >= lvl)):
                            e = lvl; s = lvl - d * 0.5 * A; t = e + d * (tp or 2) * abs(e - s)
                            hit = (x['l'] <= s) if d > 0 else (x['h'] >= s)
                            out.append((x['t'], -1.0 - cost / abs(e - s) if hit else manage(b, i + 1, end, d, e, s, t, cost))); done = True; break
                if done: break
        elif idea == 'poc_pb':      # trend pullback to yesterday's POC (from the trend side)
            for d in D_:
                if (T['o'] - y['poc']) * d <= 0.2 * A: continue
                for i in ix:
                    x = b[i]; m = x['t'].hour * 60 + x['t'].minute
                    if m >= w[1]: break
                    if (x['l'] <= y['poc']) if d > 0 else (x['h'] >= y['poc']):
                        e = y['poc']; s = e - d * 0.5 * A; t = e + d * (tp or 2) * abs(e - s)
                        hit = (x['l'] <= s) if d > 0 else (x['h'] >= s)
                        out.append((x['t'], -1.0 - cost / abs(e - s) if hit else manage(b, i + 1, end, d, e, s, t, cost))); break
    return out

def naked_poc(b, P, horizon=5):
    """share of POCs touched within `horizon` days vs a control level at the same distance on the other side of the close"""
    ks = list(P); hit = ctl = n = 0
    for q in range(len(ks) - horizon):
        y = P[ks[q]]; c = y['c']; lv = y['poc']; dist = abs(lv - c)
        if dist < 0.1 * y['adr']: continue
        mirror = c - (lv - c); n += 1
        fut = [P[ks[q + z]] for z in range(1, horizon + 1)]
        if any(f['lo'] <= lv <= f['hi'] for f in fut): hit += 1
        if any(f['lo'] <= mirror <= f['hi'] for f in fut): ctl += 1
    return n, hit / max(1, n), ctl / max(1, n)
