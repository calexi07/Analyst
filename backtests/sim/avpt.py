# "Anchored VWAP Pullback & Target Zones [PhenLabs]" rebuilt for testing, one fixed profile (Auto-Optimize picks the best
# profile on the same history = look-ahead, so it is not tested). No volume in our data -> the script's own fallback weight
# (bar range / ATR). Swing pivot (10/10) anchors a VWAP from the pivot bar; armed after a 1.4 ATR impulse; pullback into
# AVWAP +/- band, reclaim candle (close > AVWAP, bullish, close >= prev high - 0.2 ATR) with Kaufman ER and quality filters ->
# entry at close, stop beyond the pullback/band (+0.2 ATR), risk clamped 0.35-3 ATR, TP 1/2/3R with the impulse-high magnet,
# BE after TP1, time exit after 60 bars, opposite signal flips. Conservative intrabar (stop first).
import sys, os, math, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smc import prep, B, H, PRE, USDP, EURP, cost_of, pip_of
PROF = {'bal': (1.00, 2.00, 26, 52, 1.00, 0.35), 'cons': (0.80, 1.75, 35, 60, 1.15, 0.35), 'aggr': (1.25, 2.30, 18, 44, 0.85, 0.30),
        'shal': (0.65, 1.60, 30, 55, 0.90, 0.30), 'deep': (1.45, 2.50, 22, 48, 1.25, 0.40)}
DEF = dict(prof='bal', sw=10, maxpb=2, imp=1.4, slb=0.2, be=True, mag=True, part=False, bias=False, hours=None, tmax=60)
clamp = lambda v, a, b: min(max(v, a), b)

def run(p, b, P, start, end):
    P = {**DEF, **P}; band, outer, minEr, minQ, slS, minR = PROF[P['prof']]; L = P['sw']
    cost = cost_of(p) * pip_of(p); n = len(b); res = []
    A = [x['atr'] or (x['h'] - x['l']) for x in b]
    W = [max((x['h'] - x['l']) / max(A[i], 1e-9), 0.1) for i, x in enumerate(b)]
    hl3 = [(x['h'] + x['l'] + x['c']) / 3 for x in b]
    an = {1: None, -1: None}     # anchor state per side
    zone = {1: None, -1: None}   # pullback extreme while in zone
    pos = None
    for i, x in enumerate(b):
        a = A[i]; o, h, l, c = x['o'], x['h'], x['l'], x['c']
        # ---- manage position
        if pos and i > pos['i']:
            d = pos['d']; sl = pos['sl']; hit_sl = (l <= sl) if d > 0 else (h >= sl)
            fav = h if d > 0 else l
            def close_(px, why):
                R = d * (px - pos['e']) / pos['r']
                if pos.get('banked') is not None: R = 0.5 * pos['banked'] + 0.5 * R
                res.append(dict(p=p, d=d, t=pos['t'], tx=x['tc'], wk=pos['wk'], R=R - cost / pos['r'], why=why))
            if hit_sl: close_(sl if d * (o - sl) > 0 else o, 'BE' if pos['t1h'] else 'SL'); pos = None
            else:
                if not pos['t1h'] and d * (fav - pos['t1']) >= 0:
                    pos['t1h'] = True
                    if P['part']: pos['banked'] = 1.0
                    if P['be']: pos['sl'] = pos['e']
                if d * (fav - pos['t3']) >= 0: close_(pos['t3'], 'TP3'); pos = None
                elif i - pos['i'] >= P['tmax']: close_(c, 'time'); pos = None
        # ---- update anchors
        for s in (1, -1):
            A_ = an[s]
            if not A_: continue
            A_['sw'] += W[i] * hl3[i]; A_['sw2'] += W[i] * hl3[i] ** 2; A_['w'] += W[i]
            A_['v'] = A_['sw'] / A_['w']; A_['sd'] = max(math.sqrt(max(0, A_['sw2'] / A_['w'] - A_['v'] ** 2)), 0.25 * a)
            if s * (h if s > 0 else l) >= s * A_['ext']: A_['ext'] = h if s > 0 else l
            if not A_['arm'] and s * (A_['ext'] - A_['px']) >= P['imp'] * a: A_['arm'] = True
            if s * (c - A_['px']) < 0 or s * (c - (A_['v'] - s * 2.6 * A_['sd'])) < 0: an[s] = None; zone[s] = None
        # ---- seed anchors at confirmed pivots
        if i >= 2 * L:
            k = i - L; win = b[i - 2 * L:i + 1]
            for s in (1, -1):
                pv = b[k]['l'] if s > 0 else b[k]['h']
                isp = (pv == min(y['l'] for y in win)) if s > 0 else (pv == max(y['h'] for y in win))
                if not isp: continue
                A_ = an[s]
                rep = (A_ is None or s * (pv - A_['px']) < 0 or A_['used'] >= P['maxpb'] or
                       (A_['arm'] and s * (pv - A_['px']) > 0 and s * ((h if s > 0 else l) - pv) >= P['imp'] * a))
                if rep and s * (c - pv) > 0:
                    sw = sum(W[j] * hl3[j] for j in range(k, i + 1)); sw2 = sum(W[j] * hl3[j] ** 2 for j in range(k, i + 1)); w = sum(W[j] for j in range(k, i + 1))
                    ext = max(y['h'] for y in b[k:i + 1]) if s > 0 else min(y['l'] for y in b[k:i + 1])
                    v = sw / w; an[s] = dict(px=pv, sw=sw, sw2=sw2, w=w, v=v, sd=max(math.sqrt(max(0, sw2 / w - v * v)), 0.25 * a),
                                             ext=ext, arm=s * (ext - pv) >= P['imp'] * a, used=0); zone[s] = None
        if i < 11: continue
        er = abs(c - b[i - 10]['c']) / max(sum(abs(b[j]['c'] - b[j - 1]['c']) for j in range(i - 9, i + 1)), 1e-12) * 100
        span = max(h - l, 1e-12); act = clamp(span / a / 2, 0, 1); ern = clamp(er / 55, 0, 1)
        took = False
        for s in (1, -1):
            A_ = an[s]
            if took or not A_ or not A_['arm'] or A_['used'] >= P['maxpb']: continue
            v, sd = A_['v'], A_['sd']; inner = v + s * band * sd; deff = v - s * outer * sd
            ext_ = h if s > 0 else l
            if s * (inner - (l if s > 0 else h)) >= 0 and s * (c - deff) >= 0 and s * (c - A_['px']) > 0 and s * (A_['ext'] - ext_) > 0:
                pb = l if s > 0 else h
                zone[s] = pb if zone[s] is None else (min(zone[s], pb) if s > 0 else max(zone[s], pb))
            elif s * (c - deff) < 0: zone[s] = None
            prevx = b[i - 1]['h'] if s > 0 else b[i - 1]['l']
            if zone[s] is not None and s * (c - v) > 0 and s * (c - o) > 0 and s * (c - (prevx - s * 0.2 * a)) >= 0 and not (pos and pos['d'] == s):
                share = clamp(((c - l) if s > 0 else (h - c)) / span, 0, 1)
                q = clamp((0.40 * share + 0.35 * ern + 0.25 * act) * 100, 0, 100)
                leg = max(s * (A_['ext'] - A_['px']), 0.5 * a); depth = s * (A_['ext'] - zone[s]) / leg
                mv5 = (c - b[i - 5]['c']) / a; crash = (mv5 > 3.6 and c > o) if s < 0 else (mv5 < -3.6 and c < o)
                ok = er >= minEr and q >= minQ and 0.12 <= depth <= 0.85 and not crash
                bi_ = B.get((p, x['wk']), ('-',))[0]; bd = 1 if bi_ == 'U' else -1 if bi_ == 'D' else 0
                live = start <= x['t'] < end and (not P['bias'] or bd == s) and (not P['hours'] or P['hours'][0] <= x['hr'] < P['hours'][1])
                if ok:
                    took = True
                    if live:
                        if pos:   # flip: close the open opposite plan at this close
                            R = pos['d'] * (c - pos['e']) / pos['r']
                            if pos.get('banked') is not None: R = 0.5 * pos['banked'] + 0.5 * R
                            res.append(dict(p=p, d=pos['d'], t=pos['t'], tx=x['tc'], wk=pos['wk'], R=R - cost / pos['r'], why='flip')); pos = None
                        raw = (min(zone[s], v - band * sd) - slS * P['slb'] * a) if s > 0 else (max(zone[s], v + band * sd) + slS * P['slb'] * a)
                        r = clamp(abs(c - raw), minR * a, 3 * a); t3 = c + s * 3 * r
                        if P['mag']:
                            dR = s * (A_['ext'] - c) / r
                            if 2.4 < dR <= 4.5: t3 = A_['ext']
                        pos = dict(i=i, d=s, e=c, r=r, sl=c - s * r, t1=c + s * r, t3=t3, t1h=False, t=x['t'], wk=x['wk'])
                    A_['used'] += 1
                zone[s] = None
    return res

