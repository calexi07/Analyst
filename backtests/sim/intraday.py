# Intraday ideas (max hold 3-4 h) in the week's bias direction, simulated on the 5m path (EURUSD; XAUUSD when exported).
# Bucharest hours. One trade per idea per day. Conservative: stop first when stop and target share a 5m candle.
import sys, os, collections, datetime as D, itertools, json
from zoneinfo import ZoneInfo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness, ltf, macd as M
from smc import B, H, cost_of, pip_of
B.clear(); B.update(harness.B1)
BUC = ZoneInfo('Europe/Bucharest')

def agg15(b5):
    # 15m candles built from the 5m export (when no 15m export exists), with the same ATR(14) as ltf.load
    out = []
    for x in b5:
        t0 = x['t'].replace(minute=x['t'].minute // 15 * 15, second=0)
        if out and out[-1]['t'] == t0:
            y = out[-1]; y['h'] = max(y['h'], x['h']); y['l'] = min(y['l'], x['l']); y['c'] = x['c']
        else: out.append(dict(t=t0, tc=t0 + D.timedelta(minutes=15), o=x['o'], h=x['h'], l=x['l'], c=x['c'], day=x['day'], dow=x['dow'], wk=x['wk'], hr=x['hr']))
    A = None
    for i, b in enumerate(out):
        tr = b['h'] - b['l'] if i == 0 else max(b['h'], out[i - 1]['c']) - min(b['l'], out[i - 1]['c'])
        A = tr if A is None else (A * 13 + tr) / 14; b['atr'] = A if i >= 13 else None
    return out
def prep(p):
    b5 = ltf.load(p, '5')
    try: b15 = ltf.load(p, '15')
    except FileNotFoundError: b15 = agg15(b5)
    for x in b5:
        lt = x['t'].astimezone(BUC); x['lt'] = lt; x['m'] = lt.hour * 60 + lt.minute; x['cd'] = lt.date()
    # daily (NY day) closes -> SMA20 known at the start of each day; previous day high/low
    days = collections.OrderedDict()
    for x in b5:
        d = days.setdefault(x['day'], dict(h=x['h'], l=x['l'], c=x['c'])); d['h'] = max(d['h'], x['h']); d['l'] = min(d['l'], x['l']); d['c'] = x['c']
    ks = list(days); prevd = {}
    for i, k in enumerate(ks):
        prevd[k] = dict(pdh=days[ks[i - 1]]['h'] if i else None, pdl=days[ks[i - 1]]['l'] if i else None,
                        sma=sum(days[q]['c'] for q in ks[i - 20:i]) / 20 if i >= 20 else None,
                        datr=sum(days[q]['h'] - days[q]['l'] for q in ks[i - 14:i]) / 14 if i >= 14 else None)
    # 15m indicators keyed by close time
    m, sg, hs = M.macd(b15)
    e20 = e50 = None; I15 = {}
    for k, x in enumerate(b15):
        e20 = x['c'] if e20 is None else e20 + 2 / 21 * (x['c'] - e20); e50 = x['c'] if e50 is None else e50 + 2 / 51 * (x['c'] - e50)
        I15[x['tc']] = dict(k=k, h=hs[k], h1=hs[k - 1] if k else float('nan'), e20=e20, e50=e50, atr=x['atr'], o=x['o'], c=x['c'], l=x['l'], hh=x['h'])
    return b5, prevd, I15

DEF = dict(idea='lon_orb', tp=2.0, tmax=48, dirm='bias', sl='range', k=1.5, start=(9, 0), last=(18, 0), maxtr=1)
def run(p, data, P, start, end):
    P = {**DEF, **P}; b5, prevd, I15 = data; cost = cost_of(p) * pip_of(p); res = []
    byday = collections.OrderedDict()
    for i, x in enumerate(b5): byday.setdefault(x['cd'], []).append(i)
    for cd, idx in byday.items():
        x0 = b5[idx[0]]
        if x0['t'] < start or x0['t'] >= end or x0['lt'].weekday() > 4: continue
        bi = B.get((p, b5[idx[len(idx) // 2]]['wk']), ('-',))[0]; bd = 1 if bi == 'U' else -1 if bi == 'D' else 0
        if P['dirm'] in ('long', 'short'): bd = 1
        pdx = prevd.get(b5[idx[len(idx) // 2]]['day'], {})
        if P['dirm'] in ('long', 'short'): bd = 1 if P['dirm'] == 'long' else -1
        if P['dirm'] == 'anti': bd = -bd
        if P['dirm'] == 'trend':
            s_ = pdx.get('sma'); bd = 0 if s_ is None else (1 if x0['c'] > s_ else -1)
        if bd == 0: continue
        if P['dirm'] == 'both':
            s = pdx.get('sma')
            if s is None or (x0['c'] - s) * bd <= 0: continue
        d = bd; ntr = 0
        # session ranges from completed bars
        def rng(m0, m1):
            v = [b5[i] for i in idx if m0 <= b5[i]['m'] < m1]
            return (max(y['h'] for y in v), min(y['l'] for y in v)) if v else (None, None)
        asia = rng(2 * 60, 9 * 60); lon1 = rng(9 * 60, 10 * 60); ny1 = rng(15 * 60 + 30, 16 * 60)
        vw_n = vw_s = 0.0; beyond = False; swept = False; ext = None
        pend = None; pos = None; t0 = P['start'][0] * 60 + P['start'][1]; t1 = P['last'][0] * 60 + P['last'][1]
        for j in idx:
            x = b5[j]; mm = x['m']
            if mm >= 9 * 60: vw_n += 1; vw_s += (x['h'] + x['l'] + x['c']) / 3
            vw = vw_s / vw_n if vw_n else None
            # manage position
            if pos:
                px = None
                if (x['l'] <= pos['sl']) if d > 0 else (x['h'] >= pos['sl']): px = min(x['o'], pos['sl']) if d > 0 else max(x['o'], pos['sl'])
                elif (x['h'] >= pos['tp']) if d > 0 else (x['l'] <= pos['tp']): px = max(x['o'], pos['tp']) if d > 0 else min(x['o'], pos['tp'])
                elif j - pos['j'] >= P['tmax'] or mm >= 22 * 60 - 5: px = x['c']
                if px is not None:
                    res.append(dict(p=p, d=d, t=pos['t'], tx=x['tc'], wk=x['wk'], R=d * (px - pos['e']) / pos['r'] - cost / pos['r'], cd=cd)); pos = None
                continue
            if ntr >= P['maxtr']: break
            # pending stop order
            if pend:
                if mm >= pend['until']: pend = None
                elif (x['h'] >= pend['e']) if d > 0 else (x['l'] <= pend['e']):
                    e = max(x['o'], pend['e']) if d > 0 else min(x['o'], pend['e']); r = abs(e - pend['sl'])
                    if r > 0:
                        pos = dict(e=e, r=r, sl=pend['sl'], tp=e + d * P['tp'] * r, t=x['t'], j=j); ntr += 1; pend = None
                        if (x['l'] <= pos['sl']) if d > 0 else (x['h'] >= pos['sl']):
                            res.append(dict(p=p, d=d, t=x['t'], tx=x['tc'], wk=x['wk'], R=-1 - cost / r, cd=cd)); pos = None
                    continue
            if not (t0 <= mm < t1) or pend: continue
            I = P['idea']; A = I15.get(x['tc'], {}).get('atr') or (I15.get(x['tc'] - D.timedelta(minutes=5), {}) or {}).get('atr')
            sig = None   # (entry kind, price, stop)
            if I == 'lon_orb' and mm >= 10 * 60 and lon1[0] and mm < 13 * 60:
                hi, lo = lon1; sl = (lo if d > 0 else hi) if P['sl'] == 'range' else (hi + lo) / 2
                pend = dict(e=hi if d > 0 else lo, sl=sl, until=13 * 60); continue
            if I == 'asia_bo' and mm >= 9 * 60 and asia[0] and mm < 13 * 60:
                hi, lo = asia; sl = (hi + lo) / 2 if P['sl'] != 'range' else (lo if d > 0 else hi)
                pend = dict(e=hi if d > 0 else lo, sl=sl, until=13 * 60); continue
            if I == 'ny_orb' and mm >= 16 * 60 and ny1[0] and mm < 18 * 60:
                hi, lo = ny1; sl = (lo if d > 0 else hi) if P['sl'] == 'range' else (hi + lo) / 2
                pend = dict(e=hi if d > 0 else lo, sl=sl, until=18 * 60); continue
            if I in ('asia_sweep', 'pd_sweep'):
                lvl = (asia[1] if d > 0 else asia[0]) if I == 'asia_sweep' else (pdx.get('pdl') if d > 0 else pdx.get('pdh'))
                if lvl is None or (I == 'asia_sweep' and not (9 * 60 <= mm < 13 * 60)): continue
                if (x['l'] < lvl) if d > 0 else (x['h'] > lvl):
                    swept = True; ext = x['l'] if d > 0 and (ext is None or x['l'] < ext) else (x['h'] if d < 0 and (ext is None or x['h'] > ext) else ext)
                if swept and ((x['c'] > lvl) if d > 0 else (x['c'] < lvl)):
                    sig = (x['c'], ext - d * 0.1 * (A or 0))
            if I == 'vwap_pb' and vw and mm >= 10 * 60 and A:
                if (x['c'] - vw) * d > P['k'] * A: beyond = True
                if beyond and ((x['l'] <= vw) if d > 0 else (x['h'] >= vw)) and (x['c'] - x['o']) * d > 0 and (x['c'] - vw) * d > 0:
                    sig = (x['c'], (x['l'] if d > 0 else x['h']) - d * 0.3 * A)
            if I15.get(x['tc']) and A:
                q = I15[x['tc']]
                if I == 'm15_macd' and q['h'] * d > 0 and q['h1'] * d <= 0: sig = (x['c'], x['c'] - d * P['k'] * A)
                if I == 'ema_pb' and (q['e20'] - q['e50']) * d > 0 and ((q['l'] <= q['e20'] <= q['c']) if d > 0 else (q['hh'] >= q['e20'] >= q['c'])) and (q['c'] - q['o']) * d > 0:
                    sig = (x['c'], (q['l'] if d > 0 else q['hh']) - d * 0.2 * A)
                if I == 'random' and mm == 10 * 60 + ((cd.toordinal() * 37 + ntr * 11) % 7) * 60 - 5:
                    sig = (x['c'], x['c'] - d * P['k'] * A)
            if sig:
                e, sl = sig; r = abs(e - sl)
                if A and 0.3 * A <= r <= 4 * A and (e - sl) * d > 0:
                    pos = dict(e=e, r=r, sl=sl, tp=e + d * P['tp'] * r, t=x['t'], j=j); ntr += 1
        if pos:   # end of data
            x = b5[idx[-1]]; res.append(dict(p=p, d=d, t=pos['t'], tx=x['tc'], wk=x['wk'], R=d * (x['c'] - pos['e']) / pos['r'] - cost / pos['r'], cd=cd))
    return res

DATA = {}
def ev(pairs, P):
    hs = []
    for a, c in H:
        t = []
        for p in pairs:
            if p not in DATA: DATA[p] = prep(p)
            t += run(p, DATA[p], P, a, c)
        hs.append(t)
    t = sorted(hs[0] + hs[1], key=lambda x: x['tx']); eq = pk = dd = 0
    for x in t: eq += x['R']; pk = max(pk, eq); dd = min(dd, eq - pk)
    return dict(n=len(t), h1=sum(x['R'] for x in hs[0]), h2=sum(x['R'] for x in hs[1]), dd=dd, win=sum(x['R'] > 0 for x in t),
                hold=sorted((x['tx'] - x['t']).total_seconds() / 3600 for x in t))

if __name__ == '__main__':
    pairs = sys.argv[1].split(',')
    IDEAS = ['random', 'lon_orb', 'asia_bo', 'ny_orb', 'asia_sweep', 'pd_sweep', 'vwap_pb', 'm15_macd', 'ema_pb']
    out = []
    for I, tp, tm, dm, k, sl in itertools.product(IDEAS, [1.0, 1.5, 2.0, 3.0], [36, 48], ['bias', 'both'], [1.0, 1.5, 2.0], ['range', 'mid']):
        if I not in ('random', 'vwap_pb', 'm15_macd') and k != 1.5: continue
        if I not in ('lon_orb', 'asia_bo', 'ny_orb') and sl == 'mid': continue
        for mx in ([1, 2] if I in ('m15_macd', 'ema_pb', 'vwap_pb', 'random') else [1]):
            P = dict(idea=I, tp=tp, tmax=tm, dirm=dm, k=k, sl=sl, maxtr=mx); r = ev(pairs, P); r.pop('hold'); out.append((P, r))
        print(I, tp, tm, dm, flush=True) if tp == 3.0 and tm == 48 and dm == 'both' and k == 1.5 and sl == 'range' else None
    json.dump(out, open(f'/tmp/intraday_{"_".join(pairs)}.json', 'w')); print(len(out), 'runs')
