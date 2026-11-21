# The user's TradingView settings (screenshot 21 Nov): Both must agree (bias + SMA20), week-to-date confirmation, entry C
# (break of the confirming candle), SL 1x 4H ATR, Fixed exit, no TP, trailing from the close 0.75x 4H ATR, no Thu/Fri entries.
exec(open('usd_sweep_research.py').read().split('b0 = evalP')[0])
for p, bars in data.items():
    a = None; pc = None
    for i, b in enumerate(bars):
        tr = b['h'] - b['l'] if pc is None else max(b['h'], pc) - min(b['l'], pc)
        a = tr if a is None else (a * 13 + tr) / 14 if i >= 14 else (a * i + tr) / (i + 1)
        b['atr4'] = a if i >= 13 else None; pc = b['c']
    for b in bars:
        if b['atr4'] is None: b['atr'] = None
b0 = evalP({}, trend=False)
SHOT = dict(dirm='both', tsrc='sma20', cf='wtd', entry='C', k=1.0, atrsrc='4h', partial=False, tp=0, trailm='close', trailk=0.75, trailfrom=-99, maxdow=2, cool=24)
CH = dict(partial=False, maxdow=2, tp=0, trailm='chand', trailk=0.75, trailfrom=1)
for n, P in [('sweep, ½ at 1R, TP3 (old default)', {}), ('sweep, Fixed + chandelier 0.75 daily ATR (your CSV)', CH),
             ('YOUR SCREENSHOT: both+WTD, entry C, 4H ATR, trail close 0.75', SHOT),
             ('  same but bias only (no SMA agreement)', {**SHOT, 'dirm': 'bias'}),
             ('  same but daily ATR', {**SHOT, 'atrsrc': 'd'}),
             ('  same but chandelier after +1R (4H ATR)', {**SHOT, 'trailm': 'chand', 'trailfrom': 1}),
             ('  same with sweep entry', {**SHOT, 'entry': 'SWP', 'cf': 'none'})]:
    line(n, evalP(P), b0)
print('--- worst case: SL counted if touched on the entry candle')
for n, P in [('YOUR SCREENSHOT, worst-case fills', {**SHOT, 'fillchk': True}), ('  bias only, worst-case', {**SHOT, 'dirm': 'bias', 'fillchk': True}),
             ('  chandelier after +1R, worst-case', {**SHOT, 'trailm': 'chand', 'trailfrom': 1, 'fillchk': True})]:
    line(n, evalP(P), b0)
tr = sum([run(p, data[p], B, {**SHOT, 'fillchk': True}, a, c, usd) for p in USD for a, c in H], [])
import collections, statistics as St
print('exits', collections.Counter(x['why'] for x in tr), 'avg hold h', round(St.mean((x['tx'] - x['t']).total_seconds() / 3600 for x in tr), 1),
      'win', f"{sum(x['R'] > 0 for x in tr) / len(tr):.0%}", 'avg R', round(St.mean(x['R'] for x in tr), 2))
for p in USD: print('  ', p, round(sum(x['R'] for x in tr if x['pair'] == p), 1), sum(1 for x in tr if x['pair'] == p))
import swing2
_c = swing2.cost_of
for m in (2, 3):
    swing2.cost_of = lambda p, m=m: _c(p) * m
    globals()['cost_of'] = swing2.cost_of
    line(f'YOUR SCREENSHOT, worst-case, cost x{m}', evalP({**SHOT, 'fillchk': True}, trend=False), b0)
swing2.cost_of = _c
risk = [x for x in tr]
