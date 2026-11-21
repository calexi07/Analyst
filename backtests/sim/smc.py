# Five structure / liquidity strategies (BOS, CHoCH, internal vs swing structure, liquidity sweeps, FVG, draw on liquidity),
# all run on the 1H path with the engine's weekly bias as direction. Market-structure pivots are confirmed only after
# their right-hand bars close (no lookahead). Worst case on limit fills: stop counted if touched on the fill candle.
import sys, os, datetime as D, statistics as St, collections
from zoneinfo import ZoneInfo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from swing2 import *
from mtf import load1h
BUC = ZoneInfo('Europe/Bucharest'); U = lambda *a: D.datetime(*a, tzinfo=D.timezone.utc)
H = [(U(2026, 9, 27, 21), U(2026, 10, 25, 21)), (U(2026, 10, 25, 21), U(2026, 11, 22))]
PRE = (U(2026, 8, 16, 21), U(2026, 9, 27, 21))            # before the bias weeks: trend direction only
USDP = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'USDCAD', 'AUDUSD', 'NZDUSD', 'XAUUSD']
EURP = ['EURGBP', 'EURJPY', 'EURCHF', 'EURAUD', 'EURNZD', 'EURCAD']
B = bias_table()

def prep(p):
    b = load1h(p); a = None
    for i, x in enumerate(b):
        tr = x['h'] - x['l'] if i == 0 else max(x['h'], b[i - 1]['c']) - min(x['l'], b[i - 1]['c'])
        a = tr if a is None else (a * 13 + tr) / 14; x['atr'] = a if i >= 14 else None
        x['hr'] = x['t'].astimezone(BUC).hour
    # daily closes (NY trading day) -> SMA20 of completed days, previous week high/low, Asian range (00-08 Bucharest)
    dc = collections.OrderedDict(); wk = collections.OrderedDict()
    for x in b:
        dc[x['day']] = x['c']; w = wk.setdefault(x['wk'], [x['h'], x['l']]); w[0] = max(w[0], x['h']); w[1] = min(w[1], x['l'])
    dl = list(dc.items()); sma = {}
    for i, (d, c) in enumerate(dl): sma[d] = St.mean([v for _, v in dl[i - 20:i]]) if i >= 20 else None
    lastc = {d: dl[i - 1][1] if i else None for i, (d, _) in enumerate(dl)}
    wl = list(wk.items()); pw = {w: (wl[i - 1][1] if i else None) for i, (w, _) in enumerate(wl)}
    asia = {}
    for x in b:
        if x['hr'] < 8:
            a_ = asia.setdefault(x['day'], [x['h'], x['l']]); a_[0] = max(a_[0], x['h']); a_[1] = min(a_[1], x['l'])
    for x in b:
        s = sma.get(x['day']); lc = lastc.get(x['day'])
        x['td'] = 0 if s is None or lc is None else (1 if lc > s else -1); x['pw'] = pw.get(x['wk']); x['asia'] = asia.get(x['day'])
    return b

def pivots(b, L):
    # (confirm_index, pivot_index, price) lists for highs and lows
    hi, lo = [], []
    for k in range(L, len(b) - L):
        if b[k]['h'] == max(x['h'] for x in b[k - L:k + L + 1]): hi.append((k + L, k, b[k]['h']))
        if b[k]['l'] == min(x['l'] for x in b[k - L:k + L + 1]): lo.append((k + L, k, b[k]['l']))
    return hi, lo

DEF = dict(dirm='bias', exit='tp3', fri=True, hours=(6, 22), cool=12, maxdow=3, swL=12, inL=3, maxrisk=4.0)

