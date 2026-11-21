# The user's LuxAlgo "ICT Concepts" logic rebuilt in Python (MSS/BOS from its zigzag, displacement FVGs, order blocks from
# its swings(), equal-high/low liquidity clusters, killzones) and turned into entries in the engine's bias direction.
# 1H path; limit fills count the stop if it is touched on the fill candle. Indicator: LuxAlgo, CC BY-NC-SA 4.0 (personal research).
import sys, os, datetime as D, statistics as St, collections
from zoneinfo import ZoneInfo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smc import prep, B, H, PRE, USDP, EURP, U, cost_of, pip_of
LON, NYZ = ZoneInfo('Europe/London'), ZoneInfo('America/New_York')

def features(b, mlen=5, oblen=10, margin=2.5):
    n = len(b); a10 = None
    for i, x in enumerate(b):
        tr = x['h'] - x['l'] if i == 0 else max(x['h'], b[i - 1]['c']) - min(x['l'], b[i - 1]['c'])
        a10 = tr if a10 is None else (a10 * 9 + tr) / 10; x['a10'] = a10
        lt = x['t'].astimezone(LON); nt = x['t'].astimezone(NYZ)
        x['kz'] = 'LO' if 7 <= lt.hour < 10 else 'NY' if 7 <= nt.hour < 9 else None
        x['body'] = abs(x['c'] - x['o'])
    zz = []                      # zigzag points [d, x, y]
    mdir = 0; lastB = {1: None, -1: None}
    os_ = 0; top = None; btm = None; tcross = True; bcross = True
    bliq, sliq = [], []          # liquidity levels (price)
    for i, x in enumerate(b):
        x['mss'] = 0; x['bos'] = 0; x['fvg'] = None; x['ob'] = None; x['sweep'] = 0
        # zigzag pivots: left mlen, right 1 (confirmed on this bar for bar i-1)
        if i > mlen:
            k = i - 1; pk = b[k]
            if pk['h'] > max(y['h'] for y in b[k - mlen:k]) and pk['h'] >= x['h']:
                if not zz or zz[0][0] < 1: zz.insert(0, [1, k, pk['h']])
                elif pk['h'] > zz[0][2]: zz[0][1:] = [k, pk['h']]
                cl = [p[2] for p in zz[:50] if p[0] == 1 and abs(p[2] - pk['h']) < x['a10'] / margin]
                if len(cl) > 2: bliq.append(sum(cl) / len(cl))
            if pk['l'] < min(y['l'] for y in b[k - mlen:k]) and pk['l'] <= x['l']:
                if not zz or zz[0][0] > -1: zz.insert(0, [-1, k, pk['l']])
                elif pk['l'] < zz[0][2]: zz[0][1:] = [k, pk['l']]
                cl = [p[2] for p in zz[:50] if p[0] == -1 and abs(p[2] - pk['l']) < x['a10'] / margin]
                if len(cl) > 2: sliq.append(sum(cl) / len(cl))
        if len(zz) >= 3:
            iH = 2 if zz[2][0] == 1 else 1; iL = 2 if zz[2][0] == -1 else 1
            if x['c'] > zz[iH][2] and zz[iH][0] == 1 and mdir < 1: mdir = 1; x['mss'] = 1; lastB[1] = zz[iH][2]
            elif x['c'] < zz[iL][2] and zz[iL][0] == -1 and mdir > -1: mdir = -1; x['mss'] = -1; lastB[-1] = zz[iL][2]
            elif mdir == 1 and x['c'] > zz[iH][2] and lastB[1] != zz[iH][2]: x['bos'] = 1; lastB[1] = zz[iH][2]
            elif mdir == -1 and x['c'] < zz[iL][2] and lastB[-1] != zz[iL][2]: x['bos'] = -1; lastB[-1] = zz[iL][2]
        x['mdir'] = mdir; x['zzlo'] = next((p[2] for p in zz if p[0] == -1), None); x['zzhi'] = next((p[2] for p in zz if p[0] == 1), None)
        # displacement FVG (LuxAlgo: previous candle a big full-bodied candle, gap between candle 3 and candle 1)
        if i >= 6:
            pb = b[i - 1]; mb = St.mean(y['body'] for y in b[i - 6:i - 1])
            full = (pb['h'] - max(pb['c'], pb['o']) < pb['body'] * 0.36) and (min(pb['c'], pb['o']) - pb['l'] < pb['body'] * 0.36) and pb['body'] > mb
            if full and pb['c'] > pb['o'] and x['l'] > b[i - 2]['h']: x['fvg'] = (1, x['l'], b[i - 2]['h'])
            if full and pb['c'] < pb['o'] and x['h'] < b[i - 2]['l']: x['fvg'] = (-1, b[i - 2]['l'], x['h'])
        # order blocks from swings(oblen)
        if i > oblen:
            up = max(y['h'] for y in b[i - oblen + 1:i + 1]); lo = min(y['l'] for y in b[i - oblen + 1:i + 1])
            prev = os_; hl = b[i - oblen]
            os_ = 0 if hl['h'] > up else 1 if hl['l'] < lo else os_
            if os_ == 0 and prev != 0: top = (hl['h'], i - oblen); tcross = False
            if os_ == 1 and prev != 1: btm = (hl['l'], i - oblen); bcross = False
            if top and not tcross and x['c'] > top[0]:
                tcross = True; seg = b[top[1] + 1:i] or [b[i - 1]]
                j = min(range(len(seg)), key=lambda q: min(seg[q]['c'], seg[q]['o']))
                x['ob'] = (1, max(seg[j]['c'], seg[j]['o']), min(seg[j]['c'], seg[j]['o']))
            if btm and not bcross and x['c'] < btm[0]:
                bcross = True; seg = b[btm[1] + 1:i] or [b[i - 1]]
                j = max(range(len(seg)), key=lambda q: max(seg[q]['c'], seg[q]['o']))
                x['ob'] = (-1, max(seg[j]['c'], seg[j]['o']), min(seg[j]['c'], seg[j]['o']))
        # liquidity sweeps (a level is used once)
        for L_, s in ((sliq, 1), (bliq, -1)):
            for lv in list(L_[-5:]):
                if (x['l'] < lv < x['c']) if s > 0 else (x['h'] > lv > x['c']): x['sweep'] = s; L_.remove(lv)
                elif (x['c'] < lv) if s > 0 else (x['c'] > lv): L_.remove(lv)
    return b

