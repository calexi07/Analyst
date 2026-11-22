# Full port of "HTF Sweep CISD Setups [WillyAlgoTrader] v1.7.1" (trade engine included) for parameter search on EURUSD.
# Bullish logic in transformed price space (shorts = negated prices), as in the original.
import sys, os, math, datetime as Dt
from zoneinfo import ZoneInfo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smc import B, cost_of, pip_of
NY = ZoneInfo('America/New_York'); BUC = ZoneInfo('Europe/Bucharest')
ENTRY_FAM = {'obHL': 0, 'obOpen': 0, 'obMT': 0, 'obXHL': 0, 'obXC': 0, 'fvgC': 1, 'fvgCE': 1, 'fvgO': 1,
             'ifO': 2, 'ifCE': 2, 'ifC': 2, 'ifXHL': 2, 'ifXC': 2, 'brHL': 3, 'brC': 3, 'brXHL': 3, 'brXC': 3, 'uni': 4}
PRESET = {'Conservative': (2.5, 1.0, 2.0, 4.0), 'Balanced': (1.5, 1.0, 2.0, 3.0), 'Aggressive': (1.0, 1.5, 2.5, 4.0), 'Scalping': (0.8, 0.8, 1.5, 2.0)}
DEF = dict(htf='auto', piv=3, wait=36, pre=30, fvglife=120, age=120, waitClose=False, sweepPrev=True, sweepBody=False, sweepAny=True, look=10,
           stPivot=False, entry='brC', stop='piv', stopBuf=0.0, pend=60, reqOb=False, reqFvg=False, reqFvgOb=False, reqIfvg=False, reqBrk=False,
           reqPivot=True, reqUni=False, kz=(), minRisk=0.25, maxRisk=3.0, disp=0.5, minFvg=0.1, skipStale=True, cancelOut=True,
           entryMode='Limit', slMode='Structure', preset='Balanced', tps=None, be=True, model='Conservative', pd='Off', pdN=4,
           tpMode='Fixed R', minRR=1.5, pdLiq=True, noLiqFb=True, eng=True, hours=(6, 22), noFri=True, conflict='skip')
AUTO = {5: '60', 15: '240', 30: 'D', 60: 'D', 240: 'W'}
class Ctx:
    def __init__(s, d): s.d = d; s.active = False; s.pv = []; s.reset_all()
    def reset_all(s):
        s.trig = s.made = None; s.level = s.levelBar = s.anchor = None; s.ext = s.extBar = None; s.inRun = False
        s.rOpen = s.rHigh = s.rLow = s.rMinC = s.rStart = s.rPH = s.rPL = s.rPC = s.rPBar = None
        s.kOpen = s.kHigh = s.kLow = s.kMinC = s.kStart = s.kPH = s.kPL = s.kPC = s.kPBar = None
        s.obX = False; s.obBar = s.xL = s.xC = None; s.fvg = False; s.fvgTop = s.fvgBot = s.fvgBar = None
        s.ifvg = False; s.ifTop = s.ifBot = s.ixL = s.ixC = s.ifBar = s.ifXBar = None
        s.brk = False; s.brBar = s.brXBar = s.brTop = s.brBot = s.brC = s.bxL = s.bxC = None; s.opp = []
