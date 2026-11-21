# The user's settings on the EUR crosses (4H candles; worst-case same-bar fills), W40-W47, plus variants.
import sys, os, datetime as D, statistics as St, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from swing2 import *
U = lambda *a: D.datetime(*a, tzinfo=D.timezone.utc)
H = [(U(2026, 9, 27, 21), U(2026, 10, 25, 21)), (U(2026, 10, 25, 21), U(2026, 11, 22))]
EUR = ['EURGBP', 'EURJPY', 'EURCHF', 'EURAUD', 'EURNZD', 'EURCAD']
B = bias_table(); data = {}
for p in EUR:
    bars = load(p); a = None; pc = None
    for i, b in enumerate(bars):
        tr = b['h'] - b['l'] if pc is None else max(b['h'], pc) - min(b['l'], pc)
        a = tr if a is None else (a * 13 + tr) / 14 if i >= 14 else (a * i + tr) / (i + 1)
        b['atr4'] = a if i >= 13 else None; pc = b['c']
        if b['atr4'] is None: b['atr'] = None
    data[p] = bars
BASE = dict(dirm='both', tsrc='sma20', cf='none', entry='C', k=1.0, atrsrc='4h', partial=False, tp=4, trailm='close', trailk=0.75, trailk2=0.5, trailat=2, trailfrom=-99, maxdow=2, cool=24, fillchk=True)
def ev(P, pairs=EUR, show=False):
    Q = {**BASE, **P}; hs = [[], []]
    for p in pairs:
        for k, (a, c) in enumerate(H): hs[k] += run(p, data[p], B, Q, a, c)
    t = sorted(hs[0] + hs[1], key=lambda x: x['tx']); eq = pk = dd = 0; wk = collections.defaultdict(float)
    for x in t: eq += x['R']; pk = max(pk, eq); dd = min(dd, eq - pk); wk[x['wk'][1]] += x['R']
    w = [wk.get(q, 0) for q in range(40, 48)]
    return t, sum(x['R'] for x in hs[0]), sum(x['R'] for x in hs[1]), dd, [w[i] + w[i + 1] for i in range(0, 8, 2)]
def line(n, r):
    t, a, b, dd, b2 = r; win = sum(x['R'] > 0 for x in t) / max(1, len(t))
    print(f"{n:<46} {len(t):3}tr win {win:.0%} {a:+5.1f}/{b:+5.1f} = {a + b:+5.1f}R dd {dd:+.1f} 2wk[{', '.join(f'{v:+.1f}' for v in b2)}]")
print('bias W40-47:')
for p in EUR: print('  ', p, ''.join(B.get((p, (2026, w)), ('?',))[0] for w in range(40, 48)), [B.get((p, (2026, w)), ('?', '?', None))[2] for w in range(40, 48)])
r = ev({}); line('ALL EUR crosses, your settings', r)
for p in EUR: line('  ' + p, ev({}, [p]))
print('--- variants (all 6)')
for n, P in [('bias only (no SMA20)', dict(dirm='bias')), ('|gap| >= 5', dict(mingap=5)), ('|gap| >= 7', dict(mingap=7)),
             ('conviction medium/high', dict(conv='mh')), ('TP 2R', dict(tp=2)), ('TP 3R, no tighten', dict(tp=3, trailk2=None, trailat=99)),
             ('trail 1.0 / 0.5 after 2R', dict(trailk=1.0)), ('SL 1.5 ATR', dict(k=1.5)), ('cooldown 48h', dict(cool=48)), ('trend only (no bias)', dict(dirm='trend'))]:
    line('  ' + n, ev(P))
t = r[0]
print('by direction:', {k: round(sum(x['R'] for x in t if (x['d'] > 0) == (k == 'EUR long')), 1) for k in ('EUR long', 'EUR short')},
      {k: sum(1 for x in t if (x['d'] > 0) == (k == 'EUR long')) for k in ('EUR long', 'EUR short')})
