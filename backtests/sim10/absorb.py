# Absorption ("effort vs result") with tick volume, 10y 2012-2022, 12 instruments, 15m / 1H / 4H. No bias history → trend or none.
# Bar i: makes a new N-bar low (high) → volume ≥ k × the average volume of the same time of day (last 20 days)
#   and a small result: close back in the upper (lower) half of the bar, or a range ≤ the average range.
# Entry: at the close (or after a confirmation close beyond the absorption bar), SL beyond the bar's extreme, TP in R.
import sys, csv, datetime as D, collections
sys.path.insert(0, '/home/claude/analyst/backtests/sim10')
from core import SC, COST, DATA
from ideas import dirs_for
from core import load
def loadv(p, mins):
    s = SC[p]; out = []
    for r in list(csv.reader(open(f'{DATA}/{p}m15.csv')))[1:]:
        t = D.datetime.fromisoformat(r[0]); o, h, l, c = (float(x) * s for x in r[1:5]); v = float(r[5])
        if mins > 15:
            m = t.hour * 60 + t.minute; k0 = m // mins * mins; t = t.replace(hour=k0 // 60, minute=k0 % 60)
            if out and out[-1]['t'] == t:
                y = out[-1]; y['h'] = max(y['h'], h); y['l'] = min(y['l'], l); y['c'] = c; y['v'] += v; continue
        out.append(dict(t=t, o=o, h=h, l=l, c=c, v=v))
    A = None; hist = collections.defaultdict(list)
    for i, x in enumerate(out):
        tr = x['h'] - x['l'] if i == 0 else max(x['h'], out[i-1]['c']) - min(x['l'], out[i-1]['c'])
        A = tr if A is None else (A * 13 + tr) / 14; x['atr'] = A
        key = (x['t'].hour, x['t'].minute); hv = hist[key]
        x['vr'] = x['v'] / (sum(hv) / len(hv)) if len(hv) >= 10 and sum(hv) > 0 else None
        hv.append(x['v'])
        if len(hv) > 20: hv.pop(0)
    return out
def run(b, cost, dirf, N=20, k=2.0, res='close_half', conf=False, tp=2.0, maxh=40, sl_buf=0.1):
    out = []; busy = -1; n = len(b)
    for i in range(N + 1, n - 2):
        if i <= busy: continue
        x = b[i]
        if x['vr'] is None or x['vr'] < k or not x['atr']: continue
        lo = min(y['l'] for y in b[i-N:i]); hi = max(y['h'] for y in b[i-N:i]); rng = x['h'] - x['l']
        if rng <= 0: continue
        d = 1 if x['l'] < lo else -1 if x['h'] > hi else 0
        if not d: continue
        pos = (x['c'] - x['l']) / rng
        if res == 'close_half' and not (pos >= 0.5 if d > 0 else pos <= 0.5): continue
        if res == 'close_third' and not (pos >= 0.67 if d > 0 else pos <= 0.33): continue
        if res == 'small_range' and not (rng <= x['atr'] and (pos >= 0.5 if d > 0 else pos <= 0.5)): continue
        D_ = dirf(x)
        if D_ is not None and d not in D_: continue
        j0 = i + 1; e = x['c']
        if conf:     # next bar must close beyond the absorption bar's opposite extreme
            y = b[i + 1]
            if not ((y['c'] > x['h']) if d > 0 else (y['c'] < x['l'])): continue
            e = y['c']; j0 = i + 2
        s = (x['l'] if d > 0 else x['h']) - d * sl_buf * x['atr']; r = abs(e - s)
        if r <= 0 or r < 0.3 * x['atr']: continue
        t = e + d * tp * r; R = None
        for j in range(j0, min(n, j0 + maxh)):
            y = b[j]
            if (y['l'] <= s) if d > 0 else (y['h'] >= s): R = -1.0; break
            if (y['h'] >= t) if d > 0 else (y['l'] <= t): R = tp; break
        else:
            j = min(n - 1, j0 + maxh - 1); R = d * (b[j]['c'] - e) / r
        out.append((x['t'], R - cost / r)); busy = j
    return out
