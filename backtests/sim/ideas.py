# Out-of-the-box session / structure ideas, all taken only in the week's bias direction (1H chart, Bucharest hours).
#  asia_bo     Asia range (02:00-09:00) -> stop entry at the Asia high (long) after 09:00, until 15:00
#  asia_judas  London (09-13) trades below the Asia low (long) and a candle closes back inside -> enter at that close
#  ny_rev      after 15:00, price takes the London (09-15) low (long) and closes back above it -> enter
#  sd_zone     fractal demand: a 2/2 pivot low followed within 3 bars by a 1.5 ATR displacement; first return to the
#              pivot candle's body top = limit entry, stop below the pivot low
#  nr_day      yesterday was the narrowest of the last 4 days (NR4) -> stop entry at yesterday's high (long), today
#  adr_pb      today has already moved >= 50% of the 10-day ADR against the bias, then a 1H candle closes back in the
#              bias direction beyond the previous candle -> enter at the close
#  round       price trades through a 00/50 round number against the bias and a candle closes back beyond it -> enter
import sys, os, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smc import B, cost_of, pip_of, pip_of as _pip

def _days(b):
    D = collections.OrderedDict()
    for i, x in enumerate(b): D.setdefault(x['day'], []).append(i)
    return D

DEF = dict(idea='asia_bo', sl='struct', slk=1.0, tpR=3, maxR=3.0, minR=0.3, life=6, bias=True, hours=None)
def run(p, b, P, start, end):
    P = {**DEF, **P}; cost = cost_of(p) * pip_of(p); I = P['idea']
    days = _days(b); dkeys = list(days); dix = {d: k for k, d in enumerate(dkeys)}
    dh = {d: max(b[j]['h'] for j in v) for d, v in days.items()}; dl = {d: min(b[j]['l'] for j in v) for d, v in days.items()}
    adr = {}
    for k, d in enumerate(dkeys):
        if k >= 10: adr[d] = np.mean([dh[q] - dl[q] for q in dkeys[k - 10:k]])
    res = []; pos = None; pend = None; done = set()
    asia = {}; lon = {}; dlow = {}; dhigh = {}; dopen = {}
    piv = []   # pending S/D zones: [dir, top, bottom, pivot index, armed]
    step = 50 * _pip(p) if 'JPY' not in p and 'XAU' not in p else (0.5 if 'JPY' in p else 5.0)
    for i in range(3, len(b)):
        x = b[i]; A = x['atr']; d0 = x['day']; hr = x['hr']
        # session ranges (built from completed bars only)
        dopen.setdefault(d0, x['o'])
        dlow[d0] = min(dlow.get(d0, x['l']), x['l']); dhigh[d0] = max(dhigh.get(d0, x['h']), x['h'])
        # ---- manage position
        if pos:
            d = pos['d']; px = None
            if (x['l'] <= pos['sl']) if d > 0 else (x['h'] >= pos['sl']): px = min(x['o'], pos['sl']) if d > 0 else max(x['o'], pos['sl'])
            elif (x['h'] >= pos['tp']) if d > 0 else (x['l'] <= pos['tp']): px = max(x['o'], pos['tp']) if d > 0 else min(x['o'], pos['tp'])
            if px is not None:
                res.append(dict(p=p, d=d, t=pos['t'], tx=x['tc'], wk=pos['wk'], R=d * (px - pos['e']) / pos['r'] - cost / pos['r'])); pos = None
        # ---- pending order
        if pend and not pos:
            d = pend['d']
            if i > pend['until']: pend = None
            else:
                hit = (x['h'] >= pend['e']) if (d > 0) == (pend['kind'] == 'stop') else (x['l'] <= pend['e'])
                if hit:
                    if pend['kind'] == 'stop': e = max(x['o'], pend['e']) if d > 0 else min(x['o'], pend['e'])
                    else: e = min(x['o'], pend['e']) if d > 0 else max(x['o'], pend['e'])
                    r = abs(e - pend['sl'])
                    pos = dict(d=d, e=e, r=r, sl=pend['sl'], tp=e + d * P['tpR'] * r, t=x['t'], wk=x['wk']); pend = None
                    if (x['l'] <= pos['sl']) if d > 0 else (x['h'] >= pos['sl']):   # worst case on the fill bar
                        res.append(dict(p=p, d=d, t=x['t'], tx=x['tc'], wk=x['wk'], R=-1 - cost / r)); pos = None
        # S/D zones: register (needs bars i-4..i), regardless of the window
        if I == 'sd_zone' and A:
            k = i - 3   # pivot candidate at k with 2 bars each side, displacement within the 3 bars after it
            if k >= 2:
                for s in (1, -1):
                    lo_ = (b[k]['l'] < min(b[k - 1]['l'], b[k - 2]['l'], b[k + 1]['l'], b[k + 2]['l'])) if s > 0 else (b[k]['h'] > max(b[k - 1]['h'], b[k - 2]['h'], b[k + 1]['h'], b[k + 2]['h']))
                    if not lo_: continue
                    ext = max(b[j]['h'] for j in range(k + 1, i + 1)) - b[k]['h'] if s > 0 else b[k]['l'] - min(b[j]['l'] for j in range(k + 1, i + 1))
                    if ext >= 1.5 * A:
                        top = max(b[k]['o'], b[k]['c']) if s > 0 else min(b[k]['o'], b[k]['c'])
                        bot = b[k]['l'] if s > 0 else b[k]['h']
                        piv.append([s, top, bot, i, True])
                piv[:] = [z for z in piv if i - z[3] <= 72][-20:]
        bi_ = B.get((p, x['wk']), ('-',))[0]; bd = 1 if bi_ == 'U' else -1 if bi_ == 'D' else 0
        if pos or pend or A is None or not (start <= x['t'] < end) or bd == 0 or (P['bias'] is False): 
            # ranges still need updating
            if 2 <= hr < 9: a_ = asia.setdefault(d0, [x['h'], x['l']]); a_[0] = max(a_[0], x['h']); a_[1] = min(a_[1], x['l'])
            if 9 <= hr < 15: l_ = lon.setdefault(d0, [x['h'], x['l']]); l_[0] = max(l_[0], x['h']); l_[1] = min(l_[1], x['l'])
            continue
        d = bd; key = (d0, I)
        if I == 'asia_bo' and 9 <= hr < 15 and key not in done and d0 in asia:
            ah, al = asia[d0]; lvl = ah if d > 0 else al; sl = (ah + al) / 2 if P['sl'] == 'mid' else (al if d > 0 else ah)
            r = abs(lvl - sl)
            if P['minR'] * A <= r <= P['maxR'] * A and (x['c'] - lvl) * d < 0:
                pend = dict(d=d, e=lvl, sl=sl, kind='stop', until=i + 1); done.add(key)   # order live for the next candle, re-armed each hour
                done.discard(key) if hr < 14 else None
        elif I == 'asia_judas' and 9 <= hr < 13 and key not in done and d0 in asia:
            ah, al = asia[d0]
            if d > 0 and dlow[d0] < al and x['c'] > al and x['c'] > x['o']:
                sl = dlow[d0] - 0.1 * A; r = x['c'] - sl
                if P['minR'] * A <= r <= P['maxR'] * A: pos = dict(d=d, e=x['c'], r=r, sl=sl, tp=x['c'] + P['tpR'] * r, t=x['t'], wk=x['wk']); done.add(key)
            elif d < 0 and dhigh[d0] > ah and x['c'] < ah and x['c'] < x['o']:
                sl = dhigh[d0] + 0.1 * A; r = sl - x['c']
                if P['minR'] * A <= r <= P['maxR'] * A: pos = dict(d=d, e=x['c'], r=r, sl=sl, tp=x['c'] - P['tpR'] * r, t=x['t'], wk=x['wk']); done.add(key)
        elif I == 'ny_rev' and 15 <= hr < 21 and key not in done and d0 in lon:
            lh, ll = lon[d0]
            if d > 0 and x['l'] < ll and x['c'] > ll:
                sl = x['l'] - 0.1 * A; r = x['c'] - sl
                if P['minR'] * A <= r <= P['maxR'] * A: pos = dict(d=d, e=x['c'], r=r, sl=sl, tp=x['c'] + P['tpR'] * r, t=x['t'], wk=x['wk']); done.add(key)
            elif d < 0 and x['h'] > lh and x['c'] < lh:
                sl = x['h'] + 0.1 * A; r = sl - x['c']
                if P['minR'] * A <= r <= P['maxR'] * A: pos = dict(d=d, e=x['c'], r=r, sl=sl, tp=x['c'] - P['tpR'] * r, t=x['t'], wk=x['wk']); done.add(key)
        elif I == 'sd_zone':
            for z in reversed(piv):
                if z[0] != d or not z[4] or z[3] >= i: continue
                if (x['l'] <= z[1]) if d > 0 else (x['h'] >= z[1]):
                    z[4] = False
                    sl = z[2] - d * 0.1 * A; e = z[1]; r = abs(e - sl)
                    if P['minR'] * A <= r <= P['maxR'] * A:
                        # touched this bar: treat as a limit filled at the zone edge (worst case: stop checked from the next bar)
                        e = min(x['o'], e) if d > 0 else max(x['o'], e)
                        if (x['l'] <= sl) if d > 0 else (x['h'] >= sl): res.append(dict(p=p, d=d, t=x['t'], tx=x['tc'], wk=x['wk'], R=-1 - cost / abs(e - sl)))
                        else: pos = dict(d=d, e=e, r=abs(e - sl), sl=sl, tp=e + d * P['tpR'] * abs(e - sl), t=x['t'], wk=x['wk'])
                    break
        elif I == 'nr_day' and key not in done and 9 <= hr < 21:
            k = dix[d0]
            if k >= 4:
                y = dkeys[k - 1]; rngs = [dh[q] - dl[q] for q in dkeys[k - 4:k]]
                if rngs[-1] == min(rngs):
                    lvl = dh[y] if d > 0 else dl[y]; sl = dl[y] if d > 0 else dh[y]; r = abs(lvl - sl)
                    if P['minR'] * A <= r <= 3 * P['maxR'] * A and (x['c'] - lvl) * d < 0:
                        pend = dict(d=d, e=lvl, sl=sl, kind='stop', until=i + 1)
                done.add(key) if hr >= 20 else None
        elif I == 'adr_pb' and key not in done and d0 in adr:
            move = (dopen[d0] - dlow[d0]) if d > 0 else (dhigh[d0] - dopen[d0])
            if move >= 0.5 * adr[d0] and (x['c'] - b[i - 1]['h'] if d > 0 else b[i - 1]['l'] - x['c']) > 0:
                sl = (dlow[d0] if d > 0 else dhigh[d0]) - d * 0.1 * A; r = abs(x['c'] - sl)
                if P['minR'] * A <= r <= P['maxR'] * A: pos = dict(d=d, e=x['c'], r=r, sl=sl, tp=x['c'] + d * P['tpR'] * r, t=x['t'], wk=x['wk']); done.add(key)
        elif I == 'round':
            lv = (np.floor(x['c'] / step) * step) if d > 0 else (np.ceil(x['c'] / step) * step)
            if (d > 0 and x['l'] < lv < x['c'] and b[i - 1]['c'] > lv) or (d < 0 and x['h'] > lv > x['c'] and b[i - 1]['c'] < lv):
                sl = (x['l'] if d > 0 else x['h']) - d * 0.1 * A; r = abs(x['c'] - sl)
                if P['minR'] * A <= r <= P['maxR'] * A: pos = dict(d=d, e=x['c'], r=r, sl=sl, tp=x['c'] + d * P['tpR'] * r, t=x['t'], wk=x['wk'])
        if 2 <= hr < 9: a_ = asia.setdefault(d0, [x['h'], x['l']]); a_[0] = max(a_[0], x['h']); a_[1] = min(a_[1], x['l'])
        if 9 <= hr < 15: l_ = lon.setdefault(d0, [x['h'], x['l']]); l_[0] = max(l_[0], x['h']); l_[1] = min(l_[1], x['l'])
    return res

if __name__ == '__main__':
    from harness import go_bias
    print('baseline: random entry in bias direction, SL 1.5 ATR TP 3R = +0.19R/tr; MACD cross +0.45; BE Swing USD +0.68')
    for I, lab in [('asia_bo', 'Asia range breakout (London)'), ('asia_judas', 'Asia sweep in London, back inside (Judas)'),
                   ('ny_rev', 'NY takes London low/high, back inside'), ('sd_zone', 'fractal S/D zone, first retest'),
                   ('nr_day', 'NR4 day breakout'), ('adr_pb', 'half-ADR pullback against bias, turn'), ('round', 'round-number reclaim')]:
        print('==', lab)
        for xn, xp in [('TP 2R', dict(tpR=2)), ('TP 3R', dict(tpR=3)), ('TP 4R', dict(tpR=4))] + ([('SL Asia mid, TP 3R', dict(sl='mid'))] if I == 'asia_bo' else []):
            print(f"  {xn:<20} {go_bias(run, {'idea': I, **xp}, hours=None)}", flush=True)