def run(p, b, P, start, end):
    P = {**DEF, **P}; cost = cost_of(p) * pip_of(p)
    sw_h, sw_l = pivots(b, P['swL']); in_h, in_l = pivots(b, P['inL']); tr_h, tr_l = pivots(b, P.get('trL', 6))
    def last(lst, i, after=-1):     # most recent pivot confirmed by bar i (pivot index > after)
        r = None
        for c, k, v in lst:
            if c > i: break
            if k > after: r = (k, v)
        return r
    res, pos, pend, lastx, st = [], None, None, None, {}
    for i, x in enumerate(b):
        if x['atr'] is None: continue
        # ---------- manage
        if pos:
            d = pos['d']
            if (x['l'] <= pos['sl']) if d > 0 else (x['h'] >= pos['sl']):
                g = (x['o'] < pos['sl']) if d > 0 else (x['o'] > pos['sl']); ex = (x['o'] if g else pos['sl'], 'SL')
            elif pos['tp'] and ((x['h'] >= pos['tp']) if d > 0 else (x['l'] <= pos['tp'])): ex = (pos['tp'], 'TP')
            elif P['fri'] and x['dow'] == 4 and x['last_of_day']: ex = (x['c'], 'Fri')
            else:
                ex = None
                bi = B.get((p, x['wk']), ('-',))[0]; bd = 1 if bi == 'U' else -1 if bi == 'D' else 0
                if P['dirm'] == 'bias' and bd == -d and x['dow'] == 0 and x['hr'] < 2: ex = (x['o'], 'Flip')
                if not ex and P['exit'].startswith('struct'):
                    lv = last(tr_l if d > 0 else tr_h, i, pos['i'])
                    if lv: pos['sl'] = max(pos['sl'], lv[1] - d * 0.1 * x['atr']) if d > 0 else min(pos['sl'], lv[1] - d * 0.1 * x['atr'])
            if ex:
                R = (ex[0] - pos['e']) * d / pos['r'] - cost / pos['r']
                res.append(dict(p=p, t=pos['t'], tx=x['tc'], R=R, why=ex[1], wk=pos['wk'], s=pos['s'])); pos = None; lastx = x['tc']
            continue
        if not (start <= x['t'] < end): pend = None; st = {}; continue
        if pend:
            if i > pend['until']: pend = None
            elif (x['l'] <= pend['e']) if pend['d'] > 0 else (x['h'] >= pend['e']):
                pos = dict(i=i, t=x['t'], wk=x['wk'], d=pend['d'], e=pend['e'], sl=pend['sl'], r=abs(pend['e'] - pend['sl']), tp=pend['tp'], s=pend['s']); pend = None
                if (x['l'] <= pos['sl']) if pos['d'] > 0 else (x['h'] >= pos['sl']):
                    res.append(dict(p=p, t=x['t'], tx=x['tc'], R=-1 - cost / pos['r'], why='SL same bar', wk=pos['wk'], s=pos['s'])); pos = None; lastx = x['tc']
                continue
        if lastx and (x['tc'] - lastx).total_seconds() < P['cool'] * 3600: continue
        bi = B.get((p, x['wk']), ('-', '-', None)); bd = 1 if bi[0] == 'U' else -1 if bi[0] == 'D' else 0
        d = bd if P['dirm'] == 'bias' else x['td'] if P['dirm'] == 'trend' else (bd if bd == x['td'] else 0)
        allow = x['dow'] <= P['maxdow'] and P['hours'][0] <= x['hr'] < P['hours'][1]
        if d == 0: continue
        if not allow and not P.get('state_always'): continue
        A = x['atr']; S = P['strat']; entry = None
        if S == 'sweep_choch':      # swing liquidity taken against the bias, then an internal CHoCH back in the bias direction
            sl_ = last(sw_l if d > 0 else sw_h, i)
            k = st.get('sw')
            if sl_ and ((x['l'] < sl_[1]) if d > 0 else (x['h'] > sl_[1])) and (not k or k['lvl'] != sl_[1]):
                st['sw'] = k = dict(lvl=sl_[1], i=i, ext=x['l'] if d > 0 else x['h'], d=d)
            if k and k['d'] == d and i - k['i'] <= 24:
                k['ext'] = min(k['ext'], x['l']) if d > 0 else max(k['ext'], x['h'])
                ih = last(in_h if d > 0 else in_l, i)
                if ih and (x['c'] - ih[1]) * d > 0 and ih[0] >= k['i'] - 12:
                    entry = (x['c'], k['ext'] - d * 0.1 * A); st.pop('sw')
        elif S == 'bos_discount':   # swing BOS, pullback into the discount half of the leg, internal CHoCH back
            k = st.get('bos')
            sh = last(sw_h if d > 0 else sw_l, i)
            if sh and (x['c'] - sh[1]) * d > 0 and (not k or k['lvl'] != sh[1]):
                lo = last(sw_l if d > 0 else sw_h, i)
                if lo: st['bos'] = k = dict(lvl=sh[1], i=i, a=lo[1], ext=x['h'] if d > 0 else x['l'], d=d, pb=None, pbi=None)
            if k and k['d'] == d and k.get('i') != i:
                if i - k['i'] > 72 or (x['c'] - k['a']) * d < 0: st.pop('bos'); k = None
            if k and k['d'] == d and k.get('i') != i:
                mid = k['a'] + 0.5 * (k['ext'] - k['a'])
                if k['pb'] is None:
                    k['ext'] = max(k['ext'], x['h']) if d > 0 else min(k['ext'], x['l'])
                    if (x['l'] <= mid) if d > 0 else (x['h'] >= mid): k['pb'] = x['l'] if d > 0 else x['h']; k['pbi'] = i
                else:
                    k['pb'] = min(k['pb'], x['l']) if d > 0 else max(k['pb'], x['h'])
                    ih = last(in_h if d > 0 else in_l, i, k['pbi'] - 6)
                    if ih and (x['c'] - ih[1]) * d > 0 and allow: entry = (x['c'], k['pb'] - d * 0.1 * A); st.pop('bos')
        elif S == 'asia_judas':     # London takes the Asian range against the bias, then an internal CHoCH (L=2) back
            if x['asia'] and 8 <= x['hr'] < 13:
                lvl = x['asia'][1] if d > 0 else x['asia'][0]; k = st.get('j')
                if (not k or k['day'] != x['day']) and ((x['l'] < lvl) if d > 0 else (x['h'] > lvl)):
                    st['j'] = k = dict(day=x['day'], i=i, ext=x['l'] if d > 0 else x['h'], d=d)
                if k and k['day'] == x['day'] and k['d'] == d:
                    k['ext'] = min(k['ext'], x['l']) if d > 0 else max(k['ext'], x['h'])
                    ih = last(tr_h if False else (pivots_cache := None) or in_h if d > 0 else in_l, i)
                    if ih and (x['c'] - ih[1]) * d > 0 and ih[0] >= k['i'] - 6 and (x['c'] - lvl) * d > 0:
                        entry = (x['c'], k['ext'] - d * 0.1 * A); st.pop('j')
        elif S == 'fvg_disp':       # displacement candle that breaks internal structure and leaves a FVG; limit at its midpoint
            if i >= 2:
                body = (x['c'] - x['o']) * d; ih = last(in_h if d > 0 else in_l, i - 1)
                gap = (x['l'] > b[i - 2]['h']) if d > 0 else (x['h'] < b[i - 2]['l'])
                if body > 1.5 * A and ih and (x['c'] - ih[1]) * d > 0 and gap:
                    top, bot = (x['l'], b[i - 2]['h']) if d > 0 else (b[i - 2]['l'], x['h'])
                    e = (top + bot) / 2; sl = (min(b[i - 1]['l'], b[i - 2]['l']) if d > 0 else max(b[i - 1]['h'], b[i - 2]['h'])) - d * 0.1 * A
                    if abs(e - sl) <= P['maxrisk'] * A:
                        tp = e + d * 3 * abs(e - sl) if P['exit'] == 'tp3' else e + d * 2 * abs(e - sl) if P['exit'] == 'tp2' else None
                        if P['exit'] == 'liq':
                            lq = last(sw_h if d > 0 else sw_l, i); tp = lq[1] if lq and (lq[1] - e) * d >= 2 * abs(e - sl) else e + d * 3 * abs(e - sl)
                        pend = dict(d=d, e=e, sl=sl, tp=tp, until=i + 12, s=S)
        elif S == 'weekly_draw':    # early in the week, internal BOS toward last week's high/low; target = that liquidity
            if x['pw'] and x['dow'] <= 1:
                tgt = x['pw'][0] if d > 0 else x['pw'][1]
                ih = last(in_h if d > 0 else in_l, i); il = last(in_l if d > 0 else in_h, i)
                if ih and il and (x['c'] - ih[1]) * d > 0 and (b[i - 1]['c'] - ih[1]) * d <= 0:
                    sl = il[1] - d * 0.1 * A; r = abs(x['c'] - sl)
                    if (tgt - x['c']) * d >= 1.5 * r and r <= P['maxrisk'] * A: pos = dict(i=i, t=x['tc'], wk=x['wk'], d=d, e=x['c'], sl=sl, r=r, tp=tgt, s=S)
        if entry:
            e, sl = entry; r = abs(e - sl)
            if r <= 0 or r > P['maxrisk'] * A: continue
            tp = e + d * 3 * r if P['exit'] == 'tp3' else e + d * 2 * r if P['exit'] == 'tp2' else None
            if P['exit'] == 'liq':
                lq = last(sw_h if d > 0 else sw_l, i); tp = lq[1] if lq and (lq[1] - e) * d >= 2 * r else e + d * 3 * r
            pos = dict(i=i, t=x['tc'], wk=x['wk'], d=d, e=e, sl=sl, r=r, tp=tp, s=S)
    return res

