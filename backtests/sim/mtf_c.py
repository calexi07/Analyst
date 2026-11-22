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

DEF = dict(trm='atr', stp=10, stm=3.0, stat=1.0, entry='C', tp=4, trk=0.75, trk2=0.5, trat=2.0, hours=None, cool=24, dirm='both', maxdow=2, sc=None, fri=True)

def run_c(p, b4, h1, B, P, start, end):
    P = {**DEF, **P}; cost = cost_of(p) * pip_of(p)
    i1 = {b['t']: k for k, b in enumerate(h1)}
    res, lastx, k4 = [], None, 0
    if P['trm'] != 'atr':
        import st as _st
        _up, _dn, _tr, _ = _st.supertrend(b4, P['stp'], P['stm']); stl = {b4[q]['tc']: (_up[q], _dn[q]) for q in range(len(b4))}
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
        lvl = s['h'] if dr > 0 else s['l']; risk = s['atr4']
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
            # 4H close: trailing and direction flip
            while k4 < len(b4) and b4[k4]['tc'] < b['tc']: k4 += 1
            if k4 < len(b4) and b4[k4]['tc'] == b['tc']:
                c4 = b4[k4]; A = c4['atr4']
                kk = P['trk2'] if P['trk2'] and best >= P['trat'] else P['trk']
                ns = c4['c'] - dr * kk * A
                if P['trm'] != 'atr':
                    u_, d_ = stl.get(c4['tc'], (None, None)); ln = u_ if dr > 0 else d_
                    if ln is None: ln = sl
                    if P['trm'] == 'st': ns = ln
                    elif P['trm'] == 'tighter': ns = max(ns, ln) if dr > 0 else min(ns, ln)
                    elif P['trm'] == 'st_after' and best >= P['stat']: ns = ln
                sl = max(sl, ns) if dr > 0 else min(sl, ns)
                d2, _ = dir_at(c4)
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
