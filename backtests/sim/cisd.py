# "HTF Sweep CISD Setups" (WillyAlgoTrader v1.7.1) default model rebuilt for testing:
# HTF low/high swept (previous HTF candle or any untaken HTF level of the last 10 HTF candles) -> on the chart timeframe a
# displacement close (body >= 0.5 ATR) through the last confirmed pivot (len 3) formed before the swept extreme = breaker ->
# limit at the breaker candle's close, stop at the swept extreme, risk 0.25-3 ATR, TP1/TP2/TP3 = 1/2/3R, break-even after TP1,
# trade closes at TP3 or at the stop. Conservative intrabar model. Shorts = the same logic on mirrored prices.
import sys, os, datetime as D, statistics as St, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smc import prep, B, H, PRE, USDP, EURP, U, cost_of, pip_of
from swing2 import NY

def mirror(b, d):
    if d > 0: return b
    out = []
    for x in b:
        y = dict(x); y['o'], y['h'], y['l'], y['c'] = -x['o'], -x['l'], -x['h'], -x['c']; out.append(y)
    return out

def htf_key(x, htf):
    if htf == 'D': return x['day']
    ny = (x['t'] + D.timedelta(hours=7)).astimezone(NY)
    return (x['day'], ny.hour // 4)

DEF = dict(htf='D', piv=3, wait=36, age=120, disp=0.5, minr=0.25, maxr=3.0, tp=(1, 2, 3), be=True, pend=60, lookback=10,
           hours=None, bias=False, dirs=(1, -1), cool=0)

def run_dir(p, b0, d, P, start, end):
    P = {**DEF, **P}; b = mirror(b0, d); cost = cost_of(p) * pip_of(p); n = len(b)
    res = []; ctx = None; pend = None; pos = None
    htf = []; cur = None; untaken = []
    piv = []                     # confirmed pivot highs: (pivot index, high, close)
    L = P['piv']
    for i, x in enumerate(b):
        A = x['atr']
        # HTF candles
        k = htf_key(x, P['htf'])
        if cur is None or cur['k'] != k:
            if cur is not None:
                htf.append(cur); untaken.append(cur['l']); untaken[:] = untaken[-P['lookback']:]
            cur = dict(k=k, l=x['l'], h=x['h'])
        else: cur['l'] = min(cur['l'], x['l']); cur['h'] = max(cur['h'], x['h'])
        if i >= 2 * L and b[i - L]['h'] == max(y['h'] for y in b[i - 2 * L:i + 1]) and b[i - L]['h'] > max(y['h'] for y in b[i - 2 * L:i - L]):
            piv.append((i - L, b[i - L]['h'], b[i - L]['c'])); piv[:] = piv[-40:]
        # ---- open trade
        if pos:
            sl = pos['e'] if pos['be'] else pos['sl']
            if x['l'] <= sl:                                     # conservative: stop first
                px = min(x['o'], sl); res.append(dict(p=p, d=d, t=pos['t'], tx=x['tc'], wk=pos['wk'], R=(px - pos['e']) / pos['r'] - cost / pos['r'], why='BE' if pos['be'] else 'SL')); pos = None
            elif x['h'] >= pos['t3']:
                px = max(x['o'], pos['t3']); res.append(dict(p=p, d=d, t=pos['t'], tx=x['tc'], wk=pos['wk'], R=(px - pos['e']) / pos['r'] - cost / pos['r'], why='TP3')); pos = None
            else:
                if P['be'] and x['h'] >= pos['t1']: pos['be'] = True
        # ---- pending limit
        if pend and not pos:
            if i - pend['i'] > P['pend'] or x['h'] >= pend['t1'] and x['l'] > pend['e']: pend = None
            elif x['l'] <= pend['e']:
                e = min(pend['e'], x['o']); r = e - pend['sl']
                pos = dict(t=x['t'], wk=x['wk'], e=e, sl=pend['sl'], r=r, t1=e + P['tp'][0] * r, t3=e + P['tp'][2] * r, be=False); pend = None
                if x['l'] <= pos['sl']:
                    res.append(dict(p=p, d=d, t=x['t'], tx=x['tc'], wk=pos['wk'], R=-1 - cost / r, why='SL fill bar')); pos = None
        if not (start <= x['t'] < end) or A is None: ctx = None; continue
        # ---- sweep -> context
        swept = [lv for lv in untaken if x['l'] < lv]
        if swept:
            untaken[:] = [lv for lv in untaken if lv not in swept]
            if ctx is None: ctx = dict(trig=i, created=i, ext=x['l'], extBar=i, brk=None)
            else: ctx['trig'] = i
        if ctx is None: continue
        if i - ctx['trig'] > P['wait'] or i - ctx['created'] > P['age']: ctx = None; continue
        if x['l'] < ctx['ext']: ctx['ext'] = x['l']; ctx['extBar'] = i; continue      # new extreme: structure must form after it
        if pos or pend: continue
        bi_ = B.get((p, x['wk']), ('-',))[0]; bd = 1 if bi_ == 'U' else -1 if bi_ == 'D' else 0
        if P['bias'] and bd != d: continue
        if P['hours'] and not (P['hours'][0] <= x['hr'] < P['hours'][1]): continue
        lv = next(((pb, ph, pc) for pb, ph, pc in reversed(piv) if pb < ctx['extBar'] and pb + L <= i), None)
        if lv and x['c'] > lv[1] and x['c'] - x['o'] >= P['disp'] * A:
            e = lv[2]; sl = ctx['ext']; r = e - sl
            if r > 0 and P['minr'] * A <= r <= P['maxr'] * A and x['c'] > e:
                pend = dict(i=i, e=e, sl=sl, t1=e + P['tp'][0] * r)
            ctx = None
    return res

def run(p, b, P, start, end):
    P = {**DEF, **P}
    return sum([run_dir(p, b, d, P, start, end) for d in P['dirs']], [])

if __name__ == '__main__':
    ALL = USDP + EURP; DATA = {p: prep(p) for p in ALL}
    def ev(P, pairs=ALL, per=H):
        hs = [sum([run(p, DATA[p], P, a, c) for p in pairs], []) for a, c in per]
        t = sorted(sum(hs, []), key=lambda x: x['tx']); eq = pk = dd = 0; wk = collections.defaultdict(float)
        for x in t: eq += x['R']; pk = max(pk, eq); dd = min(dd, eq - pk); wk[x['wk'][1]] += x['R']
        w = [wk.get(q, 0) for q in range(40, 48)]; why = collections.Counter(x['why'] for x in t)
        return f"{len(t):3}tr {', '.join(f'{k} {v}' for k, v in sorted(why.items()))} | {' / '.join(f'{sum(x['R'] for x in h_):+.1f}' for h_ in hs)} = {eq:+6.1f}R dd {dd:+.1f} 2wk[{', '.join(f'{v:+.1f}' for v in w[0::2])}..]"
    for n, P in [('default (1H chart, HTF = Daily), both directions', {}),
                 ('  + only engine bias direction', dict(bias=True)),
                 ('  + bias + hours 06-22', dict(bias=True, hours=(6, 22))),
                 ('HTF = 4H, both directions', dict(htf='4H')),
                 ('  + only engine bias direction', dict(htf='4H', bias=True)),
                 ('  + bias + hours 06-22', dict(htf='4H', bias=True, hours=(6, 22))),
                 ('HTF = D, bias, no break-even', dict(bias=True, be=False)),
                 ('HTF = D, bias, TP 2R', dict(bias=True, tp=(1, 1.5, 2))),
                 ('HTF = 4H, bias, no break-even', dict(htf='4H', bias=True, be=False))]:
        print(f"{n:<50} W40-47: {ev(P)}")
        print(f"{'':<50} before W40 (no bias): {ev({**P, 'bias': False}, per=[PRE])}")
