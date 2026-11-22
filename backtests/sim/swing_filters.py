# BE Swing (4H entry C on the 1H path, bias + SMA20, Mon-Wed, 06-22, TP4, trailing 0.75 -> 0.5 after 2R):
# extra filters from outside the current rule set, one at a time, then the best pairs of them. Bias weeks W40-W47, 8 pairs.
import sys, os, collections, itertools, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mtf_c import *
PAIRS = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'USDCAD', 'AUDUSD', 'NZDUSD', 'XAUUSD']
B = bias_table(); D4 = {p: prep4(p) for p in PAIRS}; D1 = {p: load1h(p) for p in PAIRS}
BASE = dict(hours=(6, 22))

# daily series per pair (from the 4H bars): open, close, RSI14; known before each day
DAY = {}
for p, b4 in D4.items():
    d = collections.OrderedDict()
    for x in b4:
        r = d.setdefault(x['day'], dict(o=x['o'], h=x['h'], l=x['l'], c=x['c']))
        r['h'] = max(r['h'], x['h']); r['l'] = min(r['l'], x['l']); r['c'] = x['c']
    ks = list(d); g = l = None; prev = {}
    for k_, k in enumerate(ks):
        if k_ >= 1:
            pk = ks[k_ - 1]; ch = d[pk]['c'] - (d[ks[k_ - 2]]['c'] if k_ >= 2 else d[pk]['o'])
            up, dn = max(ch, 0), max(-ch, 0)
            g = up if g is None else (g * 13 + up) / 14; l = dn if l is None else (l * 13 + dn) / 14
            prev[k] = dict(o=d[pk]['o'], c=d[pk]['c'], rsi=100 - 100 / (1 + g / l) if l else 100)
    DAY[p] = prev
# running day range up to each 4H bar
for p, b4 in D4.items():
    hi = lo = None; day = None
    for x in b4:
        if x['day'] != day: day = x['day']; hi, lo = x['h'], x['l']
        else: hi, lo = max(hi, x['h']), min(lo, x['l'])
        x['dhi'], x['dlo'] = hi, lo
# USD basket: sign-adjusted (USD up = +) return over the last K 4H bars, other fiat USD pairs
IDX = {p: {x['tc']: k for k, x in enumerate(D4[p])} for p in PAIRS}
def usd_move(p0, tc, K):
    v = []
    for p in PAIRS:
        if p in (p0, 'XAUUSD'): continue
        k = IDX[p].get(tc)
        if k is None or k < K: continue
        b = D4[p]; s = 1 if p.startswith('USD') else -1
        v.append(s * (b[k]['c'] / b[k - K]['c'] - 1) / (b[k]['atr4'] / b[k]['c']))
    return sum(v) / len(v) if len(v) >= 3 else None
def usd_dir(p, dr): return dr if p.startswith('USD') else -dr

