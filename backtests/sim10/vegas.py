# EMA 144 / 169 tunnel (the user's MAs) on 1H / 4H: reaction statistics and entries × stops × exits.
import sys; sys.path.insert(0, '/home/claude/analyst/backtests/sim'); sys.path.insert(0, '/home/claude/analyst/backtests/sim10')
from multi import ema
def prep(b):
    C = [x['c'] for x in b]; a, c = ema(C, 144), ema(C, 169)
    for i, x in enumerate(b): x['t1'], x['t2'] = a[i], c[i]; x['tt'], x['tb'] = max(a[i], c[i]), min(a[i], c[i])
    return b
def signals(b, entry):
    out = []; far = {1: False, -1: False}; pierce = {1: None, -1: None}
    for i in range(200, len(b)):
        x = b[i]; A = x['atr']
        if not A: continue
        up = x['t1'] > x['t2'] and b[i-10]['t2'] < x['t2']; dn = x['t1'] < x['t2'] and b[i-10]['t2'] > x['t2']
        for d, ok in ((1, up), (-1, dn)):
            if not ok: far[d] = False; pierce[d] = None; continue
            edge = x['tt'] if d > 0 else x['tb']; inner = x['tb'] if d > 0 else x['tt']
            if (x['c'] - edge) * d > 2 * A: far[d] = True
            if entry == 'reject':
                touched = (x['l'] <= edge + 0.1 * A) if d > 0 else (x['h'] >= edge - 0.1 * A)
                if touched and (x['c'] - edge) * d > 0 and (x['c'] - x['o']) * d > 0 and (x['l'] - inner + A) * d > 0 if d > 0 else touched and (x['c'] - edge) * d > 0 and (x['c'] - x['o']) * d > 0:
                    out.append((i, d, 'mkt', x['c']))
            elif entry == 'limit':
                if far[d] and ((x['l'] <= edge) if d > 0 else (x['h'] >= edge)):
                    out.append((i, d, 'lim', edge)); far[d] = False
            elif entry == 'pierce':
                if (x['c'] - inner) * d < 0: pierce[d] = i
                elif pierce[d] is not None and i - pierce[d] <= 3 and (x['c'] - edge) * d > 0:
                    out.append((i, d, 'mkt', x['c'])); pierce[d] = None
            elif entry == 'fvg':   # an FVG (3-candle gap) in the trade direction whose zone touches the tunnel → limit at the gap's near edge
                if i >= 2:
                    g_lo, g_hi = (b[i-2]['h'], x['l']) if d > 0 else (x['h'], b[i-2]['l'])
                    if g_hi > g_lo and g_lo <= x['tt'] + 0.5 * A and g_hi >= x['tb'] - 0.5 * A:
                        out.append((i, d, 'limit_fvg', g_hi if d > 0 else g_lo))
    return out
def trades(b, entry, dirf, cost, sl='tunnel', ex='tp3', maxh=120, lim_bars=10):
    out = []; busy = -1
    for i, d, kind, px in signals(b, entry):
        if i <= busy: continue
        D_ = dirf(b[i])
        if D_ is None or d not in D_: continue
        x = b[i]; A = x['atr']; j0 = i + 1; e = px
        if kind in ('lim', 'limit_fvg'):
            if kind == 'lim': j0 = i; e = px            # touched on this bar: filled at the edge
            else:
                f = None
                for j in range(i + 1, min(len(b), i + 1 + lim_bars)):
                    if (b[j]['l'] <= px) if d > 0 else (b[j]['h'] >= px): f = j; break
                if f is None: continue
                j0 = f
        if kind != 'mkt' and sl == 'wick': continue       # no wick known at a limit fill (that would look into the fill bar)
        s = {'tunnel': (x['tb'] if d > 0 else x['tt']) - d * 0.5 * A, 'wick': (x['l'] if d > 0 else x['h']) - d * 0.3 * A, 'atr': e - d * 1.5 * A}[sl]
        r = abs(e - s)
        if r < 0.3 * A or r > 6 * A or (e - s) * d <= 0: continue
        tpR = {'tp2': 2, 'tp3': 3, 'tp5': 5}.get(ex); t = e + d * tpR * r if tpR else None; res = None; stop = s; best = e
        for j in range(j0, min(len(b), j0 + maxh)):
            y = b[j]
            if (y['l'] <= stop) if d > 0 else (y['h'] >= stop): res = d * (stop - e) / r; break
            if t and j > j0 - (0 if kind == 'mkt' else 0) and not (kind != 'mkt' and j == j0) and ((y['h'] >= t) if d > 0 else (y['l'] <= t)): res = tpR; break
            if ex == 'tunnel_trail' and (y['c'] - y['tb'] if d > 0 else y['tt'] - y['c']) < 0: res = d * (y['c'] - e) / r; break
            if ex == 'chand':
                best = max(best, y['h']) if d > 0 else min(best, y['l']); ns = best - d * 3 * y['atr']
                stop = max(stop, ns) if d > 0 else min(stop, ns)
        else:
            j = min(len(b) - 1, j0 + maxh - 1); res = d * (b[j]['c'] - e) / r
        out.append((x['t'], res - cost / r)); busy = j
    return out
