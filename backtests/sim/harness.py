# Shared test harness: 1H W40-47 (engine bias), pre-W40 1H (no bias), 4H W40-47 (engine bias), 4H 3y (6 pairs, trend direction).
# run(p, bars, P, start, end) must return trades with R, tx; it reads direction from smc.B[(pair, week)].
import sys, os, io, contextlib, datetime as D
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smc
from smc import prep, B, H, PRE, USDP, EURP
ALL = USDP + EURP
D1 = {p: prep(p) for p in ALL}          # 1H (must be loaded before smc_3y patches smc.load1h to 4H)
with contextlib.redirect_stdout(io.StringIO()):
    import smc_3y
D4 = {p: smc_3y.load4(p) for p in ALL}
for p in ALL:
    A = None
    for i, x in enumerate(D4[p]):
        tr_ = x['h'] - x['l'] if i == 0 else max(x['h'] - x['l'], abs(x['h'] - D4[p][i - 1]['c']), abs(x['l'] - D4[p][i - 1]['c']))
        A = tr_ if A is None else (A * 13 + tr_) / 14; x['atr'] = A if i >= 13 else None
        x['hr'] = x['t'].astimezone(D.timezone(D.timedelta(hours=2))).hour
B1 = dict(B)
def _wkdir(b):
    closes = {}; [closes.__setitem__(x['day'], x['c']) for x in b]; days = sorted(closes); wl = {}; out = {}
    for i, d in enumerate(days):
        if i >= 19: wl[d.isocalendar()[:2]] = closes[d] - sum(closes[q] for q in days[i - 19:i + 1]) / 20
    ws = sorted(wl)
    for a, nx in zip(ws, ws[1:]): out[nx] = 'U' if wl[a] > 0 else 'D'
    return out
BT = {}
for p in smc_3y.LONG:
    for wk, v in _wkdir(D4[p]).items(): BT[(p, wk)] = (v,)
def stats(t):
    t = sorted(t, key=lambda x: x['tx']); eq = pk = dd = 0
    for x in t: eq += x['R']; pk = max(pk, eq); dd = min(dd, eq - pk)
    return len(t), eq, dd, sum(x['R'] > 0 for x in t) / max(1, len(t))
def go(run, P, hours=(6, 22)):
    B.clear(); B.update(B1)
    a = stats(sum([run(p, D1[p], {**P, 'bias': True, 'hours': hours}, s, e) for p in ALL for s, e in H], []))
    pre = stats(sum([run(p, D1[p], {**P, 'bias': False, 'hours': hours}, *PRE) for p in ALL], []))
    b = stats(sum([run(p, D4[p], {**P, 'bias': True, 'hours': hours}, s, e) for p in ALL for s, e in H], []))
    B.clear(); B.update(BT)
    ys = [sum([run(p, D4[p], {**P, 'bias': True}, s, e) for p in smc_3y.LONG], []) for s, e in smc_3y.YRS]
    c = stats(sum(ys, [])); B.clear(); B.update(B1)
    yr = ','.join('%+.0f' % sum(x['R'] for x in y) for y in ys)
    return (f"1H {a[0]:3}tr {a[1]:+6.1f}R dd{a[2]:+5.1f} | pre {pre[0]:3}tr {pre[1]:+6.1f}R | 4H {b[0]:3}tr {b[1]:+5.1f}R | "
            f"3y {c[0]:3}tr {c[1]:+6.1f}R {c[1] / max(1, c[0]):+.2f}/tr dd{c[2]:+5.1f} [{yr}]")
