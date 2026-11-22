# Entry C with 1H execution: signals from completed 4H candles (bias + SMA20 agree, Mon-Wed, 24h cooldown), orders, stops,
# targets and fills checked on the 1H path; trailing (from the 4H close, x 4H ATR) moves only at 4H closes, as in BE Swing.
import sys, os, csv, datetime as D, statistics as St, collections
from zoneinfo import ZoneInfo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from swing2 import *
from mtf import load1h
BUC = ZoneInfo('Europe/Bucharest')
U = lambda *a: D.datetime(*a, tzinfo=D.timezone.utc)
H = [(U(2026, 9, 27, 21), U(2026, 10, 25, 21)), (U(2026, 10, 25, 21), U(2026, 11, 22))]

def prep4(p):
    bars = load(p); a = None; pc = None
    for i, b in enumerate(bars):
        tr = b['h'] - b['l'] if pc is None else max(b['h'], pc) - min(b['l'], pc)
        a = tr if a is None else (a * 13 + tr) / 14 if i >= 14 else (a * i + tr) / (i + 1)
        b['atr4'] = a if i >= 13 else None; pc = b['c']
    return bars

DEF = dict(rsf=None, xf=None, xx=None, tvf=None, tvx=None, mcf=None, mcx=None, sqf=None, sqx=None, trm='atr', stp=10, stm=3.0, stat=1.0, sttf='4h', slm='atr', stf=False, mingap=0, slk=1.0, entry='C', tp=4, trk=0.75, trk2=0.5, trat=2.0, hours=None, cool=24, dirm='both', maxdow=2, sc=None, fri=True)

