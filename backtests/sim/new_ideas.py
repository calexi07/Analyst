# Quick data checks for five new strategy ideas (none uses the entry-C engine).
import sys, os, csv, json, math, glob, datetime as D, statistics as St, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from swing2 import *
HERE = os.path.dirname(os.path.abspath(__file__))
h = json.load(open(os.path.join(HERE, '../../pine/history.json')))
M = list(csv.DictReader(open(os.path.join(HERE, '../ohlc/FOREXCOM_EURUSD_1D.csv'))))
PAIRS = [k[:-2] for k in M[0] if k.endswith(' %')]
day = {r['time']: {p: float(r[p + ' %']) for p in PAIRS if r[p + ' %'] not in ('', None)} for r in M}
days = sorted(day)
def wk_of(ds): return D.date.fromisoformat(ds).isocalendar()[:2]
# ---------- 1) Weekly matchup: strongest vs weakest currency by engine score, Monday open -> Friday close, no management
print('1) WEEKLY MATCHUP (engine scores, hold Mon->Fri, risk = 1.5 x avg daily range)')
tot = []; tot3 = []
for W in h['weeks']:
    if (W['y'], W['w']) < (2026, 40): continue
    cc = {k: v for k, v in W['ccy'].items() if k != 'XAU'}
    best = max(cc, key=cc.get); worst = min(cc, key=cc.get)
    wdays = [d for d in days if wk_of(d) == (W['y'], W['w'])]
    prev = [d for d in days if d < (wdays[0] if wdays else '9')][-20:]
    def pair_R(b, q):
        p, s = (b + q, 1) if b + q in PAIRS else (q + b, -1)
        ret = sum(math.log(1 + s * day[d].get(p, 0) / 100) for d in wdays)
        rng = St.mean(abs(day[d].get(p, 0)) for d in prev) / 100 * 1.4
        return ret / (1.5 * rng), p, s
    r, p, s = pair_R(best, worst); tot.append(r)
    gaps = sorted(((v['bs'] - v['qs'], k) for k, v in W['pairs'].items() if k != 'XAUUSD' and v.get('bs') is not None), key=lambda x: -abs(x[0]))[:3]
    r3 = [pair_R(k[:3], k[3:])[0] * (1 if g > 0 else -1) for g, k in gaps]; tot3.append(St.mean(r3))
    print(f"   W{W['w']}: long {best}({cc[best]:+d}) vs {worst}({cc[worst]:+d}) via {p}{' (short)' if s < 0 else ''}: {r:+.2f}R | top-3 |gap| pairs avg {St.mean(r3):+.2f}R")
print(f"   total top pair {sum(tot):+.1f}R ({sum(x > 0 for x in tot)}/{len(tot)} weeks up); top-3 basket {sum(tot3):+.1f}R")
# ---------- daily bars from 4H for the long-history pairs (3 years)
LONG = ['GBPUSD', 'AUDUSD', 'USDJPY', 'USDCHF', 'USDCAD', 'XAUUSD']
def daily(p):
    out = collections.OrderedDict()
    for b in load(p):
        d = out.setdefault(b['day'], dict(day=b['day'], o=b['o'], h=b['h'], l=b['l'], c=b['c'], wk=b['wk']))
        d['h'] = max(d['h'], b['h']); d['l'] = min(d['l'], b['l']); d['c'] = b['c']
    L = list(out.values())
    for i, d in enumerate(L):
        tr = [max(x['h'], L[j - 1]['c']) - min(x['l'], L[j - 1]['c']) for j, x in enumerate(L[max(1, i - 13):i + 1], start=max(1, i - 13))]
        d['atr'] = St.mean(tr) if len(tr) >= 10 else None
        cl = [x['c'] for x in L[max(0, i - 199):i + 1]]
        d['sma200'] = St.mean(cl) if len(cl) == 200 else None; d['sma50'] = St.mean(cl[-50:]) if len(cl) >= 50 else None
        c20 = [x['c'] for x in L[max(0, i - 19):i + 1]]
        if len(c20) == 20:
            m = St.mean(c20); sd = St.pstdev(c20); d['bbw'] = 4 * sd / m
        else: d['bbw'] = None
    return L