if __name__ == '__main__':
    ALL = USDP + EURP; DATA = {p: prep(p) for p in ALL}
    def ev(P, pairs, per=H):
        hs = [sum([run(p, DATA[p], P, a, c) for p in pairs], []) for a, c in per]
        t = sorted(sum(hs, []), key=lambda x: x['tx']); eq = pk = dd = 0; wk = collections.defaultdict(float)
        for x in t: eq += x['R']; pk = max(pk, eq); dd = min(dd, eq - pk); wk[x['wk'][1]] += x['R']
        w = [wk.get(q, 0) for q in range(40, 48)]
        return t, [sum(x['R'] for x in h_) for h_ in hs], dd, [w[i] + w[i + 1] for i in range(0, 8, 2)]
    def line(n, r, pre=None):
        t, hs, dd, b2 = r; win = sum(x['R'] > 0 for x in t) / max(1, len(t)); avg = St.mean([x['R'] for x in t]) if t else 0
        pr = f" | before W40, trend dir: {len(pre[0])}tr {sum(x['R'] for x in pre[0]):+.1f}R" if pre else ''
        print(f"{n:<44} {len(t):3}tr win {win:.0%} avg {avg:+.2f} {hs[0]:+5.1f}/{hs[1]:+5.1f} = {sum(hs):+5.1f}R dd {dd:+.1f} 2wk[{', '.join(f'{v:+.1f}' for v in b2)}]{pr}")
    for S in ['sweep_choch', 'bos_discount', 'asia_judas', 'fvg_disp', 'weekly_draw']:
        print('==', S)
        for ex in (['liq'] if S == 'weekly_draw' else ['tp2', 'tp3', 'liq', 'struct']):
            for fri in ([True, False] if ex == 'struct' else [True]):
                P = dict(strat=S, exit=ex, fri=fri)
                n = f"  {ex}{'' if fri else ' (no Friday close, flip exit)'}"
                line(n + ' 14 pairs', ev(P, ALL), ev({**P, 'dirm': 'trend'}, ALL, [PRE]))
