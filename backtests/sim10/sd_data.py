# data adapters for sd.py: 10y 15m (ejtraderLabs) and Aug-Nov 2026 5m (FOREX.com exports, with the weekly bias)
import sys, datetime as D
sys.path.insert(0, '/home/claude/analyst/backtests/sim10'); sys.path.append('/home/claude/analyst/backtests/sim')
from sd import atr_
def agg(bars, mins):
    out = []
    for b in bars:
        m = b['t'].hour * 60 + b['t'].minute; k0 = m // mins * mins
        k = b['t'].replace(hour=k0 // 60, minute=k0 % 60, second=0)
        if out and out[-1]['t'] == k: y = out[-1]; y['h'] = max(y['h'], b['h']); y['l'] = min(y['l'], b['l']); y['c'] = b['c']
        else: out.append(dict(t=k, tc=k + D.timedelta(minutes=mins), o=b['o'], h=b['h'], l=b['l'], c=b['c']))
    atr_(out); return out
def ten_year(p):
    from core import load
    from ideas import dirs_for
    bars, ks, info = load(p)
    l = [dict(t=x['t'], o=x['o'], h=x['h'], l=x['l'], c=x['c'], atr=x['atr'], d=x['d']) for x in bars]
    trend = lambda x: dirs_for(info[x['d']], 'trend') if x['d'] in info else ()
    return l, {'1H': agg(l, 60), '4H': agg(l, 240)}, trend
def y2026(p, tf_ltf='5'):
    import intraday as T, harness
    from smc import H
    b5 = T.prep(p)[0]
    l = [dict(t=x['t'], o=x['o'], h=x['h'], l=x['l'], c=x['c'], wk=x['wk'], day=x['day']) for x in b5]
    if tf_ltf == '15':
        l2 = agg(l, 15)
        for y in l2: y['wk'] = y['t'].isocalendar()[:2]
        l = l2
    atr_(l)
    # HTF bars aligned to Bucharest-agnostic UTC hours (FOREX.com 4H opens at 17:00 NY ≈ 21/22 UTC; plain UTC buckets used)
    hh = {'1H': agg(l, 60), '4H': agg(l, 240)}
    def biasf(x):
        if not any(a <= x['t'] < e for a, e in H): return ()
        r = harness.B1.get((p, x['wk'] if 'wk' in x else x['t'].isocalendar()[:2]))
        return ((1 if r[0] == 'U' else -1),) if r and r[0] in 'UD' else ()
    return l, hh, biasf