def run_c(p, b4, h1, B, P, start, end):
    P = {**DEF, **P}; cost = cost_of(p) * pip_of(p)
    i1 = {b['t']: k for k, b in enumerate(h1)}
    res, lastx, k4 = [], None, 0
    if P['rsf']:
        import bbrsi as _br
        _bas, _sd, _rsi = _br.calc(b4, 20, 6)
    if P['xf'] or P['xx']:
        import new5 as _n5
        _XF = _n5.ctx_state(P['xf'][0], b4) if P['xf'] else None
        _XX = _n5.ctx_state(P['xx'], b4) if P['xx'] else None
        ix4 = {b4[q]['tc']: q for q in range(len(b4))}
    if P['tvf'] or P['tvx']:
        import tvp as _tv
        _T = _tv.tvp(b4); ix4 = {b4[q]['tc']: q for q in range(len(b4))}
    if P['mcf'] or P['mcx']:
        import macd as _mc
        _m, _sg, _hs = _mc.macd(b4); ix4 = {b4[q]['tc']: q for q in range(len(b4))}
    if P['sqf'] or P['sqx']:
        import sqz as _sq
        _v, _on, _off = _sq.squeeze(b4); ix4 = {b4[q]['tc']: q for q in range(len(b4))}
    if P['trm'] != 'atr':
        import st as _st
        _up, _dn, _tr, _ = _st.supertrend(b4, P['stp'], P['stm']); stl = {b4[q]['tc']: (_up[q], _dn[q]) for q in range(len(b4))}
    if P['trm'] != 'atr' or P['slm'] != 'atr' or P['stf']:
        import st as _st
        _u4, _d4, _t4, _ = _st.supertrend(b4, P['stp'], P['stm']); st4 = {b4[q]['tc']: (_u4[q], _d4[q], _t4[q]) for q in range(len(b4))}
        _u1, _d1, _t1, _ = _st.supertrend(h1, P['stp'], P['stm'])
    def dir_at(b):
        bi = B.get((p, b['wk']), ('-', '-', None)); bd = 1 if bi[0] == 'U' else -1 if bi[0] == 'D' else 0
        td = 0 if b['sma20'] is None else (1 if b['c'] > b['sma20'] else -1)
        return (bd if bd == td else 0) if P['dirm'] == 'both' else bd, bi
    i = 0
    while i < len(b4) - 1:
        s = b4[i]
        if s['t'] < start or s['t'] >= end or s['atr4'] is None: i += 1; continue
        if lastx and (s['tc'] - lastx).total_seconds() < P['cool'] * 3600: i += 1; continue
        dr, bi = dir_at(s)
        if dr == 0 or s['dow'] > P['maxdow']: i += 1; continue
        if P['sc'] == 'dir' and (s['c'] - s['o']) * dr <= 0: i += 1; continue
        if P['sc'] == 'ema' and (s['ema'] is None or (s['c'] - s['ema']) * dr <= 0): i += 1; continue
        if P['sqf']:
            v_, v1_ = _v[i], _v[i - 1]
            if v_ != v_ or v1_ != v1_: i += 1; continue
            ok = {'pos': v_ * dr > 0, 'rising': (v_ - v1_) * dr > 0, 'both': v_ * dr > 0 and (v_ - v1_) * dr > 0,
                  'nosqz': not _on[i], 'sqzon': bool(_on[i]), 'fired': bool(_on[max(0, i - 6):i].any()) and not _on[i],
                  'notfade': not (v_ * dr > 0 and (v_ - v1_) * dr < 0), 'neg_rising': v_ * dr < 0 and (v_ - v1_) * dr > 0}[P['sqf']]
            if not ok: i += 1; continue
        if P['rsf']:
            r_ = _rsi[i]; inside = _bas[i] == _bas[i] and abs(s['c'] - _bas[i]) < 2 * _sd[i]
            if r_ != r_ or not {'agree': (r_ - 50) * dr > 0, 'against': (r_ - 50) * dr < 0, 'inside': inside}[P['rsf']]: i += 1; continue
        if P['xf']:
            v_ = _XF[i]
            if not {'agree': v_ == dr, 'notagainst': v_ != -dr, 'against': v_ == -dr}[P['xf'][1]]: i += 1; continue
        if P['tvf']:
            a_, pc_ = _T['act'][i], _T['poc'][i]
            ok = {'trend': a_ == dr, 'notagainst': a_ != -dr, 'poc': pc_ == pc_ and (s['c'] - pc_) * dr > 0,
                  'trend_poc': a_ == dr and pc_ == pc_ and (s['c'] - pc_) * dr > 0, 'young': a_ == dr and i - _T['start'][i] <= 12}[P['tvf']]
            if not ok: i += 1; continue
        if P['mcf']:
            m_, h_, h1_ = _m[i], _hs[i], _hs[i - 1]
            if h_ != h_ or h1_ != h1_: i += 1; continue
            ok = {'above': h_ * dr > 0, 'trend': m_ * dr > 0, 'both': h_ * dr > 0 and m_ * dr > 0, 'hrising': (h_ - h1_) * dr > 0,
                  'notfade': not (h_ * dr > 0 and (h_ - h1_) * dr < 0), 'pullback': m_ * dr > 0 and h_ * dr < 0}[P['mcf']]
            if not ok: i += 1; continue
        if P['mingap'] and (bi[2] is None or abs(bi[2]) < P['mingap']): i += 1; continue
        if P.get('flt') and not P['flt'](p, i, s, dr, bi): i += 1; continue
        if P.get('maxloss') is not None and sum(1 for x in res if x['wk'] == s['wk'] and x['R'] < 0) >= P['maxloss']: i += 1; continue
        if P.get('maxwk') and sum(1 for x in res if x['wk'] == s['wk']) >= P['maxwk']: i += 1; continue
        lvl = s['h'] if dr > 0 else s['l']; risk = s['atr4'] * P['slk']
        if P['stf'] or P['slm'] != 'atr':
            u4, d4, t4 = st4.get(s['tc'], (None, None, None))
            if P['stf'] and t4 != dr: i += 1; continue
            if P['slm'] != 'atr':
                ln = u4 if dr > 0 else d4
                if ln is None: i += 1; continue
                dist = abs(lvl - ln) + (0.1 * s['atr4'] if P['slm'] == 'st' else 0)
                if P['slm'] == 'st': risk = dist
                elif P['slm'] == 'wider': risk = max(risk, dist)
                elif P['slm'] == 'tighter': risk = min(risk, dist)
                if not (0.4 * s['atr4'] <= risk <= 3 * s['atr4']): i += 1; continue
        # 1H bars of the next 4H candle (the order's life); retest / pullback modes get one more 4H candle
        k = i1.get(s['tc'])
        if k is None: i += 1; continue
        life = 4 if P['entry'] in ('C', 'C1c') else 8
        ent = None; broke = False; pb = None
        for j in range(k, min(len(h1), k + life)):
            b = h1[j]
            if b['wk'] != s['wk']: break
            hr = b['t'].astimezone(BUC).hour
            okh = P['hours'] is None or (P['hours'][0] <= hr < P['hours'][1])
            hit = (b['h'] >= lvl) if dr > 0 else (b['l'] <= lvl)
            if P['entry'] == 'C':
                if hit and okh: ent = (j, max(lvl, b['o']) if dr > 0 else min(lvl, b['o']), True); break
            elif P['entry'] == 'C1c':       # a 1H candle closes beyond the level: enter at that close
                if okh and (b['c'] - lvl) * dr > 0: ent = (j, b['c'], False); break
            elif P['entry'] == 'Cret':      # break first, then a limit back at the broken level
                if broke and okh and ((b['l'] <= lvl) if dr > 0 else (b['h'] >= lvl)): ent = (j, lvl, True); break
                if hit: broke = True
            elif P['entry'] == 'C1pb':      # after the break, a 1H candle against the trade, then a stop beyond it
                if pb is not None and okh and ((b['h'] >= pb) if dr > 0 else (b['l'] <= pb)): ent = (j, pb, True); break
                if broke and (b['c'] - b['o']) * dr < 0: pb = b['h'] if dr > 0 else b['l']
                if hit: broke = True
        if ent is None: i += 1; continue
        j, e, intrabar = ent; sl = e - dr * risk; tpl = e + dr * P['tp'] * risk if P['tp'] else None
        best = 0.0; exitp = None; why = None
        # worst case on the fill candle: stop touched after an intrabar fill
        b = h1[j]
        if intrabar and ((b['l'] <= sl) if dr > 0 else (b['h'] >= sl)): exitp, why, jx = sl, 'SL same bar', j
        jj = j + (0 if exitp is not None else 1) if not intrabar else j + 1
        if exitp is None and not intrabar: jj = j + 1
        while exitp is None and jj < len(h1):
            b = h1[jj]
            if (b['l'] <= sl) if dr > 0 else (b['h'] >= sl):
                g = (b['o'] < sl) if dr > 0 else (b['o'] > sl); exitp, why = (b['o'] if g else sl), 'SL'; jx = jj; break
            if tpl is not None and ((b['h'] >= tpl) if dr > 0 else (b['l'] <= tpl)): exitp, why, jx = tpl, 'TP', jj; break
            best = max(best, ((b['h'] if dr > 0 else b['l']) - e) * dr / risk)
            if P['sttf'] == '1h' and P['trm'] != 'atr' and (P['trm'] != 'st_after' or best >= P['stat']):
                ln1 = _u1[jj] if dr > 0 else _d1[jj]
                if ln1 is not None and _t1[jj] == dr: sl = max(sl, ln1) if dr > 0 else min(sl, ln1)
            # 4H close: trailing and direction flip
            while k4 < len(b4) and b4[k4]['tc'] < b['tc']: k4 += 1
            if k4 < len(b4) and b4[k4]['tc'] == b['tc']:
                c4 = b4[k4]; A = c4['atr4']
                kk = P['trk2'] if P['trk2'] and best >= P['trat'] else P['trk']
                ns = c4['c'] - dr * kk * A
                if P['trm'] != 'atr' and P['sttf'] == '4h':
                    u_, d_ = stl.get(c4['tc'], (None, None)); ln = u_ if dr > 0 else d_
                    if ln is None: ln = sl
                    if P['trm'] == 'st': ns = ln
                    elif P['trm'] == 'tighter': ns = max(ns, ln) if dr > 0 else min(ns, ln)
                    elif P['trm'] == 'st_after' and best >= P['stat']: ns = ln
                if P['trm'] == 'st' and P['sttf'] == '1h': ns = sl
                sl = max(sl, ns) if dr > 0 else min(sl, ns)
                d2, _ = dir_at(c4)
                if P['xx'] and _XX[ix4[c4['tc']]] == -dr: exitp, why, jx = b['c'], 'X', jj; break
                if P['tvx']:
                    q = ix4[c4['tc']]
                    if P['tvx'] == 'flip' and _T['act'][q] == -dr: exitp, why, jx = b['c'], 'TVP', jj; break
                    if P['tvx'] in ('band', 'band_1R') and (P['tvx'] == 'band' or best >= 1):
                        ln = _T['lo'][q] if dr > 0 else _T['up'][q]
                        if ln == ln: sl = max(sl, ln) if dr > 0 else min(sl, ln)
                if P['mcx']:
                    q = ix4[c4['tc']]; h_, h1_, h2_ = _hs[q], _hs[q - 1], _hs[q - 2]
                    xx = {'cross': h_ * dr < 0, 'cross_1R': best >= 1 and h_ * dr < 0, 'cross_2R': best >= 2 and h_ * dr < 0,
                          'fade2_1R': best >= 1 and (h_ - h1_) * dr < 0 and (h1_ - h2_) * dr < 0}[P['mcx']]
                    if xx: exitp, why, jx = b['c'], 'MACD', jj; break
                if P['sqx']:
                    q = ix4[c4['tc']]; v_, v1_, v2_ = _v[q], _v[q - 1], _v[q - 2]
                    xx = {'fade2': (v_ - v1_) * dr < 0 and (v1_ - v2_) * dr < 0, 'zero': v_ * dr < 0,
                          'fade_2R': best >= 2 and (v_ - v1_) * dr < 0, 'fade2_1R': best >= 1 and (v_ - v1_) * dr < 0 and (v1_ - v2_) * dr < 0}[P['sqx']]
                    if xx: exitp, why, jx = b['c'], 'SQZ', jj; break
                if d2 == -dr: exitp, why, jx = b['c'], 'Flip', jj; break
            if P['fri'] and b['dow'] == 4 and b['last_of_day']: exitp, why, jx = b['c'], 'Fri', jj; break
            jj += 1
        if exitp is None: break
        R = (exitp - e) * dr / risk - cost / risk
        res.append(dict(pair=p, t=h1[j]['t'], tx=h1[jx]['tc'], d=dr, R=R, why=why, wk=s['wk'], hr=h1[j]['t'].astimezone(BUC).hour, gap=bi[2]))
        lastx = h1[jx]['tc']
        while i < len(b4) and b4[i]['tc'] <= lastx: i += 1
    return res

