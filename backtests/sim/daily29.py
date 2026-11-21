# Daily close-to-close study on all 29 pairs (Daily Observer-style % columns in the EURUSD 1D export, May 2022 - Nov 2026).
# No intraday highs/lows for 28 of the pairs, so there are no stops/targets here: trades are held to Friday's close and measured
# in units of the pair's 20-day daily standard deviation (sigma). Mechanics with the trend as direction on 4.5 years, and the
# fundamental bias on the bias weeks W40-W47 across all 29 pairs.
import csv, os, math, json, statistics as S, datetime as D, collections
HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, '../ohlc/FOREXCOM_EURUSD_1D.csv'))))
PAIRS = [c[:-2] for c in rows[0] if c.endswith(' %')]
dates = [D.date.fromisoformat(r['time'][:10]) for r in rows]
ret = {p: [float(r[p + ' %']) / 100 if r[p + ' %'] not in ('', None) else 0.0 for r in rows] for p in PAIRS}
lr = {p: [math.log1p(x) for x in ret[p]] for p in PAIRS}
N = len(dates)
def sd20(p, i): x = lr[p][max(0, i - 20):i]; return S.pstdev(x) if len(x) >= 15 else None
def mom(p, i, n=20): return sum(lr[p][i - n:i]) if i >= n else None
weeks = collections.OrderedDict()
for i, d in enumerate(dates): weeks.setdefault(d.isocalendar()[:2], []).append(i)
h = json.load(open(os.path.join(HERE, '../../pine/history.json')))
BIAS = {((W['y'], W['w']), p): x['b'] for W in h['weeks'] for p, x in W['pairs'].items()}
def trade(p, i_entry_close, i_exit, d):
    s = sd20(p, i_entry_close + 1)
    if not s: return None
    return d * sum(lr[p][i_entry_close + 1:i_exit + 1]) / s
def run(dirfn, rule, wk_filter=None):
    out = []
    for wk, idx in weeks.items():
        if wk_filter and not wk_filter(wk): continue
        if len(idx) < 4: continue
        fri = idx[-1]
        for p in PAIRS:
            d = dirfn(p, wk, idx[0])
            if not d: continue
            ent = None
            if rule == 'hold': ent = idx[0] - 1                               # enter at last Friday's close = Monday open
            elif rule == 'wtd':                                               # Monday closed in the direction -> enter at Monday close
                if lr[p][idx[0]] * d > 0: ent = idx[0]
            elif rule == 'pull':                                              # first day (Mon-Thu) that closed against the direction
                for i in idx[:-1]:
                    if lr[p][i] * d < 0: ent = i; break
            elif rule == 'pull_wtd':                                          # first pullback day after which week-to-date is still with the direction
                for k, i in enumerate(idx[:-1]):
                    if lr[p][i] * d < 0 and sum(lr[p][idx[0]:i + 1]) * d > 0: ent = i; break
            if ent is None or ent >= fri: continue
            r = trade(p, ent, fri, d)
            if r is not None: out.append((wk, p, r))
    return out
def rep(name, tr):
    if not tr: print(f'{name:<52} no trades'); return
    v = [x[2] for x in tr]; m = S.mean(v); t = m / (S.stdev(v) / len(v) ** .5)
    yrs = collections.defaultdict(list)
    for wk, p, r in tr: yrs[wk[0]].append(r)
    print(f"{name:<52} {len(v):5}tr  mean {m:+.3f}σ  hit {sum(x > 0 for x in v)/len(v):.0%}  t {t:+.1f}  by year " + ' '.join(f"{y}:{S.mean(z):+.2f}" for y, z in sorted(yrs.items())))
trend = lambda n: (lambda p, wk, i0: (1 if (mom(p, i0, n) or 0) > 0 else -1) if mom(p, i0, n) is not None else 0)
print('=== 4.5 years, trend (sign of the last N days) as direction, all 29 pairs ===')
for n in (20, 60):
    for rule in ('hold', 'wtd', 'pull', 'pull_wtd'):
        rep(f'trend {n}d + {rule}', run(trend(n), rule))
# cross-sectional currency momentum: strongest vs weakest currency by 20-day strength, hold the week
CCY = ['USD', 'EUR', 'GBP', 'JPY', 'CHF', 'CAD', 'AUD', 'NZD']
def strength(i0, n=20):
    s = {c: [] for c in CCY}
    for p in PAIRS:
        if p == 'XAUUSD' or mom(p, i0, n) is None: continue
        m = mom(p, i0, n); s[p[:3]].append(m); s[p[3:]].append(-m)
    return {c: S.mean(v) for c, v in s.items() if v}
cs = []
for wk, idx in weeks.items():
    if len(idx) < 4 or idx[0] < 21: continue
    st = strength(idx[0]); top = max(st, key=st.get); bot = min(st, key=st.get)
    p = top + bot if top + bot in PAIRS else bot + top; d = 1 if p == top + bot else -1
    r = trade(p, idx[0] - 1, idx[-1], d)
    if r is not None: cs.append((wk, p, r))
rep('cross-sectional: strongest vs weakest currency', cs)
print('\n=== bias weeks (W40-W47), fundamental bias as direction, all 29 pairs ===')
bias = lambda p, wk, i0: {'U': 1, 'D': -1}.get(BIAS.get((wk, p)), 0)
inb = lambda wk: wk[0] == 2026 and 40 <= wk[1] <= 47
for rule in ('hold', 'wtd', 'pull', 'pull_wtd'):
    rep(f'bias + {rule}', run(bias, rule, inb))
both = lambda p, wk, i0: (bias(p, wk, i0) if bias(p, wk, i0) == trend(20)(p, wk, i0) else 0)
for rule in ('hold', 'wtd', 'pull'):
    rep(f'bias + trend20 agree + {rule}', run(both, rule, inb))
for rule in ('hold', 'wtd', 'pull'):
    rep(f'trend 20d only (same weeks) + {rule}', run(trend(20), rule, inb))
