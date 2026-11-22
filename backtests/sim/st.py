# Supertrend (ATR 10, x3, hl2, RMA ATR) as a strategy. Entry at the close of the flip bar in the allowed direction.
# Risk unit R = distance from entry to the Supertrend line at entry (where the stop would sit).
# exit 'close'  : exit at the close of the opposite flip (can lose more than 1R)
# exit 'line'   : stop = Supertrend line of the previous bar, hit intrabar (gap -> open)
# tpR > 0       : add a fixed take-profit at tpR x R
# pull=True     : instead of entering at the flip, wait for a pullback: limit at the line + k ATR while the trend holds
import sys, os, io, contextlib, collections, datetime as D
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smc
from smc import prep, B, H, PRE, USDP, EURP, cost_of, pip_of

def supertrend(b, per=10, mult=3.0):
    n = len(b); tr = [0.0] * n; atr = [None] * n
    for i, x in enumerate(b):
        tr[i] = x['h'] - x['l'] if i == 0 else max(x['h'] - x['l'], abs(x['h'] - b[i - 1]['c']), abs(x['l'] - b[i - 1]['c']))
        if i == per - 1: atr[i] = sum(tr[:per]) / per
        elif i >= per: atr[i] = (atr[i - 1] * (per - 1) + tr[i]) / per
    up = [None] * n; dn = [None] * n; tr_ = [1] * n
    for i, x in enumerate(b):
        if atr[i] is None: continue
        src = (x['h'] + x['l']) / 2; u = src - mult * atr[i]; d = src + mult * atr[i]
        u1 = up[i - 1] if up[i - 1] is not None else u; d1 = dn[i - 1] if dn[i - 1] is not None else d
        up[i] = max(u, u1) if b[i - 1]['c'] > u1 else u
        dn[i] = min(d, d1) if b[i - 1]['c'] < d1 else d
        t = tr_[i - 1]
        tr_[i] = 1 if t == -1 and x['c'] > d1 else -1 if t == 1 and x['c'] < u1 else t
    return up, dn, tr_, atr

DEF = dict(per=10, mult=3.0, exit='line', tpR=0, bias=True, hours=None, minR=0.3, maxR=4, reenter=False)
def run(p, b, P, start, end):
    P = {**DEF, **P}; up, dn, tr, atr = supertrend(b, P['per'], P['mult']); cost = cost_of(p) * pip_of(p)
    res = []; pos = None
    for i in range(1, len(b)):
        x = b[i]
        if pos:
            d = pos['d']; line = up[i - 1] if d > 0 else dn[i - 1]
            px = None
            if P['exit'] == 'line':
                if (d > 0 and x['l'] <= line) or (d < 0 and x['h'] >= line):
                    px = min(x['o'], line) if d > 0 else max(x['o'], line); why = 'line'
            if px is None and pos['tp'] is not None and ((d > 0 and x['h'] >= pos['tp']) or (d < 0 and x['l'] <= pos['tp'])):
                px = max(x['o'], pos['tp']) if d > 0 else min(x['o'], pos['tp']); why = 'TP'
            if px is None and tr[i] != d: px = x['c']; why = 'flip'
            if px is not None:
                res.append(dict(p=p, d=d, t=pos['t'], tx=x['tc'], wk=pos['wk'], R=d * (px - pos['e']) / pos['r'] - cost / pos['r'], why=why)); pos = None
        if atr[i] is None or pos or not (start <= x['t'] < end): continue
        flip = tr[i] != tr[i - 1]
        d = tr[i]
        if not (flip or (P['reenter'] and pos is None and i > 1 and res and res[-1]['why'] == 'TP' and res[-1]['d'] == d)): continue
        bi_ = B.get((p, x['wk']), ('-',))[0]; bd = 1 if bi_ == 'U' else -1 if bi_ == 'D' else 0
        if P['bias'] and bd != d: continue
        if P['hours'] and not (P['hours'][0] <= x['hr'] < P['hours'][1]): continue
        line = up[i] if d > 0 else dn[i]; r = abs(x['c'] - line)
        if not (P['minR'] * atr[i] <= r <= P['maxR'] * atr[i]): continue
        pos = dict(d=d, e=x['c'], r=r, t=x['t'], wk=x['wk'], tp=x['c'] + d * P['tpR'] * r if P['tpR'] else None)
    return res