if __name__ == '__main__':
    PAIRS = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'USDCAD', 'AUDUSD', 'NZDUSD', 'XAUUSD']
    B = bias_table(); D4 = {p: prep4(p) for p in PAIRS}; D1 = {p: load1h(p) for p in PAIRS}
    def ev(P):
        hs = [sum([run_c(p, D4[p], D1[p], B, P, a, c) for p in PAIRS], []) for a, c in H]
        allt = sorted(hs[0] + hs[1], key=lambda x: x['tx']); eq = pk = dd = 0; wk = collections.defaultdict(float)
        for x in allt: eq += x['R']; pk = max(pk, eq); dd = min(dd, eq - pk); wk[x['wk'][1]] += x['R']
        w = [wk.get(q, 0) for q in range(40, 48)]
        return dict(n=len(allt), h1=sum(x['R'] for x in hs[0]), h2=sum(x['R'] for x in hs[1]), dd=dd, b2=[w[q] + w[q + 1] for q in range(0, 8, 2)],
                    win=sum(x['R'] > 0 for x in allt) / max(1, len(allt)), avg=St.mean([x['R'] for x in allt]) if allt else 0, t=allt)
    base = None
    for n, P in [('C on 1H path, all hours (tighten 0.5 after 2R, TP 4R)', {}),
                 ('  hours 06-22', dict(hours=(6, 22))),
                 ('  hours 06-22, TP 3R, no tighten (old settings)', dict(hours=(6, 22), tp=3, trk2=None)),
                 ('--- 1H entries, hours 06-22', None),
                 ('  1H close beyond the 4H level', dict(entry='C1c', hours=(6, 22))),
                 ('  break, then retest of the level (limit)', dict(entry='Cret', hours=(6, 22))),
                 ('  break, 1H pullback candle, then its break', dict(entry='C1pb', hours=(6, 22))),
                 ('  C + signal candle in direction', dict(sc='dir', hours=(6, 22))),
                 ('  C + 4H close beyond 4H EMA20', dict(sc='ema', hours=(6, 22))),
                 ('  retest + signal candle in direction', dict(entry='Cret', sc='dir', hours=(6, 22)))]:
        if P is None: print(n); continue
        r = ev(P); base = base or r
        flag = '  ✓ both halves better' if (r['h1'] > base['h1'] and r['h2'] > base['h2'] and r is not base) else ''
        print(f"{n:<55} {r['n']:3}tr win {r['win']:.0%} avg {r['avg']:+.2f}  {r['h1']:+5.1f}/{r['h2']:+5.1f} = {r['h1'] + r['h2']:+5.1f}R  dd {r['dd']:+.1f}  2wk[{', '.join(f'{v:+.1f}' for v in r['b2'])}]{flag}")
    t = ev(dict(hours=(6, 22)))['t']
    print('entry hours (06-22, C):', sorted(collections.Counter(x['hr'] for x in t).items()))
