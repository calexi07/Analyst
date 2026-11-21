# BE Swing replay, extended: entry/exit/filter variants + portfolio rules, on 4H OHLC exports.
# R per trade is net of a cost of `cost` pips per round trip. Conservative intrabar order: stop first.
import csv, json, os, datetime as D
from zoneinfo import ZoneInfo
NY = ZoneInfo('America/New_York')
HERE = os.path.dirname(os.path.abspath(__file__))
USD = ['EURUSD', 'GBPUSD', 'AUDUSD', 'NZDUSD', 'USDJPY', 'USDCHF', 'USDCAD', 'XAUUSD']

def pip_of(p): return 0.01 if 'JPY' in p else 0.1 if 'XAU' in p else 0.0001
def cost_of(p): return 3.0 if 'XAU' in p else 1.0

def load(pair):
    bars = []
    for r in csv.DictReader(open(os.path.join(HERE, f'../ohlc/FOREXCOM_{pair}_240.csv'))):
        t = D.datetime.fromisoformat(r['time']).astimezone(D.timezone.utc)
        bars.append(dict(t=t, o=float(r['open']), h=float(r['high']), l=float(r['low']), c=float(r['close'])))
    bars.sort(key=lambda b: b['t'])
    for b in bars:
        ny = (b['t'] + D.timedelta(hours=7)).astimezone(NY)
        b['day'] = ny.date(); b['dow'] = ny.weekday(); b['wk'] = ny.date().isocalendar()[:2]
        b['tc'] = b['t'] + D.timedelta(hours=4)
        b['hl'] = b['t'].astimezone(ZoneInfo('Europe/Bucharest')).hour
    # daily values known at the start of each day (previous completed days only)
    days = {}
    for b in bars:
        d = days.setdefault(b['day'], dict(h=b['h'], l=b['l'], c=b['c']))
        d['h'] = max(d['h'], b['h']); d['l'] = min(d['l'], b['l']); d['c'] = b['c']
    trs, cl, prev, atr, sma, pdhl, last = [], [], None, {}, {}, {}, None
    feat, atrh, hs, ls, W, DX, adx_v, ph, pl, sTR, sP, sN = {}, [], [], [], [], [], None, None, None, 0, 0, 0
    for k in sorted(days):
        pdhl[k] = (days[last]['h'], days[last]['l']) if last else (None, None); last = k
        atr[k] = sum(trs[-14:]) / 14 if len(trs) >= 14 else None
        sma[k] = {n: (sum(cl[-n:]) / n if len(cl) >= n else None) for n in (20, 50)}
        feat[k] = dict(
            sma100=sum(cl[-100:]) / 100 if len(cl) >= 100 else None, sma200=sum(cl[-200:]) / 200 if len(cl) >= 200 else None,
            ret60=(cl[-1] / cl[-61] - 1) if len(cl) >= 61 else None, ret20=(cl[-1] / cl[-21] - 1) if len(cl) >= 21 else None,
            adx=adx_v, atrp=(sum(1 for x in atrh[-100:] if x <= atr[k]) / len(atrh[-100:]) if atr[k] and len(atrh) >= 50 else None),
            dch=max(hs[-20:]) if len(hs) >= 20 else None, dcl=min(ls[-20:]) if len(ls) >= 20 else None,
            er=(abs(cl[-1] - cl[-21]) / sum(abs(cl[i] - cl[i - 1]) for i in range(len(cl) - 20, len(cl)))) if len(cl) >= 22 else None,
            lastc=cl[-1] if cl else None)
        if atr[k]: atrh.append(atr[k])
        d = days[k]
        if prev is not None:
            up = d['h'] - ph; dn = pl - d['l']; pdm = up if up > dn and up > 0 else 0; ndm = dn if dn > up and dn > 0 else 0
            tr_ = max(d['h'], prev) - min(d['l'], prev); W.append((tr_, pdm, ndm))
            if len(W) == 14: sTR, sP, sN = (sum(x[i] for x in W) for i in range(3))
            elif len(W) > 14: sTR = sTR - sTR / 14 + tr_; sP = sP - sP / 14 + pdm; sN = sN - sN / 14 + ndm
            if len(W) >= 14 and sTR > 0:
                pdi, ndi = 100 * sP / sTR, 100 * sN / sTR; dx = 100 * abs(pdi - ndi) / (pdi + ndi) if pdi + ndi else 0
                DX.append(dx); adx_v = sum(DX[-14:]) / len(DX[-14:]) if len(DX) >= 14 else None
        ph, pl = d['h'], d['l']; hs.append(d['h']); ls.append(d['l'])
        trs.append(d['h'] - d['l'] if prev is None else max(d['h'], prev) - min(d['l'], prev)); cl.append(d['c']); prev = d['c']
    wko, wk = None, None; ema = None; a = 2 / 21
    for b in bars:
        if b['wk'] != wk: wk = b['wk']; wko = b['o']
        b['wko'] = wko; b['atr'] = atr.get(b['day']); b['sma20'] = sma[b['day']][20]; b['sma50'] = sma[b['day']][50]
        b['ema_prev'] = ema; ema = b['c'] if ema is None else ema + a * (b['c'] - ema); b['ema'] = ema
        b['pdh'], b['pdl'] = pdhl[b['day']]; b['f'] = feat[b['day']]
    return bars

