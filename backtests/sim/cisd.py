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

DEF = dict(htf='D', piv=3, wait=36, age=120, disp=0.5, minr=0.25, maxr=3.0, tp=(1, 2, 3), pend=60, lookback=10,
           hours=None, bias=False, dirs=(1, -1), cool=0,
           tpR=3, be=1, belock=0, part=0, pfrac=0.5, trail=0, trail2=0, tr2at=2, tract=1, trref='close', swtrail=False, stm=0, sqf=None, mcf=None, tvf=None, xf=None, liq=False, liqmin=1, tmax=0)

def run_dir(p, b0, d, P, start, end):
    P = {**DEF, **P}; b = mirror(b0, d); cost = cost_of(p) * pip_of(p); n = len(b)
    res = []; ctx = None; pend = None; pos = None
    htf = []; cur = None; untaken = []
    piv = []                     # confirmed pivot highs: (pivot index, high, close)
    piv_l = []
    L = P['piv']
    if P['xf']:
        import new5 as _n5
        _XA = d * _n5.ctx_state(P['xf'][0], b0)
    if P['tvf']:
        import tvp as _tv
        _TA = d * _tv.tvp(b0)['act']
    if P['mcf']:
        import macd as _mc
        _mm, _ms, _mh = [d * a for a in _mc.macd(b0)]
    if P['sqf']:
        import sqz as _sq
        _v = d * _sq.squeeze(b0)[0]
    if P['stm']:
        import st as _st
        stup = _st.supertrend(b, 10, P['stm'])[0]
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
        if i >= 2 * L and b[i - L]['l'] == min(y['l'] for y in b[i - 2 * L:i + 1]) and b[i - L]['l'] < min(y['l'] for y in b[i - 2 * L:i - L]):
            piv_l.append((i - L, b[i - L]['l'])); piv_l[:] = piv_l[-40:]
        # ---- open trade
        if pos:
            r = pos['r']; best = pos['best']
            def out(px, why):
                R = (px - pos['e']) / r
                if pos['bank'] is not None: R = P['pfrac'] * pos['bank'] + (1 - P['pfrac']) * R
                res.append(dict(p=p, d=d, t=pos['t'], tx=x['tc'], wk=pos['wk'], R=R - cost / r, why=why))
            if x['l'] <= pos['sl']:                              # conservative: stop first
                px = min(x['o'], pos['sl']); out(px, 'SL' if pos['sl'] < pos['e'] - 1e-12 else 'BE/trail'); pos = None
            elif pos['tp'] is not None and x['h'] >= pos['tp']:
                out(max(x['o'], pos['tp']), 'TP'); pos = None
            elif P['tmax'] and i - pos['i'] >= P['tmax']:
                out(x['c'], 'time'); pos = None
            else:
                pos['best'] = best = max(best, x['h'])
                if P['part'] and pos['bank'] is None and x['h'] >= pos['e'] + P['part'] * r:
                    pos['bank'] = P['part']
                if P['be'] is not None and best >= pos['e'] + P['be'] * r: pos['sl'] = max(pos['sl'], pos['e'] + P['belock'] * r)
                if P['trail'] and best >= pos['e'] + P['tract'] * r:
                    k = P['trail2'] if P['trail2'] and best >= pos['e'] + P['tr2at'] * r else P['trail']
                    ref = x['c'] if P['trref'] == 'close' else best
                    pos['sl'] = max(pos['sl'], ref - k * A)
                if P['stm'] and best >= pos['e'] + P['tract'] * r and stup[i] is not None: pos['sl'] = max(pos['sl'], stup[i])
                if P['swtrail'] and best >= pos['e'] + P['tract'] * r and piv_l:
                    lv_ = piv_l[-1]
                    if lv_[0] > pos['i']: pos['sl'] = max(pos['sl'], lv_[1] - 0.1 * A)
        # ---- pending limit
        if pend and not pos:
            if i - pend['i'] > P['pend'] or x['h'] >= pend['t1'] and x['l'] > pend['e']: pend = None
            elif x['l'] <= pend['e']:
                e = min(pend['e'], x['o']); r = e - pend['sl']
                tp_ = pend['liq'] if P['liq'] and pend['liq'] and pend['liq'] - e >= P['liqmin'] * r else (e + P['tpR'] * r if P['tpR'] else None)
                pos = dict(i=i, t=x['t'], wk=x['wk'], e=e, sl=pend['sl'], r=r, tp=tp_, best=x['h'], bank=None); pend = None
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
        if P.get('maxdow') is not None and x['dow'] > P['maxdow']: continue
        if P['sqf'] == 'pos' and not _v[i] > 0: continue
        if P['sqf'] == 'rising' and not _v[i] > _v[i - 1]: continue
        if P['sqf'] == 'neg' and not _v[i] < 0: continue
        if P['xf'] and not {'agree': _XA[i] == 1, 'notagainst': _XA[i] != -1, 'against': _XA[i] == -1}[P['xf'][1]]: continue
        if P['tvf'] == 'trend' and _TA[i] != 1: continue
        if P['tvf'] == 'counter' and _TA[i] != -1: continue
        if P['mcf'] == 'above' and not _mh[i] > 0: continue
        if P['mcf'] == 'below' and not _mh[i] < 0: continue
        if P['mcf'] == 'trend' and not _mm[i] > 0: continue
        if P['mcf'] == 'counter' and not _mm[i] < 0: continue
        lv = next(((pb, ph, pc) for pb, ph, pc in reversed(piv) if pb < ctx['extBar'] and pb + L <= i), None)
        if lv and x['c'] > lv[1] and x['c'] - x['o'] >= P['disp'] * A:
            e = lv[2]; sl = ctx['ext']; r = e - sl
            if r > 0 and P['minr'] * A <= r <= P['maxr'] * A and x['c'] > e:
                hi_ = [c_['h'] for c_ in htf[-P['lookback']:] if c_['h'] > e]
                pend = dict(i=i, e=e, sl=sl, t1=e + P['tp'][0] * r, liq=min(hi_) if hi_ else None)
            ctx = None
    return res

def run(p, b, P, start, end):
    P = {**DEF, **P}
    return sum([run_dir(p, b, d, P, start, end) for d in P['dirs']], [])

if __name__ == '__main__':
    pass