if __name__ == '__main__':
    ALL = USDP + EURP; DATA = {p: prep(p) for p in ALL}
    def ev(P, per=H):
        hs = [sum([run(p, DATA[p], P, a, c) for p in ALL], []) for a, c in per]
        t = sorted(sum(hs, []), key=lambda x: x['tx']); eq = pk = dd = 0
        for x in t: eq += x['R']; pk = max(pk, eq); dd = min(dd, eq - pk)
        why = collections.Counter(x['why'] for x in t); w = sum(x['R'] > 0 for x in t) / max(1, len(t))
        return f"{len(t):3}tr win {w:.0%} {', '.join(f'{k} {v}' for k, v in sorted(why.items()))} | {' / '.join(f'{sum(x['R'] for x in h_):+.1f}' for h_ in hs)} = {eq:+6.1f}R dd {dd:+.1f}"
    for n, P in [('Balanced, both directions', {}), ('  + engine bias', dict(bias=True)), ('  + bias + 06-22', dict(bias=True, hours=(6, 22))),
                 ('  + bias, 50% at TP1 (their R math)', dict(bias=True, part=True)), ('  + bias, no BE', dict(bias=True, be=False)),
                 ('Conservative + bias', dict(prof='cons', bias=True)), ('Aggressive + bias', dict(prof='aggr', bias=True)),
                 ('Shallow + bias', dict(prof='shal', bias=True)), ('Deep + bias', dict(prof='deep', bias=True))]:
        print(f"{n:<36} W40-47: {ev(P)}")
        print(f"{'':<36} pre-W40, both dirs: {ev({**P, 'bias': False}, per=[PRE])}")