def bias_table():
    h = json.load(open(os.path.join(HERE, '../../pine/history.json')))
    out = {}
    for W in h['weeks']:
        for p, x in W['pairs'].items():
            g = (x['bs'] - x['qs']) if x.get('bs') is not None and x.get('qs') is not None else None
            out[(p, (W['y'], W['w']))] = (x['b'], x['c'], g)
    return out

def usd_strength(data):
    # week-to-date USD strength at each bar time: average of sign-adjusted (USD up = +) WTD % moves of the fiat USD pairs
    acc = {}
    for p, bars in data.items():
        if p == 'XAUUSD' or p not in USD: continue
        s = 1 if p.startswith('USD') else -1
        for b in bars: acc.setdefault(b['t'], []).append(s * (b['c'] / b['wko'] - 1))
    return {t: sum(v) / len(v) for t, v in acc.items() if len(v) >= 4}

DEF = dict(dirm='bias', cf='wtd', k=1.0, tp=2.0, hold=4, entry='A', sess=False, first=False, exh=None, conv='any', mingap=None,
           partial=False, be=False, thesis=False, usdcf=False, trlen=20, nomon=False, restx='none', trail=2.0, minwtd=0.0, tsrc='sma20', adx=None, atrp=None, er=None)

def run(pair, bars, B, P, start, end=None, usd=None):
    P = {**DEF, **P}; pip = pip_of(pair); cost = cost_of(pair) * pip
    res, pos, pend, lastx, wk_done = [], None, None, None, set()
    for i, b in enumerate(bars):
        if b['t'] < start or (end and b['t'] >= end):
            if pos is None and pend is None: continue
        bi = B.get((pair, b['wk']), ('-', '-', None))
        bd = 1 if bi[0] == 'U' else -1 if bi[0] == 'D' else 0
        if P['conv'] == 'mh' and bi[1] not in ('m', 'h'): bd = 0
        if P['mingap'] is not None and (bi[2] is None or abs(bi[2]) < P['mingap']): bd = 0
        f = b['f']; ts = P['tsrc'] if P['trlen'] == 20 else 'sma50'
        if ts in ('sma20', 'sma50', 'sma100', 'sma200'):
            s = b['sma20'] if ts == 'sma20' else b['sma50'] if ts == 'sma50' else f[ts]
            td = 0 if s is None else (1 if b['c'] > s else -1)
        elif ts in ('ret20', 'ret60'):
            td = 0 if f[ts] is None else (1 if f[ts] > 0 else -1)
        elif ts == 'dual':
            a1, a2 = b['sma50'], f['sma200']
            td = 0 if a1 is None or a2 is None else (1 if b['c'] > a1 > a2 else -1 if b['c'] < a1 < a2 else 0)
        dr = bd if P['dirm'] == 'bias' else td if P['dirm'] == 'trend' else (bd if bd == td else 0)
        # pending limit order (entry B / E) fills on this bar?
        if pend and pos is None:
            if (b['t'] - pend['t0']).total_seconds() > pend['life'] * 3600 or b['wk'] != pend['wk']: pend = None
            elif (pend.get('stop') and (b['h'] >= pend['e'] if pend['d'] > 0 else b['l'] <= pend['e'])) or (not pend.get('stop') and (b['l'] <= pend['e'] if pend['d'] > 0 else b['h'] >= pend['e'])):
                pos = dict(i=i, t=b['t'], d=pend['d'], e=pend['e'], risk=pend['risk'], sl=pend['e'] - pend['d'] * pend['risk'], w=1.0, banked=0.0, part=False, meta=pend['meta'])
                pos['tp'] = pos['e'] + pos['d'] * P['tp'] * pos['risk'] if P['tp'] else None
                pend = None
        # manage the open position from the bar after entry
        if pos and i > pos['i']:
            d = pos['d']; R = lambda px: (px - pos['e']) * d / pos['risk']
            ex = None
            if (b['l'] <= pos['sl']) if d > 0 else (b['h'] >= pos['sl']): ex = (pos['sl'], 'SL')
            else:
                hit1R = (b['h'] >= pos['e'] + pos['risk']) if d > 0 else (b['l'] <= pos['e'] - pos['risk'])
                if P['partial'] and not pos['part'] and hit1R:
                    pos['banked'] += 0.5 * 1.0; pos['w'] = 0.5; pos['part'] = True; pos['sl'] = pos['e']
                if P['be'] and not pos['part'] and hit1R: pos['sl'] = pos['e']; pos['part'] = True
                if pos['part'] and P['restx'] == 'trail':
                    ns = b['c'] - d * P['trail'] * b['atr']; pos['sl'] = max(pos['sl'], ns) if d > 0 else min(pos['sl'], ns)
                if pos['tp'] is not None and ((b['h'] >= pos['tp']) if d > 0 else (b['l'] <= pos['tp'])): ex = (pos['tp'], 'TP')
                else:
                    lastbar = b['dow'] == 4 and (i + 1 == len(bars) or bars[i + 1]['day'] != b['day'])
                    held = (b['tc'] - pos['t']).total_seconds() / 86400
                    if lastbar: ex = (b['c'], 'Fri')
                    elif P['hold'] != 'fri' and held >= P['hold']: ex = (b['c'], 'Time')
                    elif pos['part'] and P['restx'] == 'ema20' and (b['c'] - b['ema']) * d < 0: ex = (b['c'], 'EMA20')
                    elif pos['part'] and P['restx'] == 'prevday' and b['pdl'] is not None and ((b['c'] < b['pdl']) if d > 0 else (b['c'] > b['pdh'])): ex = (b['c'], 'PrevDay')
                    elif P['thesis'] and (b['c'] - b['wko']) * d < 0 and b['wk'] == bars[pos['i']]['wk']: ex = (b['c'], 'Thesis')
                    elif dr == -d: ex = (b['c'], 'Flip')
            if ex:
                r = pos['banked'] + pos['w'] * R(ex[0]) - cost / pos['risk']
                res.append(dict(pair=pair, t=pos['t'], tx=b['tc'], d=d, R=r, why=ex[1], **pos['meta'])); pos = None; lastx = b['tc']
            continue
        if pos or pend: continue
        if b['t'] < start or (end and b['t'] >= end): continue
        if lastx and (b['tc'] - lastx).total_seconds() < 24 * 3600: continue
        if b['atr'] is None or dr == 0 or b['dow'] > 3: continue          # Mon–Thu (trading day), no Friday entries
        if P['nomon'] and b['dow'] == 0: continue
        if P['adx'] is not None and (b['f']['adx'] is None or b['f']['adx'] < P['adx']): continue
        if P['atrp'] is not None and (b['f']['atrp'] is None or not (P['atrp'][0] <= b['f']['atrp'] <= P['atrp'][1])): continue
        if P['er'] is not None and (b['f']['er'] is None or b['f']['er'] < P['er']): continue
        if P['sess'] and not (8 <= b['hl'] < 20): continue                # candle opening 08:00–19:59 Bucharest
        if P['first'] and (pair, b['wk']) in wk_done: continue
        wtd = (b['c'] - b['wko']) * dr
        if P['cf'] == 'wtd' and wtd <= P['minwtd'] * b['atr']: continue
        if P['exh'] is not None and wtd > P['exh'] * b['atr']: continue
        if P['usdcf'] and pair != 'XAUUSD':
            u = (usd or {}).get(b['t'])
            usd_dir = dr if pair.startswith('USD') else -dr
            if u is None or u * usd_dir <= 0: continue
        risk = P['k'] * b['atr']
        meta = dict(bias=bi[0], conv=bi[1], gap=bi[2], wk=b['wk'])
        wk_done.add((pair, b['wk']))
        if P['entry'] == 'A':
            pos = dict(i=i, t=b['tc'], d=dr, e=b['c'], risk=risk, sl=b['c'] - dr * risk, w=1.0, banked=0.0, part=False, meta=meta)
            pos['tp'] = pos['e'] + dr * P['tp'] * risk if P['tp'] else None
        elif P['entry'] == 'B':
            pend = dict(t0=b['tc'], wk=b['wk'], d=dr, e=(b['h'] + b['l']) / 2, risk=risk, life=4, meta=meta)
        elif P['entry'] == 'D' and b['pdh'] is not None:
            e = b['pdh'] if dr > 0 else b['pdl']
            if (e - b['c']) * dr > 0: pend = dict(t0=b['tc'], wk=b['wk'], d=dr, e=e, risk=risk, life=24, meta=meta, stop=True)
            else: wk_done.discard((pair, b['wk']))
        elif P['entry'] == 'DC' and b['f']['dch'] is not None:
            e = b['f']['dch'] if dr > 0 else b['f']['dcl']
            if (e - b['c']) * dr > 0: pend = dict(t0=b['tc'], wk=b['wk'], d=dr, e=e, risk=risk, life=24, meta=meta, stop=True)
            else: wk_done.discard((pair, b['wk']))
        elif P['entry'] == 'P':
            # pullback then resumption: the previous candle closed against the direction, this one closes beyond its high/low
            pb = bars[i - 1]
            if (pb['c'] - pb['o']) * dr < 0 and ((b['c'] > pb['h']) if dr > 0 else (b['c'] < pb['l'])):
                pos = dict(i=i, t=b['tc'], d=dr, e=b['c'], risk=risk, sl=b['c'] - dr * risk, w=1.0, banked=0.0, part=False, meta=meta)
                pos['tp'] = pos['e'] + dr * P['tp'] * risk if P['tp'] else None
            else: wk_done.discard((pair, b['wk']))
        elif P['entry'] == 'E' and b['ema_prev'] is not None:
            e = b['ema_prev']
            if (b['c'] - e) * dr > 0: pend = dict(t0=b['tc'], wk=b['wk'], d=dr, e=e, risk=risk, life=24, meta=meta)
    return res

