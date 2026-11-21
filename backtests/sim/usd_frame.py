# Best technical frameworks from usd_research.py, with portfolio rules, on 3 years (trend) and on the bias weeks (bias + trend agree).
import sys, os, datetime as D, collections, statistics as S
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from swing2 import *
U = lambda *a: D.datetime(*a, tzinfo=D.timezone.utc)
data = {p: load(p) for p in USD}; usd = usd_strength(data); B = bias_table()
LONG = ['GBPUSD', 'AUDUSD', 'USDJPY', 'USDCHF', 'USDCAD', 'XAUUSD']
def stats(t):
    t = sorted(t, key=lambda x: x['tx']); eq = pk = m = 0; wk = collections.OrderedDict()
    for x in t:
        eq += x['R']; pk = max(pk, eq); m = min(m, eq - pk); k = x['tx'].astimezone(NY).isocalendar()[:2]; wk[k] = wk.get(k, 0) + x['R']
    w = list(wk.values()); b2 = [sum(w[i:i + 2]) for i in range(0, len(w) - 1, 2)]
    return f"{len(t):4}tr {sum(x['R'] for x in t):+6.1f}R  {sum(x['R'] for x in t)/max(len(t),1):+.2f}/tr  maxDD {m:+5.1f}R  2wk>=4R {sum(x>=4 for x in b2)}/{len(b2)}  2wk<0 {sum(x<0 for x in b2)}/{len(b2)}"
EX = dict(partial=True, tp=3, hold='fri')
F = [('Current default (SMA20, entry A)', dict(tsrc='sma20', entry='A')),
     ('SMA20 + break of yesterday', dict(tsrc='sma20', entry='D')),
     ('SMA50 + break of yesterday', dict(tsrc='sma50', entry='D'))]
for name, P in F:
    Q = {**EX, **P}
    t3 = sum([run(p, data[p], B, {**Q, 'dirm': 'trend'}, U(2024, 3, 1), U(2026, 11, 22), usd) for p in LONG], [])
    tb = sum([run(p, data[p], B, {**Q, 'dirm': 'both'}, U(2026, 9, 27, 21), U(2026, 11, 22), usd) for p in USD], [])
    tbo = sum([run(p, data[p], B, {**Q, 'dirm': 'bias'}, U(2026, 9, 27, 21), U(2026, 11, 22), usd) for p in USD], [])
    print(f"\n{name}")
    print('  3y trend        ', stats(t3))
    for lab, port in [('cap 2', dict(cap=2)), ('cap 3', dict(cap=3)), ('week stop -2R', dict(wkstop=2)), ('cap 3 + week stop', dict(cap=3, wkstop=2))]:
        print(f'  3y {lab:<14}', stats(portfolio(t3, **port)))
    print('  bias weeks both ', stats(tb))
    print('  bias weeks bias ', stats(tbo))