def run(p, b, P, start, end, mins=60):
    P = {**DEF, **P}; htf = AUTO[mins] if P['htf'] == 'auto' else P['htf']
    slm, t1m, t2m, t3m = PRESET.get(P['preset'], PRESET['Balanced']) if P['tps'] is None else P['tps']
    cost = cost_of(p) * pip_of(p); N = len(b); L = P['piv']
    O = [x['o'] for x in b]; Hh = [x['h'] for x in b]; Ll = [x['l'] for x in b]; C = [x['c'] for x in b]; A = [x['atr'] or 0.0 for x in b]
    nyt = [(x['t']).astimezone(NY) for x in b]
    def key(i):
        t = nyt[i] + Dt.timedelta(hours=7)
        if htf == 'D': return t.date()
        if htf == 'W': return t.date().isocalendar()[:2]
        if htf == '240': return (t.date(), t.hour // 4)
        return (t.date(), t.hour)
    def dkey(i): return (nyt[i] + Dt.timedelta(hours=7)).date()
    def kz_ok(i):
        if not P['kz']: return True
        m = nyt[i].hour * 60 + nyt[i].minute
        win = {'asia': (20 * 60, 24 * 60), 'london': (120, 300), 'nyam': (510, 660), 'nypm': (810, 960)}
        return any(win[k][0] <= m < win[k][1] for k in P['kz'])
    bull, bear = Ctx(1), Ctx(-1)
    htfs = []; cur = None; liqH = []; liqL = []; hcount = 0; first_done = False
    flags = dict(bP=False, sP=False, bB=False, sB=False); accL = accH = None; accLB = accHB = None
    dayHi = dayLo = pdH = pdL = None; lastday = None
    tr = None; pend = None; res = []
    def T(i, d, k=0):
        j = i - k
        if j < 0: return (None,) * 4
        return (O[j], Hh[j], Ll[j], C[j]) if d == 1 else (-O[j], -Ll[j], -Hh[j], -C[j])
    def advance(t, bi, cnt):
        d = t.d; o, h, l, c = T(bi, d); _, h1, l1, c1 = T(bi, d, 1); _, h2, l2, _ = T(bi, d, 2); a = A[bi]
        disp = c - o >= P['disp'] * a; newExt = False
        if cnt and (t.ext is None or l < t.ext): t.ext = l; t.extBar = bi; newExt = True
        if c < o:
            if not t.inRun: t.inRun = True; t.rOpen = o; t.rHigh = h; t.rLow = l; t.rMinC = c; t.rStart = bi; t.rPH, t.rPL, t.rPC, t.rPBar = h1, l1, c1, bi - 1
            else: t.rHigh = max(t.rHigh, h); t.rLow = min(t.rLow, l); t.rMinC = min(t.rMinC, c)
        else: t.inRun = False
        if newExt:
            t.kOpen, t.kHigh, t.kLow, t.kMinC, t.kStart = t.rOpen, t.rHigh, t.rLow, t.rMinC, t.rStart
            t.kPH, t.kPL, t.kPC, t.kPBar = t.rPH, t.rPL, t.rPC, t.rPBar
            t.obX = t.fvg = t.ifvg = t.brk = False
        elif t.inRun and t.rStart == t.kStart: t.kMinC = t.rMinC; t.kLow = t.rLow
        if l2 is not None and h < l2 and l2 - h >= P['minFvg'] * a: t.opp.append([l2, h, bi - 1])
        for j in range(len(t.opp) - 1, -1, -1):
            tp, bt_, ob = t.opp[j]; inWin = cnt and t.extBar is not None and bi >= t.extBar; rm = False
            if c > tp and inWin and disp:
                t.ifvg = True; t.ifXBar = bi; t.ifTop = tp; t.ifBot = bt_; t.ixL = l; t.ixC = c; t.ifBar = ob - 1; rm = True
            elif c > tp and not inWin: rm = True
            elif bi - ob > P['fvglife']: rm = True
            if rm: t.opp.pop(j)
        if cnt and t.extBar is not None and bi >= t.extBar:
            if t.obX and c < t.kLow: t.obX = False
            if t.ifvg and c < t.ifBot: t.ifvg = False
            if t.brk and t.brBot is not None and c < t.brBot: t.brk = False
            if not t.obX and t.kOpen is not None and c > t.kOpen and disp: t.obX = True; t.obBar = bi; t.xL = l; t.xC = c
            if bi - 2 >= t.extBar and h2 is not None and l > h2 and l - h2 >= P['minFvg'] * a:
                t.fvg = True; t.fvgTop = l; t.fvgBot = h2; t.fvgBar = bi - 1
            elif t.fvg and c < t.fvgBot: t.fvg = False
            if not t.brk:
                lv = zb = zc = zx = None
                if P['reqPivot']:
                    for pp, pb, plw, pcl in reversed(t.pv):
                        if pb < t.extBar and pb + L <= bi: lv, zb, zc, zx = pp, plw, pcl, pb; break
                else: lv, zb, zc, zx = t.kPH, t.kPL, t.kPC, t.kPBar
                if lv is not None and c > lv and disp:
                    t.brk = True; t.brXBar = bi; t.brBar = zx; t.brTop = lv; t.brBot = zb; t.brC = zc; t.bxL = l; t.bxC = c
    def build(t, i):
        uni = False; uTop = None
        if t.brk and t.fvg:
            ovT = min(t.brTop, t.fvgTop); ovB = max(t.brBot, t.fvgBot)
            if ovT > ovB: uni = True; uTop = ovT
        fvgOb = t.fvg and t.obX and t.fvgTop > t.kOpen and t.fvgBar >= t.obBar - 1
        miss = (P['reqOb'] and not t.obX) or (P['reqFvg'] and not t.fvg) or (P['reqFvgOb'] and not fvgOb) or (P['reqIfvg'] and not t.ifvg) or (P['reqBrk'] and not t.brk) or (P['reqUni'] and not uni)
        E = P['entry']
        e = {'obHL': t.kHigh if t.obX else None, 'obOpen': t.kOpen if t.obX else None, 'obMT': (t.kOpen + t.kMinC) / 2 if t.obX else None,
             'obXHL': t.xL if t.obX else None, 'obXC': t.xC if t.obX else None, 'fvgC': t.fvgTop if t.fvg else None,
             'fvgCE': (t.fvgTop + t.fvgBot) / 2 if t.fvg else None, 'fvgO': t.fvgBot if t.fvg else None,
             'ifO': t.ifTop if t.ifvg else None, 'ifCE': (t.ifTop + t.ifBot) / 2 if t.ifvg else None, 'ifC': t.ifBot if t.ifvg else None,
             'ifXHL': t.ixL if t.ifvg else None, 'ifXC': t.ixC if t.ifvg else None, 'brHL': t.brTop if t.brk else None, 'brC': t.brC if t.brk else None,
             'brXHL': t.bxL if t.brk else None, 'brXC': t.bxC if t.brk else None, 'uni': uTop if uni else None}[E]
        fam = ENTRY_FAM[E]
        xl = (t.ixL if t.ifvg else None) if fam == 2 else (t.bxL if t.brk else None) if fam == 3 else (t.xL if t.obX else None)
        s = {'piv': t.ext, 'ob': t.kLow if t.obX else None, 'cross': xl, 'fvg': t.fvgBot if t.fvg else None, 'ifvg': t.ifBot if t.ifvg else None,
             'brk': t.brBot if t.brk else None}[P['stop']]
        if s is None: s = t.ext
        if s is not None: s = s - P['stopBuf'] * A[i]
        cT = C[i] if t.d == 1 else -C[i]
        cb = {0: t.obBar, 1: (t.fvgBar + 1) if t.fvg else None, 2: t.ifXBar, 3: t.brXBar}.get(fam, max(t.brXBar, t.fvgBar + 1) if (t.brk and t.fvg) else None)
        stale = False
        if P['skipStale'] and P['entryMode'] == 'Limit' and e is not None and cb is not None:
            for k in range(1, min(i - cb - 1, 400) + 1):
                lw = Ll[i - k] if t.d == 1 else -Hh[i - k]
                if lw <= e: stale = True; break
        stopOk = P['slMode'] != 'Structure' or (s is not None and e is not None and e > s and cT > s)
        ok = t.extBar is not None and not miss and e is not None and not stale and stopOk
        return ok, e, s
    def plan(t, i, e, s):
        d = t.d; cT = C[i] if d == 1 else -C[i]; lT = Ll[i] if d == 1 else -Hh[i]; a = A[i]
        mkt = P['entryMode'] == 'Market' or cT <= e; en = cT if mkt else e
        sl = min(lT - a * 0.25, en - a * 0.5) if P['slMode'] == 'Wick-Anchored' else (en - a * slm if P['slMode'] == 'ATR' else s)
        risk = en - sl
        if not (risk > 0 and cT > sl) or a <= 0: return None
        rA = risk / a
        if P['minRisk'] > 0 and rA < P['minRisk']: return None
        if P['maxRisk'] > 0 and rA > P['maxRisk']: return None
        rH = rL = None
        if P['pd'] == 'Previous day': rH, rL = pdH, pdL
        elif cur is not None:
            rH, rL = cur['h'], cur['l']
            for hb_ in htfs[-(P['pdN'] - 1):] if P['pdN'] > 1 else []: rH = max(rH, hb_['h']); rL = min(rL, hb_['l'])
        if rH is not None and rL is not None:
            pdGood = en < d * (rH + rL) / 2
            if P['pd'] != 'Off' and not pdGood: return None
        tp1 = en + risk * t1m; tp2 = en + risk * t2m; tp3 = en + risk * t3m
        if P['tpMode'] != 'Fixed R':
            cands = [d * q[0] for q in (liqH if d == 1 else liqL) if d * q[0] > en]
            if P['pdLiq']:
                pv = (pdH if (pdH is not None and dayHi <= pdH) else None) if d == 1 else ((-pdL) if (pdL is not None and dayLo >= pdL) else None)
                if pv is not None and pv > en: cands.append(pv)
            pick = None
            for v in sorted(cands):
                if P['tpMode'] == 'Nearest HTF liquidity' or ((v - en) / risk >= P['minRR'] and v > tp1): pick = v; break
            if pick is not None and (pick - en) / risk >= P['minRR'] and pick > tp1: tp3 = pick; tp2 = (tp1 + tp3) / 2
            elif not cands and P['noLiqFb']: pass
            else: return None
        if not (sl < en < tp1 < tp2 < tp3): return None
        return dict(dir=d, en=d * en, sl=d * sl, tp1=d * tp1, tp3=d * tp3, mkt=mkt)
    for i in range(N):
        # previous-day high/low (FX day)
        dk = dkey(i)
        if dk != lastday: pdH, pdL = dayHi, dayLo; dayHi, dayLo = Hh[i], Ll[i]; lastday = dk
        else: dayHi = max(dayHi, Hh[i]); dayLo = min(dayLo, Ll[i])
        # pivots
        if i >= 2 * L:
            k = i - L
            if Hh[k] > max(Hh[k - L:k]) and Hh[k] >= max(Hh[k + 1:i + 1]): bull.pv.append((Hh[k], k, Ll[k], C[k])); bull.pv[:] = bull.pv[-40:]
            if Ll[k] < min(Ll[k - L:k]) and Ll[k] <= min(Ll[k + 1:i + 1]): bear.pv.append((-Ll[k], k, -Hh[k], -C[k])); bear.pv[:] = bear.pv[-40:]
        # HTF aggregation + triggers
        bt = None; st = None
        def put(tg, lvl, lb, anch, d):
            if tg is None: return [lvl, lb, anch]
            if (lvl < tg[0]) if d == 1 else (lvl > tg[0]): tg[0], tg[1] = lvl, lb
            tg[2] = min(tg[2], anch); return tg
        kk = key(i)
        if cur is None or kk != cur['k']:
            if cur is not None and first_done:
                if htfs:
                    pp = htfs[-1]
                    if P['waitClose']:
                        if P['sweepPrev'] and cur['l'] < pp['l']: bt = put(bt, pp['l'], pp['lb'], cur['b'], 1)
                        if P['sweepPrev'] and cur['h'] > pp['h']: st = put(st, pp['h'], pp['hb'], cur['b'], -1)
                        if P['sweepAny'] and accL is not None: bt = put(bt, accL, accLB, cur['b'], 1)
                        if P['sweepAny'] and accH is not None: st = put(st, accH, accHB, cur['b'], -1)
                htfs.append(cur); htfs[:] = htfs[-300:]; hcount += 1
                liqH.append((cur['h'], cur['hb'], hcount)); liqL.append((cur['l'], cur['lb'], hcount))
            if cur is not None: first_done = True
            cur = dict(k=kk, o=O[i], h=Hh[i], l=Ll[i], c=C[i], b=i, hb=i, lb=i)
            flags = dict(bP=False, sP=False); accL = accH = None
        else:
            if Hh[i] > cur['h']: cur['h'] = Hh[i]; cur['hb'] = i
            if Ll[i] < cur['l']: cur['l'] = Ll[i]; cur['lb'] = i
            cur['c'] = C[i]
        if not P['waitClose'] and htfs:
            pp = htfs[-1]
            if P['sweepPrev'] and not flags['bP'] and Ll[i] < pp['l']: bt = put(bt, pp['l'], pp['lb'], i, 1); flags['bP'] = True
            if P['sweepPrev'] and not flags['sP'] and Hh[i] > pp['h']: st = put(st, pp['h'], pp['hb'], i, -1); flags['sP'] = True
        for arr, isH in ((liqL, False), (liqH, True)):
            sw = swB = None
            for j in range(len(arr) - 1, -1, -1):
                q = arr[j]
                if hcount - q[2] >= P['look']: arr.pop(j)
                elif (Hh[i] > q[0]) if isH else (Ll[i] < q[0]):
                    if sw is None or ((q[0] > sw) if isH else (q[0] < sw)): sw, swB = q[0], q[1]
                    arr.pop(j)
            if sw is not None:
                if P['waitClose']:
                    if isH and (accH is None or sw > accH): accH, accHB = sw, swB
                    if not isH and (accL is None or sw < accL): accL, accLB = sw, swB
                elif P['sweepAny']:
                    if isH: st = put(st, sw, swB, i, -1)
                    else: bt = put(bt, sw, swB, i, 1)
        for t, tg in ((bull, bt), (bear, st)):
            started = False
            if tg is not None:
                lvT = t.d * tg[0]
                if not t.active:
                    t.reset_all(); t.active = True; t.trig = t.made = i; t.level, t.levelBar, t.anchor = lvT, tg[1], tg[2]; started = True
                else:
                    t.trig = i
                    if lvT < t.level: t.level, t.levelBar = lvT, tg[1]
            if t.active:
                n = max(0, min(max(i - t.anchor, 0) + P['pre'], 450, i - 2)) if started else 0
                for k in range(n, -1, -1):
                    bi = i - k; advance(t, bi, bi >= t.anchor)
            if t.active and (i - t.trig > P['wait'] or i - t.made > P['age']): t.active = False
        # ---- trade engine: management
        if tr is not None and i > tr['bar']:
            d = tr['dir']; eSL = tr['sl']
            slRaw = (Ll[i] <= eSL) if d == 1 else (Hh[i] >= eSL)
            t1Raw = (Hh[i] >= tr['tp1']) if d == 1 else (Ll[i] <= tr['tp1']); t3Raw = (Hh[i] >= tr['tp3']) if d == 1 else (Ll[i] <= tr['tp3'])
            gapSl = (O[i] <= eSL) if d == 1 else (O[i] >= eSL); gapTp = (O[i] >= tr['tp1']) if d == 1 else (O[i] <= tr['tp1'])
            slFirst = slRaw and (gapSl or (P['model'] == 'Conservative' and not gapTp))
            t1First = t1Raw and not tr['hit1'] and not slFirst
            if t1First: tr['hit1'] = True
            if P['be'] and t1First and not tr['be']: tr['sl'] = tr['entry']; tr['be'] = True
            beyond = (C[i] <= eSL) if d == 1 else (C[i] >= eSL)
            t3Close = t3Raw and not slFirst
            bySl = slRaw and not t3Close and (slFirst or not t1First or beyond)
            if t3Close or bySl:
                px = (max(O[i], tr['tp3']) if d == 1 else min(O[i], tr['tp3'])) if t3Close else (min(O[i], eSL) if d == 1 else max(O[i], eSL))
                res.append(dict(p=p, d=d, t=tr['t'], tx=b[i]['tc'], wk=tr['wk'], R=d * (px - tr['entry']) / tr['risk'] - cost / tr['risk'], why='TP3' if t3Close else ('BE' if tr['be'] else 'SL')))
                tr = None
        # pending
        if pend is not None and tr is None and i > pend['bar']:
            d = pend['dir']; touched = (Ll[i] <= pend['en']) if d == 1 else (Hh[i] >= pend['en'])
            t1b = (Hh[i] >= pend['tp1']) if d == 1 else (Ll[i] <= pend['tp1'])
            if i - pend['bar'] > P['pend'] or (P['cancelOut'] and not kz_ok(i)): pend = None
            elif touched:
                fx = min(O[i], pend['en']) if d == 1 else max(O[i], pend['en']); risk = abs(fx - pend['sl'])
                tr = dict(dir=d, entry=fx, sl=pend['sl'], tp1=pend['tp1'], tp3=pend['tp3'], risk=risk, bar=i, hit1=False, be=False, t=b[i]['t'], wk=b[i]['wk'])
                gapStop = d * (fx - pend['sl']) <= 0; stopTouch = (Ll[i] <= pend['sl']) if d == 1 else (Hh[i] >= pend['sl'])
                stopClose = (C[i] <= pend['sl']) if d == 1 else (C[i] >= pend['sl'])
                pend = None
                if gapStop or (stopTouch if P['model'] == 'Conservative' else stopClose):
                    res.append(dict(p=p, d=d, t=b[i]['t'], tx=b[i]['tc'], wk=b[i]['wk'], R=(0 if gapStop else -1) - cost / max(risk, 1e-9), why='SL fill')); tr = None
            elif t1b: pend = None
        # ---- signals
        live = start <= b[i]['t'] < end and A[i] > 0 and i >= 50
        bi_ = B.get((p, b[i]['wk']), ('-',))[0]; engDir = 1 if bi_ == 'U' else -1 if bi_ == 'D' else 0
        tOk = (not P['hours'] or P['hours'][0] <= b[i]['t'].astimezone(BUC).hour < P['hours'][1]) and not (P['noFri'] and dkey(i).weekday() == 4)
        plans = {}
        for t in (bull, bear):
            if not t.active: continue
            if not (live and kz_ok(i) and tOk): continue
            if P['eng'] and engDir != t.d: continue
            ok, e, s = build(t, i)
            if not ok: continue
            pl = plan(t, i, e, s)
            if pl is None: continue
            fresh = tr is not None and tr['dir'] == -t.d and tr['bar'] == i
            pl['acc'] = t.d != (tr['dir'] if tr else 0) and t.d != (pend['dir'] if pend else 0) and not fresh
            plans[t.d] = pl; t.active = False
        if 1 in plans and -1 in plans and plans[1]['acc'] and plans[-1]['acc']: plans[1]['acc'] = plans[-1]['acc'] = False
        sig = next((pl for pl in plans.values() if pl['acc']), None)
        if sig is not None:
            d = sig['dir']
            if tr is not None and tr['dir'] == -d:
                res.append(dict(p=p, d=tr['dir'], t=tr['t'], tx=b[i]['tc'], wk=tr['wk'], R=tr['dir'] * (C[i] - tr['entry']) / tr['risk'] - cost / tr['risk'], why='REV')); tr = None
            if pend is not None and pend['dir'] == -d: pend = None
            if tr is None:
                if sig['mkt']:
                    tr = dict(dir=d, entry=sig['en'], sl=sig['sl'], tp1=sig['tp1'], tp3=sig['tp3'], risk=abs(sig['en'] - sig['sl']), bar=i, hit1=False, be=False, t=b[i]['t'], wk=b[i]['wk'])
                else:
                    pend = dict(dir=d, en=sig['en'], sl=sig['sl'], tp1=sig['tp1'], tp3=sig['tp3'], bar=i)
    return res