def portfolio(trades, cap=None, topn=None, B=None, wkstop=None):
    # cap: max open trades at once across the list; topn: per week keep only the N pairs with the largest |gap|
    tr = sorted(trades, key=lambda x: x['t'])
    if topn:
        by = {}
        for x in tr:
            if x['gap'] is not None: by.setdefault(x['wk'], set()).add((abs(x['gap']), x['pair']))
        keep = {w: {p for _, p in sorted(v, reverse=True)[:topn]} for w, v in by.items()}
        tr = [x for x in tr if x['pair'] in keep.get(x['wk'], set())]
    if wkstop is not None:
        out = []
        for x in tr:
            closed = sum(y['R'] for y in out if y['wk'] == x['wk'] and y['tx'] <= x['t'])
            if closed > -wkstop: out.append(x)
        tr = out
    if cap:
        out, open_ = [], []
        for x in tr:
            open_ = [y for y in open_ if y['tx'] > x['t']]
            if len(open_) < cap: out.append(x); open_.append(x)
        tr = out
    return tr

def summ(v):
    n = len(v); s = sum(x['R'] for x in v)
    return dict(n=n, R=round(s, 1), exp=round(s / n, 2) if n else 0, win=round(sum(x['R'] > 0 for x in v) / n, 2) if n else 0)