F = {
 'no Monday': lambda p, i, s, dr, bi: s['dow'] != 0,
 'Tue-Wed only': lambda p, i, s, dr, bi: s['dow'] in (1, 2),
 'week-to-date against (pullback)': lambda p, i, s, dr, bi: (s['c'] - s['wko']) * dr < 0,
 'week-to-date with': lambda p, i, s, dr, bi: (s['c'] - s['wko']) * dr > 0,
 'price vs day open: against': lambda p, i, s, dr, bi: (s['c'] - s['dop']) * dr < 0,
 'price vs day open: with': lambda p, i, s, dr, bi: (s['c'] - s['dop']) * dr > 0,
 'USD basket agrees (1 day)': lambda p, i, s, dr, bi: (lambda m: m is not None and m * usd_dir(p, dr) > 0)(usd_move(p, s['tc'], 6)),
 'USD basket agrees (2 days)': lambda p, i, s, dr, bi: (lambda m: m is not None and m * usd_dir(p, dr) > 0)(usd_move(p, s['tc'], 12)),
 'USD basket not against (1 day)': lambda p, i, s, dr, bi: (lambda m: m is None or m * usd_dir(p, dr) > -0.5)(usd_move(p, s['tc'], 6)),
 'day range used < 70% of ATR': lambda p, i, s, dr, bi: (s['dhi'] - s['dlo']) < 0.7 * s['atr'],
 'day range used < 50% of ATR': lambda p, i, s, dr, bi: (s['dhi'] - s['dlo']) < 0.5 * s['atr'],
 'not stretched: |close-SMA20| < 1.5 ATR': lambda p, i, s, dr, bi: abs(s['c'] - s['sma20']) < 1.5 * s['atr'],
 'stretched: |close-SMA20| > 1 ATR': lambda p, i, s, dr, bi: abs(s['c'] - s['sma20']) > 1.0 * s['atr'],
 'daily RSI not extreme (<70 long / >30 short)': lambda p, i, s, dr, bi: (lambda r: r is None or (r['rsi'] < 70 if dr > 0 else r['rsi'] > 30))(DAY[p].get(s['day'])),
 'daily RSI in the trend half (>50 long)': lambda p, i, s, dr, bi: (lambda r: r is not None and (r['rsi'] - 50) * dr > 0)(DAY[p].get(s['day'])),
 'daily RSI pullback (40-60)': lambda p, i, s, dr, bi: (lambda r: r is not None and 40 <= r['rsi'] <= 60)(DAY[p].get(s['day'])),
 'yesterday closed in direction': lambda p, i, s, dr, bi: (lambda r: r is not None and (r['c'] - r['o']) * dr > 0)(DAY[p].get(s['day'])),
 'yesterday closed against (pullback day)': lambda p, i, s, dr, bi: (lambda r: r is not None and (r['c'] - r['o']) * dr < 0)(DAY[p].get(s['day'])),
 'signal candle strong body (>=50% range, in dir)': lambda p, i, s, dr, bi: (s['c'] - s['o']) * dr > 0 and abs(s['c'] - s['o']) >= 0.5 * (s['h'] - s['l']),
 'signal candle small (< 1.2 x 4H ATR)': lambda p, i, s, dr, bi: (s['h'] - s['l']) < 1.2 * s['atr4'],
 'signal candle big (> 0.8 x 4H ATR)': lambda p, i, s, dr, bi: (s['h'] - s['l']) > 0.8 * s['atr4'],
 '4H EMA20 sloping with': lambda p, i, s, dr, bi: s['ema'] is not None and s['ema_prev'] is not None and (s['ema'] - s['ema_prev']) * dr > 0,
 'daily ADX > 20': lambda p, i, s, dr, bi: s['f']['adx'] is not None and s['f']['adx'] > 20,
 'daily ADX > 25': lambda p, i, s, dr, bi: s['f']['adx'] is not None and s['f']['adx'] > 25,
 'daily ATR in top half of 100 days': lambda p, i, s, dr, bi: s['f']['atrp'] is not None and s['f']['atrp'] > 0.5,
 'daily ATR in bottom half': lambda p, i, s, dr, bi: s['f']['atrp'] is not None and s['f']['atrp'] <= 0.5,
 'efficiency ratio > 0.3 (clean trend)': lambda p, i, s, dr, bi: s['f']['er'] is not None and s['f']['er'] > 0.3,
 'beyond last week high/low': lambda p, i, s, dr, bi: (s['c'] - (s['pwh'] if dr > 0 else s['pwl'])) * dr > 0,
 'inside last week range': lambda p, i, s, dr, bi: s['pwl'] <= s['c'] <= s['pwh'],
 'SMA20 above SMA50 (longs) / below (shorts)': lambda p, i, s, dr, bi: s['sma50'] is not None and (s['sma20'] - s['sma50']) * dr > 0,
 '20-day return with the trade': lambda p, i, s, dr, bi: s['f']['ret20'] is not None and s['f']['ret20'] * dr > 0,
 'conviction gap >= 6': lambda p, i, s, dr, bi: bi[2] is not None and abs(bi[2]) >= 6,
 'conviction gap <= 9': lambda p, i, s, dr, bi: bi[2] is not None and abs(bi[2]) <= 9,
}
EXTRA = {'max 1 loss per pair per week': dict(maxloss=1), 'max 2 trades per pair per week': dict(maxwk=2), 'entries from 08:00': dict(hours=(8, 22)),
         'entries 08-20': dict(hours=(8, 20)), 'signal candle closed in direction': dict(sc='dir'), 'close beyond 4H EMA20': dict(sc='ema'),
         'trail 1.0 -> 0.5': dict(trk=1.0)}

def ev(P):
    hs = [sum([run_c(p, D4[p], D1[p], B, {**BASE, **P}, a, c) for p in PAIRS], []) for a, c in H]
    t = sorted(hs[0] + hs[1], key=lambda x: x['tx']); eq = pk = dd = 0; pp = collections.defaultdict(float)
    for x in t: eq += x['R']; pk = max(pk, eq); dd = min(dd, eq - pk); pp[x['pair']] += x['R']
    return dict(n=len(t), h1=sum(x['R'] for x in hs[0]), h2=sum(x['R'] for x in hs[1]), dd=dd, win=sum(x['R'] > 0 for x in t), neg=sum(v < 0 for v in pp.values()), pp=pp)
def line(n, r, base=None):
    t = r['h1'] + r['h2']; mark = ''
    if base: mark = '  ✓✓' if r['h1'] > base['h1'] and r['h2'] > base['h2'] else ''
    return f"{n:<48} {r['n']:3}tr w{r['win']/max(1,r['n']):.0%} {t/max(1,r['n']):+.2f}R/tr {r['h1']:+5.1f}/{r['h2']:+5.1f} = {t:+5.1f}R dd {r['dd']:+5.1f} pairs<0 {r['neg']}{mark}"
if __name__ == '__main__':
    base = ev({}); print(line('BASE (your settings)', base))
    out = []
    for n, f in F.items(): r = ev(dict(flt=f)); out.append((n, dict(flt=f), r)); print(line(n, r, base), flush=True)
    for n, P in EXTRA.items(): r = ev(P); out.append((n, P, r)); print(line(n, r, base), flush=True)
    good = [x for x in out if x[2]['h1'] > base['h1'] and x[2]['h2'] > base['h2']]
    print('\n== pairs of the filters that beat the base in both halves')
    for (n1, P1, _), (n2, P2, _) in itertools.combinations(good, 2):
        P = {**P1, **P2}
        if 'flt' in P1 and 'flt' in P2: P['flt'] = (lambda a, b: lambda *z: a(*z) and b(*z))(P1['flt'], P2['flt'])
        print(line(n1[:22] + ' + ' + n2[:22], ev(P), base), flush=True)
