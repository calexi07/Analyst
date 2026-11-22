# LuxAlgo "Smart Money Concepts" structure (leg / BOS / CHoCH / internal OB) rebuilt on 5m, as entries.
# Instruments with 5m exports: EURUSD, GBPUSD, XAUUSD, GER40 (Aug-Nov 2026). Direction: weekly bias (FX/gold), daily SMA20 trend, or none.
import sys, os, collections, datetime as D
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import intraday as T
from smc import B, H, cost_of, pip_of
import harness
B.clear(); B.update(harness.B1)
def structure(b, s):
    """events: list of (i, kind, dir, pivot_index) kind = 'CHoCH' or 'BOS'"""
    n = len(b); leg = None; ph = pl = None; phc = plc = True; trend = 0; ev = []
    for i in range(s, n):
        hi = max(x['h'] for x in b[i-s+1:i+1]); lo = min(x['l'] for x in b[i-s+1:i+1])
        nl = leg
        if b[i-s]['h'] > hi: nl = 0
        elif b[i-s]['l'] < lo: nl = 1
        if nl != leg and leg is not None:
            if nl == 0: ph = (b[i-s]['h'], i - s); phc = False
            else: pl = (b[i-s]['l'], i - s); plc = False
        leg = nl
        c, c1 = b[i]['c'], b[i-1]['c']
        if ph and not phc and c > ph[0] and c1 <= ph[0]:
            ev.append((i, 'CHoCH' if trend == -1 else 'BOS', 1, ph[1])); phc = True; trend = 1
        if pl and not plc and c < pl[0] and c1 >= pl[0]:
            ev.append((i, 'CHoCH' if trend == 1 else 'BOS', -1, pl[1])); plc = True; trend = -1
    return ev
def atr(b, n=14):
    A = None
    for i, x in enumerate(b):
        tr = x['h'] - x['l'] if i == 0 else max(x['h'], b[i-1]['c']) - min(x['l'], b[i-1]['c'])
        A = tr if A is None else (A * (n - 1) + tr) / n; x['atr'] = A
def run(p, data, s=5, mode='choch', dirm='bias', tp=2.0, w=(540, 1080), tmax=48, ob_valid=24):
    b5, prevd, _ = data; cost = cost_of(p) * pip_of(p); out = []
    if 'atr' not in b5[0]: atr(b5)
    ev = structure(b5, s); lastday = None
    for i, kind, d, pv in ev:
        x = b5[i]
        if not (w[0] <= x['m'] < w[1]) or x['lt'].weekday() > 4: continue
        if mode.startswith('choch') and kind != 'CHoCH': continue
        if mode.startswith('bos') and kind != 'BOS': continue
        if lastday == x['cd']: continue    # one trade a day per instrument
        bi = B.get((p, x['wk']), ('-',))[0]; bd = 1 if bi == 'U' else -1 if bi == 'D' else 0
        sm = prevd.get(x['day'], {}).get('sma'); td = 0 if sm is None else (1 if x['c'] > sm else -1)
        want = {'bias': (bd,), 'trend': (td,), 'both': (1, -1), 'bias+trend': (bd,) if bd == td else ()}[dirm]
        if d not in want or d == 0: continue
        seg = b5[pv:i+1]
        if mode.endswith('_ob'):    # LuxAlgo internal OB: the bar with the lowest low (bull) / highest high (bear) of the leg
            k = min(range(len(seg)), key=lambda j: seg[j]['l']) if d > 0 else max(range(len(seg)), key=lambda j: seg[j]['h'])
            ob = seg[k]; e = ob['h'] if d > 0 else ob['l']; sl = (ob['l'] if d > 0 else ob['h']) - d * 0.1 * x['atr']
            fill = None
            for j in range(i + 1, min(len(b5), i + 1 + ob_valid)):
                y = b5[j]
                if y['cd'] != x['cd'] or y['m'] >= 21 * 60: break
                if (y['l'] <= e) if d > 0 else (y['h'] >= e): fill = j; break
            if fill is None: continue
            j0 = fill
        else:
            e = x['c']; sl = (min(y['l'] for y in seg) if d > 0 else max(y['h'] for y in seg)) - d * 0.1 * x['atr']; j0 = i + 1
        r = abs(e - sl)
        if r <= 0 or r > 6 * x['atr'] or r < 0.5 * x['atr']: continue
        t = e + d * tp * r; res = None
        for j in range(j0, min(len(b5), j0 + tmax)):
            y = b5[j]
            if (y['l'] <= sl) if d > 0 else (y['h'] >= sl): res = -1; break
            if (y['h'] >= t) if d > 0 else (y['l'] <= t): res = tp; break
            if y['m'] >= 21 * 60 + 45 or y['cd'] != x['cd']: res = d * (y['c'] - e) / r; break
        if res is None: j = min(len(b5) - 1, j0 + tmax); res = d * (b5[j]['c'] - e) / r
        out.append((x['t'], res - cost / r)); lastday = x['cd']
    return out
if __name__ == '__main__':
    def st(o):
        R = [r for _, r in o]; n = len(R)
        if not n: return '   0tr'
        mid = o[0][0] + (o[-1][0] - o[0][0]) / 2; h1 = sum(r for t, r in o if t < mid)
        return f"{n:3d}tr {sum(R):+5.1f}R {sum(R)/n:+.2f}/tr ({h1:+.1f}/{sum(R)-h1:+.1f})"
    P = ['EURUSD', 'GBPUSD', 'XAUUSD', 'GER40']; DATA = {p: T.prep(p) for p in P}
    for mode in ['choch', 'choch_ob', 'bos', 'bos_ob']:
        for s in [5, 20]:
            for dirm in ['bias', 'trend', 'both']:
                for tp in [2.0, 3.0]:
                    cells = []; tot = []
                    for p in P:
                        if dirm == 'bias' and p == 'GER40': cells.append(f"{'n/a':>28}"); continue
                        o = run(p, DATA[p], s, mode, dirm, tp); tot += o; cells.append(f"{st(o):>28}")
                    tot.sort()
                    print(f"{mode:8} s{s:<2} {dirm:5} TP{tp:.0f} | " + " | ".join(cells) + f" || ALL {st(tot)}")