DL = {p: daily(p) for p in LONG}
def hold(L, i, d, stop_atr, max_days, trail=None):
    # enter at next day's open, fixed stop (and optional chandelier), exit at max_days close
    if i + 1 >= len(L): return None
    e = L[i + 1]['o']; A = L[i]['atr']; sl = e - d * stop_atr * A; best = e
    for j in range(i + 1, min(len(L), i + 1 + max_days)):
        x = L[j]
        if (x['l'] <= sl) if d > 0 else (x['h'] >= sl): return (sl - e) * d / (stop_atr * A), j
        best = max(best, x['h']) if d > 0 else min(best, x['l'])
        if trail: sl = max(sl, best - trail * A) if d > 0 else min(sl, best + trail * A)
    j = min(len(L), i + 1 + max_days) - 1
    return (L[j]['c'] - e) * d / (stop_atr * A), j
def yr_report(name, fn):
    by = collections.defaultdict(list)
    for p, L in DL.items():
        i = 210
        while i < len(L) - 1:
            r = fn(L, i)
            if r: R, j = r; by[L[i]['day'].year].append(R); i = j + 1
            else: i += 1
    allr = sum(by.values(), [])
    print(f"   {name}: {len(allr)} trades, {sum(allr):+.1f}R, win {sum(x > 0 for x in allr) / max(1, len(allr)):.0%}, by year " + ', '.join(f"{y}:{sum(v):+.0f}" for y, v in sorted(by.items())))
print('\n2) TREND + CARRY proxy (no rate history here): 50/200 trend, hold 20 days, stop 3 ATR, chandelier 3 ATR -- 6 pairs, 3 years')
def trend(L, i):
    d = L[i]
    if None in (d['sma200'], d['sma50'], d['atr']): return None
    prev = L[i - 1]
    up = d['sma50'] > d['sma200'] and prev['sma50'] is not None and prev['sma50'] <= prev['sma200']
    dn = d['sma50'] < d['sma200'] and prev['sma50'] is not None and prev['sma50'] >= prev['sma200']
    if not (up or dn): return None
    return hold(L, i, 1 if up else -1, 3, 60, trail=3)
yr_report('golden/death cross, trail 3 ATR', trend)
print('\n3) VOLATILITY SQUEEZE: Bollinger width at a 120-day low, break of the 20-day range in the 200-SMA direction, stop 2 ATR, trail 3 ATR, max 30 days')
def squeeze(L, i):
    d = L[i]
    if None in (d['bbw'], d['sma200'], d['atr']): return None
    w = [x['bbw'] for x in L[i - 120:i] if x['bbw'] is not None]
    if len(w) < 100 or L[i - 1]['bbw'] is None or L[i - 1]['bbw'] > min(w) * 1.1: return None
    hi = max(x['h'] for x in L[i - 20:i]); lo = min(x['l'] for x in L[i - 20:i])
    dr = 1 if d['c'] > d['sma200'] else -1
    if (d['c'] > hi) if dr > 0 else (d['c'] < lo): return hold(L, i, dr, 2, 30, trail=3)
    return None
yr_report('squeeze breakout', squeeze)
print('\n4) WEEK-ANCHORED VWAP PULLBACK (TWAP proxy, no FX volume in the exports): 8 USD pairs W40-47, bias direction,')
print('   limit at the week-to-date average price after price was 0.5 ATR beyond it, stop 1 daily ATR, hold to Friday close')
B = bias_table(); U = lambda *a: D.datetime(*a, tzinfo=D.timezone.utc)
res = []
for p in USD:
    bars = load(p); wk = None; s = n = 0; armed = False; pos = None
    for b in bars:
        if b['wk'] != wk: wk = b['wk']; s = n = 0; armed = False
        tw = s / n if n else None
        if pos:
            d, e, sl, rk = pos
            if (b['l'] <= sl) if d > 0 else (b['h'] >= sl): res.append((p, -1 - 1e-4 / rk)); pos = None
            elif b['dow'] == 4 and b['tc'].astimezone(NY).hour >= 16: res.append((p, (b['c'] - e) * d / rk)); pos = None
        elif tw and b['t'] >= U(2026, 9, 27, 21) and b['atr'] and b['dow'] <= 3:
            bi = B.get((p, b['wk']), ('-',))[0]; d = 1 if bi == 'U' else -1 if bi == 'D' else 0
            if d and (b['c'] - tw) * d > 0.5 * b['atr']: armed = True
            if d and armed and ((b['l'] <= tw) if d > 0 else (b['h'] >= tw)):
                pos = (d, tw, tw - d * b['atr'], b['atr']); armed = False
        s += (b['h'] + b['l'] + b['c']) / 3; n += 1
print(f"   {len(res)} trades, {sum(r for _, r in res):+.1f}R, win {sum(r > 0 for _, r in res) / max(1, len(res)):.0%}")
