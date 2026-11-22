# Swing v2 idea: reaction at the user's moving averages (EMA50, SMMA50, SMMA100 from his "US30 Strategy" script) on 1H / 4H.
# Signal: trend stack (EMA50 > SMMA50 > SMMA100 for longs, mirror for shorts), the candle's wick reaches the MA (or the MA zone)
# and it closes back on the trend side as a rejection candle. Entry at the close; SL beyond the wick (or beyond SMMA100); TP in R.
import sys; sys.path.insert(0, '/home/claude/analyst/backtests/sim'); sys.path.insert(0, '/home/claude/analyst/backtests/sim10')
from multi import ema, rma
def ma_signals(b, touch='ema50', stack=True):
    C = [x['c'] for x in b]; e50 = ema(C, 50); s50 = rma(C, 50); s100 = rma(C, 100); out = []
    for i in range(110, len(b)):
        x = b[i]; a, m1, m2 = e50[i], s50[i], s100[i]
        if m2 is None: continue
        up = a > m1 > m2 if stack else x['c'] > m2; dn = a < m1 < m2 if stack else x['c'] < m2
        lvl_u = {'ema50': a, 'smma50': m1, 'smma100': m2, 'zone': max(a, m1)}[touch]
        if up:
            lo_ok = x['l'] <= lvl_u and (touch != 'zone' or x['l'] >= m2 - 0.25 * x['atr'])
            if lo_ok and x['c'] > lvl_u and x['c'] > x['o']: out.append((i, 1, m2))
        if dn:
            lvl_d = {'ema50': a, 'smma50': m1, 'smma100': m2, 'zone': min(a, m1)}[touch]
            hi_ok = x['h'] >= lvl_d and (touch != 'zone' or x['h'] <= m2 + 0.25 * x['atr'])
            if hi_ok and x['c'] < lvl_d and x['c'] < x['o']: out.append((i, -1, m2))
    return out
def trades(b, sigs, dirf, cost, sl='wick', tp=3.0, maxh=60):
    out = []; busy = -1
    for i, d, m2 in sigs:
        if i <= busy or not b[i].get('atr'): continue
        D_ = dirf(b[i])
        if D_ is None or d not in D_: continue
        x = b[i]; e = x['c']
        s = (x['l'] - 0.2 * x['atr']) if d > 0 else (x['h'] + 0.2 * x['atr'])
        if sl == 'smma100': s = m2 - d * 0.2 * x['atr']
        if sl == 'atr': s = e - d * 1.5 * x['atr']
        r = abs(e - s)
        if r < 0.3 * x['atr'] or r > 5 * x['atr'] or (e - s) * d <= 0: continue
        t = e + d * tp * r; res = None
        for j in range(i + 1, min(len(b), i + 1 + maxh)):
            y = b[j]
            if (y['l'] <= s) if d > 0 else (y['h'] >= s): res = -1; break
            if (y['h'] >= t) if d > 0 else (y['l'] <= t): res = tp; break
        else: j = min(len(b) - 1, i + maxh); res = d * (b[j]['c'] - e) / r
        out.append((x['t'], res - cost / r)); busy = j
    return out