DEF = dict(entry='mss', exit='tp3', kz=False, hours=(6, 22), fri=True, cool=12, maxdow=3, align=True, life=24, buf=0.1, dirm='bias')

def run(p, b, P, start, end):
    P = {**DEF, **P}; cost = cost_of(p) * pip_of(p)
    res, pos, pend, lastx, swept = [], None, None, None, None
    mss_i = {1: -999, -1: -999}
    for i, x in enumerate(b):
        if x['atr'] is None: continue
        if x['mss']: mss_i[x['mss']] = i
        if x['sweep']: swept = (x['sweep'], i, x['l'] if x['sweep'] > 0 else x['h'])
        if pos:
            d = pos['d']
            if (x['l'] <= pos['sl']) if d > 0 else (x['h'] >= pos['sl']):
                g = (x['o'] < pos['sl']) if d > 0 else (x['o'] > pos['sl']); ex = (x['o'] if g else pos['sl'], 'SL')
            elif pos['tp'] and ((x['h'] >= pos['tp']) if d > 0 else (x['l'] <= pos['tp'])): ex = (pos['tp'], 'TP')
            elif P['exit'] == 'mss' and x['mss'] == -d: ex = (x['c'], 'MSS')
            elif P['fri'] and x['dow'] == 4 and x['last_of_day']: ex = (x['c'], 'Fri')
            else: ex = None
            if ex:
                res.append(dict(p=p, t=pos['t'], tx=x['tc'], R=(ex[0] - pos['e']) * d / pos['r'] - cost / pos['r'], why=ex[1], wk=pos['wk'])); pos = None; lastx = x['tc']
            continue
        if not (start <= x['t'] < end): pend = None; continue
        bi = B.get((p, x['wk']), ('-', '-', None)); d = 1 if bi[0] == 'U' else -1 if bi[0] == 'D' else 0
        if P['dirm'] == 'trend': d = x['td']
        ok = d != 0 and x['dow'] <= P['maxdow'] and P['hours'][0] <= x['hr'] < P['hours'][1] and (not P['kz'] or x['kz']) and not (lastx and (x['tc'] - lastx).total_seconds() < P['cool'] * 3600)
        if pend:
            if i > pend['until'] or pend['d'] != d: pend = None
            elif ok and ((x['l'] <= pend['e']) if pend['d'] > 0 else (x['h'] >= pend['e'])):
                e = min(pend['e'], x['o']) if pend['d'] > 0 else max(pend['e'], x['o']); r = abs(e - pend['sl'])
                if r > 0:
                    pos = dict(t=x['t'], wk=x['wk'], d=pend['d'], e=e, sl=pend['sl'], r=r, tp=tpfor(P, pend['d'], e, r, x)); pend = None
                    if (x['l'] <= pos['sl']) if pos['d'] > 0 else (x['h'] >= pos['sl']):
                        res.append(dict(p=p, t=x['t'], tx=x['tc'], R=-1 - cost / r, why='SL same bar', wk=pos['wk'])); pos = None; lastx = x['tc']
                    continue
        if not ok: continue
        A = x['atr']; al = not P['align'] or x['mdir'] == d; E = P['entry']; mkt = None
        if E == 'mss' and x['mss'] == d and x['zzlo' if d > 0 else 'zzhi'] is not None:
            mkt = x['zzlo' if d > 0 else 'zzhi'] - d * P['buf'] * A
        elif E == 'bos' and x['bos'] == d and x['zzlo' if d > 0 else 'zzhi'] is not None:
            mkt = x['zzlo' if d > 0 else 'zzhi'] - d * P['buf'] * A
        elif E == 'sweep_mss' and x['mss'] == d and swept and swept[0] == d and i - swept[1] <= P['life']:
            mkt = swept[2] - d * P['buf'] * A; swept = None
        elif E == 'sweep_any' and x['sweep'] == d and al:
            mkt = (x['l'] if d > 0 else x['h']) - d * P['buf'] * A
        elif E in ('fvg', 'mss_fvg') and x['fvg'] and x['fvg'][0] == d and al and (E == 'fvg' or i - mss_i[d] <= P['life']):
            top, bot = x['fvg'][1], x['fvg'][2]
            e = top if d > 0 else bot; sl = (bot if d > 0 else top) - d * P['buf'] * A
            sl = min(sl, e - 0.5 * A) if d > 0 else max(sl, e + 0.5 * A)      # at least half an ATR of room
            pend = dict(d=d, e=e, sl=sl, until=i + P['life'])
        elif E in ('ob', 'mss_ob') and x['ob'] and x['ob'][0] == d and al and (E == 'ob' or i - mss_i[d] <= P['life']):
            t_, b_ = x['ob'][1], x['ob'][2]
            e = t_ if d > 0 else b_; sl = (b_ if d > 0 else t_) - d * P['buf'] * A
            sl = min(sl, e - 0.5 * A) if d > 0 else max(sl, e + 0.5 * A)
            pend = dict(d=d, e=e, sl=sl, until=i + 2 * P['life'])
        if mkt is not None:
            r = abs(x['c'] - mkt)
            if 0 < r <= 4 * A and (x['c'] - mkt) * d > 0:
                pos = dict(t=x['tc'], wk=x['wk'], d=d, e=x['c'], sl=mkt, r=r, tp=tpfor(P, d, x['c'], r, x))
    return res