def stats(t):
    t = sorted(t, key=lambda x: x['tx']); eq = pk = dd = 0
    for x in t: eq += x['R']; pk = max(pk, eq); dd = min(dd, eq - pk)
    return len(t), eq, dd, sum(x['R'] > 0 for x in t) / max(1, len(t))

if __name__ == '__main__':
    ALL = USDP + EURP
    D1 = {p: prep(p) for p in ALL}
    with contextlib.redirect_stdout(io.StringIO()):
        import smc_3y
    D4 = {p: smc_3y.load4(p) for p in ALL}
    for p in ALL:
        A = None
        for i, x in enumerate(D4[p]):
            tr_ = x['h'] - x['l'] if i == 0 else max(x['h'] - x['l'], abs(x['h'] - D4[p][i - 1]['c']), abs(x['l'] - D4[p][i - 1]['c']))
            A = tr_ if A is None else (A * 13 + tr_) / 14; x['atr'] = A; x['hr'] = x['t'].astimezone(D.timezone(D.timedelta(hours=2))).hour
    B1 = dict(B)
    def wkdir(b):
        closes = {}; [closes.__setitem__(x['day'], x['c']) for x in b]; days = sorted(closes); wl = {}; out = {}
        for i, d in enumerate(days):
            if i >= 19: wl[d.isocalendar()[:2]] = closes[d] - sum(closes[q] for q in days[i - 19:i + 1]) / 20
        ws = sorted(wl)
        for a, nx in zip(ws, ws[1:]): out[nx] = 'U' if wl[a] > 0 else 'D'
        return out
    BT = {}
    for p in smc_3y.LONG:
        for wk, v in wkdir(D4[p]).items(): BT[(p, wk)] = (v,)
    def go(P):
        B.clear(); B.update(B1)
        a = stats(sum([run(p, D1[p], P, s, e) for p in ALL for s, e in H], []))
        b = stats(sum([run(p, D4[p], P, s, e) for p in ALL for s, e in H], []))
        B.clear(); B.update(BT)
        ys = [sum([run(p, D4[p], P, s, e) for p in smc_3y.LONG], []) for s, e in smc_3y.YRS]
        c = stats(sum(ys, []))
        yr = ','.join('%+.0f' % sum(x['R'] for x in y) for y in ys)
        return (f"1H W40-47 {a[0]:3}tr {a[1]:+6.1f}R dd{a[2]:+5.1f} | 4H W40-47 {b[0]:3}tr {b[1]:+6.1f}R dd{b[2]:+5.1f} | "
                f"4H 3y trend {c[0]:3}tr {c[1]:+6.1f}R {c[1] / max(1, c[0]):+.2f}/tr dd{c[2]:+5.1f} win {c[3]:.0%} [{yr}]")
    V = [('10/3, no direction filter, line stop', dict(bias=False)),
         ('10/3, bias, exit on flip close', dict(exit='close')),
         ('10/3, bias, line stop (trailing)', {}),
         ('10/3, bias, line stop + TP 2R', dict(tpR=2)),
         ('10/3, bias, line stop + TP 3R', dict(tpR=3)),
         ('10/3, bias, line stop + TP 4R', dict(tpR=4)),
         ('10/3, bias, line + TP 3R, re-enter', dict(tpR=3, reenter=True)),
         ('10/2, bias, line stop', dict(mult=2.0)),
         ('10/2, bias, line + TP 3R', dict(mult=2.0, tpR=3)),
         ('14/4, bias, line stop', dict(per=14, mult=4.0)),
         ('14/4, bias, line + TP 3R', dict(per=14, mult=4.0, tpR=3)),
         ('10/3, bias, line stop, 06-22', dict(hours=(6, 22))),
         ('10/3, bias, line + TP 3R, 06-22', dict(tpR=3, hours=(6, 22)))]
    for n, P in V: print(f"{n:<38} {go(P)}")
