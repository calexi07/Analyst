# Daily context + lower-timeframe entry for BE Swing (EURUSD first). The daily chart gives the context or the setup,
# the 4H or 1H chart gives the sweep entry; trades are managed on 1H (half at 1R, rest BE, TP 3R, Friday close).
import sys, os, csv, datetime as D
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from swing2 import *; from mtf import load1h, simulate
HERE = os.path.dirname(os.path.abspath(__file__))
U = lambda *a: D.datetime(*a, tzinfo=D.timezone.utc)

def load1d(pair):
    rows = [r for r in csv.DictReader(open(os.path.join(HERE, f'../ohlc/FOREXCOM_{pair}_1D.csv')))]
    days = [(D.date.fromisoformat(r['time'][:10]), float(r['open']), float(r['high']), float(r['low']), float(r['close'])) for r in rows]
    out, trs = {}, []
    for i, (d, o, h, l, c) in enumerate(days):
        prev = days[i - 1] if i else None
        out[d] = dict(o=o, h=h, l=l, c=c, prev=prev, atr=sum(trs[-14:]) / 14 if len(trs) >= 14 else None, i=i)
        trs.append(h - l if prev is None else max(h, prev[4]) - min(l, prev[4]))
    return out, days

def ctx_ok(dd, day, d, ctx):
    x = dd.get(day)
    if not x or not x['prev']: return False
    p = x['prev']; pdir = 1 if p[4] > p[1] else -1 if p[4] < p[1] else 0
    if ctx == 'none': return True
    if ctx == 'with': return pdir == d          # yesterday's daily candle closed in the bias direction
    if ctx == 'against': return pdir == -d      # yesterday was a pullback day against the bias
    if ctx == 'dsweep':                          # yesterday's daily candle itself swept the day before and closed back
        pp = days_list[x['i'] - 2] if x['i'] >= 2 else None
        if not pp: return False
        return (p[3] < pp[3] < p[4]) if d > 0 else (p[2] > pp[2] > p[4])
    return True

def sweeps(pair, bars, dd, B, start, end, ctx):
    res = []
    for b in bars:
        if b['t'] < start or b['t'] >= end or b['dow'] > 3: continue
        x = dd.get(b['day'])
        if not x or not x['prev'] or x['atr'] is None: continue
        bi = B.get((pair, b['wk']), ('-', '-', None)); d = 1 if bi[0] == 'U' else -1 if bi[0] == 'D' else 0
        if d == 0 or not ctx_ok(dd, b['day'], d, ctx): continue
        p = x['prev']; lv = p[3] if d > 0 else p[2]
        if (b['l'] < lv < b['c']) if d > 0 else (b['h'] > lv > b['c']):
            res.append(dict(t=b['tc'], d=d, atr=x['atr'], c=b['c'], h=b['h'], l=b['l'], wk=b['wk'], ext=b['l'] if d > 0 else b['h'], gap=bi[2]))
    return res

def daily_setups(pair, h1, dd, B, start, end):
    # pure daily: the daily candle swept the day before and closed back in the bias direction -> enter at the next day's open
    res = []; first = {}
    for b in h1:
        first.setdefault(b['day'], b)
    for day, b in sorted(first.items()):
        if b['t'] < start or b['t'] >= end or b['dow'] > 3: continue
        x = dd.get(day)
        if not x or x['atr'] is None: continue
        bi = B.get((pair, b['wk']), ('-', '-', None)); d = 1 if bi[0] == 'U' else -1 if bi[0] == 'D' else 0
        if d and ctx_ok(dd, day, d, 'dsweep'):
            res.append(dict(t=b['t'], d=d, atr=x['atr'], c=b['o'], h=b['h'], l=b['l'], wk=b['wk'], ext=x['prev'][3] if d > 0 else x['prev'][2], gap=bi[2]))
    return res

if __name__ == '__main__':
    pair = sys.argv[1] if len(sys.argv) > 1 else 'EURUSD'
    B = bias_table(); H = [(U(2026, 9, 27, 21), U(2026, 10, 25, 21)), (U(2026, 10, 25, 21), U(2026, 11, 22))]
    dd, days_list = load1d(pair); b4 = load(pair); h1 = load1h(pair)
    def show(name, S_fn):
        parts = [simulate(pair, h1, S_fn(a, b), 'close4h') for a, b in H]; allt = sum(parts, []); R = sum(x['R'] for x in allt)
        print(f"{name:<52} {len(allt):3}tr " + ' / '.join(f"{sum(x['R'] for x in t):+5.1f}" for t in parts) + f" = {R:+5.1f}R  per trade {R/max(len(allt),1):+.2f}")
    print(f'{pair}, bias weeks W40-W47, managed on 1H')
    for ctx, cname in [('none', 'no daily filter'), ('with', 'yesterday closed WITH the bias'), ('against', 'yesterday closed AGAINST the bias (pullback)'), ('dsweep', 'yesterday was a daily sweep + reclaim')]:
        show(f'Daily: {cname} + 4H sweep entry', lambda a, b, c=ctx: sweeps(pair, b4, dd, B, a, b, c))
        show(f'Daily: {cname} + 1H sweep entry', lambda a, b, c=ctx: sweeps(pair, h1, dd, B, a, b, c))
    show('Daily sweep + reclaim only, entry at next day open', lambda a, b: daily_setups(pair, h1, dd, B, a, b))
