# Correction 21 Nov: price confirmation = Close vs 20-day SMA. With "Both must agree" on a 20-day SMA trend this is the same
# condition as the trend, so it adds nothing: cf = none.
exec(open('usd_screenshot.py').read().split('b0 = evalP({}, trend=False)')[0])
b0 = evalP({}, trend=False)
SHOT = dict(dirm='both', tsrc='sma20', cf='none', entry='C', k=1.0, atrsrc='4h', partial=False, tp=0, trailm='close', trailk=0.75, trailfrom=-99, maxdow=2, cool=24, fillchk=True)
for n, P in [('YOUR SETTINGS (both, close vs SMA20, C, 4H ATR, trail close 0.75)', SHOT), ('  bias only', {**SHOT, 'dirm': 'bias'}),
             ('  with week-to-date instead', {**SHOT, 'cf': 'wtd'}), ('  trailing 0.5', {**SHOT, 'trailk': 0.5}), ('  trailing 1.0', {**SHOT, 'trailk': 1.0}),
             ('  SL 1.5 x 4H ATR', {**SHOT, 'k': 1.5}), ('  Thursday entries allowed', {**SHOT, 'maxdow': 3})]:
    line(n, evalP(P), b0)
import collections, statistics as St, swing2
tr = sum([run(p, data[p], B, SHOT, a, c, usd) for p in USD for a, c in H], [])
print('avg hold h', round(St.mean((x['tx'] - x['t']).total_seconds() / 3600 for x in tr), 1), 'win', f"{sum(x['R'] > 0 for x in tr) / len(tr):.0%}", 'avg R', round(St.mean(x['R'] for x in tr), 2), 'USD-long share', f"{sum((x['d'] > 0) == x['pair'].startswith('USD') for x in tr) / len(tr):.0%}")
_c = swing2.cost_of; swing2.cost_of = lambda p: _c(p) * 3
line('YOUR SETTINGS, cost x3', evalP(SHOT, trend=False), b0)
