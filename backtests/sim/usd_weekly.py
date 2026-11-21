# R per week for the BE Swing default on the USD pairs: bias weeks, and the trend version over 3 years; risk scaled by |gap|.
import sys, os, datetime as D, collections, statistics as S
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'usd_ideas.py')).read().split('IDEAS = [')[0])
BASE = dict(dirm='both', partial=True, tp=3, hold='fri')
def weekly(tr, w=lambda x: 1.0):
    by = collections.OrderedDict()
    for x in sorted(tr, key=lambda x: x['tx']): k = x['tx'].astimezone(NY).isocalendar()[:2]; by[k] = by.get(k, 0) + x['R'] * w(x)
    return by
def dd(tr, w=lambda x: 1.0):
    eq = pk = m = 0
    for x in sorted(tr, key=lambda x: x['tx']): eq += x['R'] * w(x); pk = max(pk, eq); m = min(m, eq - pk)
    return m
bt = sum([run(p, data[p], B, BASE, H1[0], H2[1], usd) for p in USD], [])
wk = weekly(bt); print('Bias weeks, R per week:', {f'W{k[1]}': round(v, 1) for k, v in wk.items()}, 'mean', round(S.mean(wk.values()), 2))
sz = lambda x: 1.5 if x['gap'] is not None and abs(x['gap']) >= 8 else 1.0 if x['gap'] is not None and abs(x['gap']) >= 5 else 0.5
wk2 = weekly(bt, sz); print('Risk by |gap| (0.5/1/1.5%):', {f'W{k[1]}': round(v, 1) for k, v in wk2.items()}, 'mean', round(S.mean(wk2.values()), 2), 'maxDD', round(dd(bt, sz), 1), 'vs', round(dd(bt), 1))
for pairs, lab in [(LONG, '6 USD pairs')]:
    tt = sum([run(p, data[p], B, {**BASE, 'dirm': 'trend'}, D.datetime(2024, 3, 1, tzinfo=D.timezone.utc), H2[1], usd) for p in pairs], [])
    w = list(weekly(tt).values()); w2 = [sum(w[i:i + 2]) for i in range(0, len(w) - 1, 2)]
    print(f'Trend version {lab} 2024-03..2026-11: {len(tt)} trades, {len(w)} weeks, mean {S.mean(w):+.2f}R/week, 2-week mean {S.mean(w2):+.2f}R, 2-week blocks >= +4R: {sum(x >= 4 for x in w2)}/{len(w2)}, negative: {sum(x < 0 for x in w2)}/{len(w2)}, worst week {min(w):+.1f}R, maxDD {dd(tt):+.1f}R')
