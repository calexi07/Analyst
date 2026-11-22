# BE Swing on any signal timeframe: entry C (stop beyond the signal candle's high/low), bias + daily SMA20 agree,
# stop = k x signal-TF ATR, trailing from the signal close (tightened after +R), TP, direction-flip and Friday exits.
# Signals from completed signal candles; fills, stops and targets on a finer path (or the signal bars themselves).
import sys, os, datetime as D, collections, bisect
from zoneinfo import ZoneInfo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smc import cost_of, pip_of
BUC = ZoneInfo('Europe/Bucharest'); NY = ZoneInfo('America/New_York')
DEF = dict(entry='C', slk=1.5, tp=4, trk=1.0, trk2=None, trat=2.0, cool=12, maxdow=2, hours=(6, 22), dirm='both', life=1, flip=True, fri=True, sma=20)

def daily_sma(bars, n=20):
    # SMA of the previous n completed NY-17:00 days, keyed by trading day
    closes = collections.OrderedDict()
    for b in bars:
        d = (b['t'] + D.timedelta(hours=7)).astimezone(NY).date(); closes[d] = b['c']
    ks = list(closes); out = {}
    for i, k in enumerate(ks):
        out[k] = sum(closes[x] for x in ks[i - n:i]) / n if i >= n else None
    return out

def prep(bars):
    sm = daily_sma(bars)
    for b in bars:
        d = (b['t'] + D.timedelta(hours=7)).astimezone(NY).date()
        b['nyd'] = d; b['sma20'] = sm.get(d); b['nydow'] = d.weekday()
    for i, b in enumerate(bars):
        b['lastday'] = i + 1 >= len(bars) or bars[i + 1]['nyd'] != b['nyd']
    return bars

def run(p, sig, path, B, P, start, end):
    P = {**DEF, **P}; cost = cost_of(p) * pip_of(p)
    pt = [b['t'] for b in path]; res = []; lastx = None; i = 0
    sigtc = {b['tc']: k for k, b in enumerate(sig)}
    def dir_at(b):
        bi = B.get((p, b['wk']), ('-', '-', None)); bd = 1 if bi[0] == 'U' else -1 if bi[0] == 'D' else 0
        if P['dirm'] == 'bias': return bd
        td = 0 if b['sma20'] is None else (1 if b['c'] > b['sma20'] else -1)
        return bd if bd == td else 0
    dur = sig[1]['tc'] - sig[1]['t']
    while i < len(sig) - 1:
        s = sig[i]
        if s['t'] < start or s['t'] >= end or not s['atr']: i += 1; continue
        if lastx and (s['tc'] - lastx).total_seconds() < P['cool'] * 3600: i += 1; continue
        dr = dir_at(s)
        if dr == 0 or s['nydow'] > P['maxdow']: i += 1; continue
        risk = P['slk'] * s['atr']; lvl = s['h'] if dr > 0 else s['l']
        j0 = bisect.bisect_left(pt, s['tc']); jend = bisect.bisect_left(pt, s['tc'] + dur * P['life'])
        ent = None
        if P['entry'] == 'A':
            if j0 < len(path):
                hr = path[j0]['t'].astimezone(BUC).hour
                if P['hours'] is None or P['hours'][0] <= hr < P['hours'][1]: ent = (j0, s['c'], False)
        else:
            for j in range(j0, min(jend, len(path))):
                b = path[j]
                if b['wk'] != s['wk']: break
                hr = b['t'].astimezone(BUC).hour
                if P['hours'] is not None and not (P['hours'][0] <= hr < P['hours'][1]): continue
                if (b['h'] >= lvl) if dr > 0 else (b['l'] <= lvl): ent = (j, max(lvl, b['o']) if dr > 0 else min(lvl, b['o']), True); break
        if ent is None: i += 1; continue
        j, e, intrabar = ent; sl = e - dr * risk; tpl = e + dr * P['tp'] * risk if P['tp'] else None
        best = 0.0; exitp = None; jx = j
        b = path[j]
        if intrabar and ((b['l'] <= sl) if dr > 0 else (b['h'] >= sl)): exitp, why = sl, 'SL'
        jj = j + 1 if intrabar else j
        while exitp is None and jj < len(path):
            b = path[jj]
            if (b['l'] <= sl) if dr > 0 else (b['h'] >= sl):
                g = (b['o'] < sl) if dr > 0 else (b['o'] > sl); exitp, why, jx = (b['o'] if g else sl), 'SL', jj; break
            if tpl is not None and ((b['h'] >= tpl) if dr > 0 else (b['l'] <= tpl)): exitp, why, jx = tpl, 'TP', jj; break
            best = max(best, ((b['h'] if dr > 0 else b['l']) - e) * dr / risk)
            q = sigtc.get(b['tc'])
            if q is not None:                      # a signal candle closed: trailing and flip
                c = sig[q]
                if P['trk']:
                    kk = P['trk2'] if P['trk2'] and best >= P['trat'] else P['trk']
                    ns = c['c'] - dr * kk * c['atr']; sl = max(sl, ns) if dr > 0 else min(sl, ns)
                if P['flip'] and dir_at(c) == -dr: exitp, why, jx = b['c'], 'Flip', jj; break
            if P['fri'] and b['nydow'] == 4 and b['lastday']: exitp, why, jx = b['c'], 'Fri', jj; break
            jj += 1
        if exitp is None: break
        R = (exitp - e) * dr / risk - cost / risk
        res.append(dict(pair=p, t=path[j]['t'], tx=path[jx]['tc'], d=dr, R=R, why=why, wk=s['wk']))
        lastx = path[jx]['tc']
        while i < len(sig) and sig[i]['tc'] <= lastx: i += 1
    return res