def tpfor(P, d, e, r, x):
    if P['exit'] in ('tp2', 'tp3', 'tp4'): return e + d * int(P['exit'][2]) * r
    if P['exit'] == 'liq':
        lv = x['zzhi'] if d > 0 else x['zzlo']
        return lv if lv is not None and (lv - e) * d >= 2 * r else e + d * 3 * r
    return None

if __name__ == '__main__':
    ALL = USDP + EURP; DATA = {p: features(prep(p)) for p in ALL}
    def ev(P, pairs=ALL, per=H):
        hs = [sum([run(p, DATA[p], P, a, c) for p in pairs], []) for a, c in per]
        t = sorted(sum(hs, []), key=lambda x: x['tx']); eq = pk = dd = 0; wk = collections.defaultdict(float)
        for x in t: eq += x['R']; pk = max(pk, eq); dd = min(dd, eq - pk); wk[x['wk'][1]] += x['R']
        w = [wk.get(q, 0) for q in range(40, 48)]
        return dict(n=len(t), h=[sum(x['R'] for x in h_) for h_ in hs], dd=dd, b2=[w[i] + w[i + 1] for i in range(0, 8, 2)],
                    win=sum(x['R'] > 0 for x in t) / max(1, len(t)), R=sum(x['R'] for x in t))
    rows = []
    for E in ['mss', 'bos', 'sweep_mss', 'sweep_any', 'fvg', 'mss_fvg', 'ob', 'mss_ob']:
        for ex in ['tp2', 'tp3', 'liq', 'mss']:
            for kz in [False, True]:
                P = dict(entry=E, exit=ex, kz=kz); r = ev(P); pre = ev({**P, 'dirm': 'trend'}, ALL, [PRE])
                rows.append((E, ex, kz, r, pre))
    rows.sort(key=lambda z: -z[3]['R'])
    print('entry      exit kz  | W40-47 bias: tr win  H1/H2 = total dd | before W40 (trend dir)')
    for E, ex, kz, r, pre in rows[:20] + [('...', '', '', None, None)] + rows[-5:]:
        if r is None: print('   ...'); continue
        both = '✓' if min(r['h']) > 0 and pre['R'] > 0 else ' '
        print(f"{both} {E:<10} {ex:<4} {'KZ' if kz else '  '} | {r['n']:3}tr {r['win']:.0%} {r['h'][0]:+5.1f}/{r['h'][1]:+5.1f} = {r['R']:+5.1f}R dd {r['dd']:+5.1f} 2wk[{', '.join(f'{v:+.1f}' for v in r['b2'])}] | {pre['n']}tr {pre['R']:+.1f}R")
