# BE Swing replay, extended: entry/exit/filter variants + portfolio rules, on 4H OHLC exports.
# R per trade is net of a cost of `cost` pips per round trip. Conservative intrabar order: stop first.
import csv, json, os, datetime as D
from zoneinfo import ZoneInfo
NY = ZoneInfo('America/New_York')
HERE = os.path.dirname(os.path.abspath(__file__))
USD = ['EURUSD', 'GBPUSD', 'AUDUSD', 'NZDUSD', 'USDJPY', 'USDCHF', 'USDCAD', 'XAUUSD']

def pip_of(p): return 1.0 if p in ('GER40', 'US30', 'NAS100', 'SPX500', 'UK100') else 0.01 if 'JPY' in p else 0.1 if 'XAU' in p else 0.0001
def cost_of(p): return 1.5 if p in ('GER40', 'US30', 'NAS100', 'SPX500', 'UK100') else 3.0 if 'XAU' in p else 1.0

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
    wko, wk = None, None; ema = None; a = 2 / 21; e144 = e169 = None
    dop, dk, mop, mk, pwh, pwl, cwh, cwl, yop, yk = None, None, None, None, None, None, None, None, None, None
    # daily fractal swing points (2 days each side), usable from the day after confirmation
    ks = sorted(days); sup = {}; res_ = {}; lows = []; highs = []
    for n_, k in enumerate(ks):
        if n_ >= 4:
            m = ks[n_ - 2]; win = ks[n_ - 4:n_ + 1]
            if days[m]['l'] == min(days[x]['l'] for x in win): lows.append((k, days[m]['l']))
            if days[m]['h'] == max(days[x]['h'] for x in win): highs.append((k, days[m]['h']))
        sup[k] = [v for d_, v in lows[-12:]]; res_[k] = [v for d_, v in highs[-12:]]
    for j, b in enumerate(bars):
        if b['wk'] != wk:
            if wk is not None: pwh, pwl = cwh, cwl
            wk = b['wk']; wko = b['o']; cwh, cwl = b['h'], b['l']
        else: cwh, cwl = max(cwh, b['h']), min(cwl, b['l'])
        if b['day'] != dk: dk = b['day']; dop = b['o']
        if (b['day'].year, b['day'].month) != mk: mk = (b['day'].year, b['day'].month); mop = b['o']
        if b['day'].year != yk: yk = b['day'].year; yop = b['o']
        b['yop'] = yop
        b['dop'], b['mop'], b['pwh'], b['pwl'] = dop, mop, pwh, pwl
        b['sups'], b['ress'] = sup[b['day']], res_[b['day']]
        b['sw6l'] = min(x['l'] for x in bars[max(0, j - 6):j]) if j >= 6 else None
        b['sw6h'] = max(x['h'] for x in bars[max(0, j - 6):j]) if j >= 6 else None
        b['wko'] = wko; b['atr'] = atr.get(b['day']); b['sma20'] = sma[b['day']][20]; b['sma50'] = sma[b['day']][50]
        b['ema_prev'] = ema; ema = b['c'] if ema is None else ema + a * (b['c'] - ema); b['ema'] = ema
        e144 = b['c'] if e144 is None else e144 + 2 / 145 * (b['c'] - e144); e169 = b['c'] if e169 is None else e169 + 2 / 170 * (b['c'] - e169)
        b['v1'], b['v2'] = (e144, e169) if j >= 300 else (None, None)
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
           partial=False, be=False, thesis=False, usdcf=False, trlen=20, nomon=False, restx='none', trail=2.0, minwtd=0.0, tsrc='sma20', adx=None, atrp=None, er=None, swsl=False, fri=True, opens='none', vegas='none', pf=0.5, pl=1.0, bemove=True, belock=0.0, cool=24, hours=None, maxwk=0, swdepth=(0, 99), swclose=0.0, swlimit=False, tpmode='R', steps=(), trailm='none', trailk=2.0, trailn=6, trailfrom=0.0, p2=None, p2f=0.25)

def run(pair, bars, B, P, start, end=None, usd=None):
    P = {**DEF, **P}; pip = pip_of(pair); cost = cost_of(pair) * pip
    res, pos, pend, lastx, wk_done = [], None, None, None, set()
    obz, fvz = [], []   # 4H demand/supply zones and fair value gaps: [dir, top, bottom, created_index]
    for i, b in enumerate(bars):
        if i >= 25 and P['entry'] in ('OB', 'FVG', 'OBFVG'):
            body = [abs(x['c'] - x['o']) for x in bars[i - 20:i]]; avg = sum(body) / 20
            for dz in (1, -1):
                if (b['c'] - b['o']) * dz > 1.5 * avg and ((b['c'] > max(x['h'] for x in bars[i - 5:i])) if dz > 0 else (b['c'] < min(x['l'] for x in bars[i - 5:i]))):
                    for j in range(i - 1, i - 4, -1):
                        x = bars[j]
                        if (x['c'] - x['o']) * dz < 0:
                            obz.append([dz, x['o'] if dz > 0 else x['h'], x['l'] if dz > 0 else x['o'], i]); break
            if b['l'] > bars[i - 2]['h']: fvz.append([1, b['l'], bars[i - 2]['h'], i])
            if b['h'] < bars[i - 2]['l']: fvz.append([-1, bars[i - 2]['l'], b['h'], i])
            # zones die when price closes through them; old ones expire after 5 days
            obz = [z for z in obz if i - z[3] < 30 and not ((b['c'] < z[2]) if z[0] > 0 else (b['c'] > z[1]))]
            fvz = [z for z in fvz if i - z[3] < 30 and not ((b['l'] <= z[2]) if z[0] > 0 else (b['h'] >= z[1]))]
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
            elif P.get('fillhrs') and b['hl'] not in P['fillhrs']: pass      # outside the trader's hours: the order waits (or expires)
            elif (pend.get('stop') and (b['h'] >= pend['e'] if pend['d'] > 0 else b['l'] <= pend['e'])) or (not pend.get('stop') and (b['l'] <= pend['e'] if pend['d'] > 0 else b['h'] >= pend['e'])):
                pos = dict(i=i, t=b['t'], d=pend['d'], e=pend['e'], risk=pend['risk'], sl=pend['e'] - pend['d'] * pend['risk'], w=1.0, banked=0.0, part=False, meta=pend['meta'])
                pos['tp'] = pos['e'] + pos['d'] * P['tp'] * pos['risk'] if P['tp'] else None
                if P['tpmode'] != 'R':
                    lvl = {'pdh': b['pdh'] if pos['d'] > 0 else b['pdl'], 'pwh': b['pwh'] if pos['d'] > 0 else b['pwl']}[P['tpmode']]
                    if lvl is not None and (lvl - pos['e']) * pos['d'] >= 1.0 * pos['risk']: pos['tp'] = lvl
                pend = None
                if P.get('fillchk') and ((b['l'] <= pos['sl']) if pos['d'] > 0 else (b['h'] >= pos['sl'])):
                    # worst case: the stop is touched on the same candle that filled the entry
                    res.append(dict(pair=pair, t=b['t'], tx=b['tc'], d=pos['d'], R=-1 - cost / pos['risk'], why='SL same bar', mfe=0.0, **pos['meta'])); pos = None; lastx = b['tc']
        # manage the open position from the bar after entry
        if pos and i > pos['i']:
            d = pos['d']; R = lambda px: (px - pos['e']) * d / pos['risk']
            ex = None
            if (b['l'] <= pos['sl']) if d > 0 else (b['h'] >= pos['sl']):
                gap = (b['o'] < pos['sl']) if d > 0 else (b['o'] > pos['sl'])
                ex = (b['o'] if gap else pos['sl'], 'SL')
            else:
                pl = P['pl']
                hit1R = (b['h'] >= pos['e'] + pl * pos['risk']) if d > 0 else (b['l'] <= pos['e'] - pl * pos['risk'])
                if P['partial'] and not pos['part'] and hit1R:
                    pos['banked'] += P['pf'] * pl; pos['w'] = 1 - P['pf']; pos['part'] = True
                    pos['sl'] = pos['e'] + d * P['belock'] * pos['risk'] if P['bemove'] else pos['sl']
                if P['be'] and not pos['part'] and hit1R: pos['sl'] = pos['e']; pos['part'] = True
                ext = b['h'] if d > 0 else b['l']
                pos['best'] = max(pos.get('best', 0.0), R(ext))
                if P['p2'] and pos['part'] and not pos.get('p2') and pos['best'] >= P['p2'][0]:
                    pos['banked'] += P['p2f'] * P['p2'][0]; pos['w'] -= P['p2f']; pos['p2'] = True
                    pos['sl'] = pos['e'] + d * P['p2'][1] * pos['risk'] if (pos['sl'] - (pos['e'] + d * P['p2'][1] * pos['risk'])) * d < 0 else pos['sl']
                for trg, lock in P['steps']:
                    if pos['best'] >= trg:
                        ns = pos['e'] + d * lock * pos['risk']; pos['sl'] = max(pos['sl'], ns) if d > 0 else min(pos['sl'], ns)
                if P['trailm'] != 'none' and pos['best'] >= P['trailfrom']:
                    A = b['atr4'] if P.get('atrsrc') == '4h' else b['atr']
                    if P['trailm'] == 'chand': ns = pos['e'] + d * (pos['best'] * pos['risk']) - d * P['trailk'] * A
                    elif P['trailm'] == 'close':
                        k_ = P.get('trailk2', P['trailk']) if pos['best'] >= P.get('trailat', 99) else P['trailk']
                        ns = b['c'] - d * k_ * A
                    elif P['trailm'] == 'nbar':
                        win = bars[max(pos['i'] + 1, i - P['trailn'] + 1):i + 1]
                        ns = min(x['l'] for x in win) if d > 0 else max(x['h'] for x in win)
                    elif P['trailm'] == 'pday': ns = b['pdl'] if d > 0 else b['pdh']
                    if ns is not None: pos['sl'] = max(pos['sl'], ns) if d > 0 else min(pos['sl'], ns)
                if pos['part'] and P['restx'] == 'trail':
                    ns = b['c'] - d * P['trail'] * b['atr']; pos['sl'] = max(pos['sl'], ns) if d > 0 else min(pos['sl'], ns)
                if pos['tp'] is not None and ((b['h'] >= pos['tp']) if d > 0 else (b['l'] <= pos['tp'])): ex = (pos['tp'], 'TP')
                else:
                    lastbar = b['dow'] == 4 and (i + 1 == len(bars) or bars[i + 1]['day'] != b['day'])
                    held = (b['tc'] - pos['t']).total_seconds() / 86400
                    if lastbar and P['fri']: ex = (b['c'], 'Fri')
                    elif P['hold'] != 'fri' and held >= P['hold']: ex = (b['c'], 'Time')
                    elif pos['part'] and P['restx'] == 'ema20' and (b['c'] - b['ema']) * d < 0: ex = (b['c'], 'EMA20')
                    elif pos['part'] and P['restx'] == 'prevday' and b['pdl'] is not None and ((b['c'] < b['pdl']) if d > 0 else (b['c'] > b['pdh'])): ex = (b['c'], 'PrevDay')
                    elif P['thesis'] and (b['c'] - b['wko']) * d < 0 and b['wk'] == bars[pos['i']]['wk']: ex = (b['c'], 'Thesis')
                    elif dr == -d: ex = (b['c'], 'Flip')
            if ex:
                r = pos['banked'] + pos['w'] * R(ex[0]) - cost / pos['risk']
                res.append(dict(pair=pair, t=pos['t'], tx=b['tc'], d=d, R=r, why=ex[1], mfe=pos.get('best', 0.0), **pos['meta'])); pos = None; lastx = b['tc']
            continue
        if pos or pend: continue
        if b['t'] < start or (end and b['t'] >= end): continue
        if lastx and (b['tc'] - lastx).total_seconds() < P['cool'] * 3600: continue
        if P['hours'] and not (P['hours'][0] <= b['hl'] < P['hours'][1]): continue
        if P['maxwk'] and sum(1 for x in res if x['pair'] == pair and x['wk'] == b['wk']) >= P['maxwk']: continue
        if b['atr'] is None or dr == 0 or b['dow'] > P.get('maxdow', 3): continue          # Mon–Thu (trading day), no Friday entries
        if P['nomon'] and b['dow'] == 0: continue
        if P['vegas'] != 'none':
            if b['v1'] is None: continue
            hi, lo = max(b['v1'], b['v2']), min(b['v1'], b['v2'])
            if P['vegas'] == 'side' and not ((b['c'] > hi) if dr > 0 else (b['c'] < lo)): continue          # price on the trade's side of the tunnel
            if P['vegas'] == 'slope' and not ((b['v1'] > b['v2']) if dr > 0 else (b['v1'] < b['v2'])): continue  # EMA144 above EMA169 for longs
            if P['vegas'] == 'both' and not (((b['c'] > hi) and b['v1'] > b['v2']) if dr > 0 else ((b['c'] < lo) and b['v1'] < b['v2'])): continue
            if P['vegas'] == 'near' and not (0 <= ((b['l'] - hi) if dr > 0 else (lo - b['h'])) <= 0.5 * b['atr'] or (lo <= (b['l'] if dr > 0 else b['h']) <= hi)): continue  # candle touches / near the tunnel
        if P['opens'] != 'none':
            lv = {'w': [b['wko']], 'm': [b['mop']], 'y': [b['yop']], 'wm': [b['wko'], b['mop']], 'wmy': [b['wko'], b['mop'], b['yop']], 'my': [b['mop'], b['yop']]}[P['opens']]
            if any(v is None or (b['c'] - v) * dr <= 0 for v in lv): continue
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
        risk = P['k'] * (b['atr4'] if P.get('atrsrc') == '4h' else b['atr'])
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
        elif P['entry'] in ('PDL', 'WO', 'DO', 'MO', 'PWL'):
            # limit order at a level on the trade's side: yesterday's low/high, week open, day open, month open, last week's low/high
            lv = {'PDL': b['pdl'] if dr > 0 else b['pdh'], 'WO': b['wko'], 'DO': b['dop'], 'MO': b['mop'], 'PWL': b['pwl'] if dr > 0 else b['pwh']}[P['entry']]
            life = {'PDL': 24, 'WO': 120, 'DO': 24, 'MO': 120, 'PWL': 120}[P['entry']]
            if lv is not None and (b['c'] - lv) * dr > 0: pend = dict(t0=b['tc'], wk=b['wk'], d=dr, e=lv, risk=risk, life=life, meta=meta)
            else: wk_done.discard((pair, b['wk']))
        elif P['entry'] in ('SD', 'SWO'):
            # combination: a sweep of yesterday's low/high enters at once; otherwise a pending order (D: break of yesterday, WO: week open)
            lv = b['pdl'] if dr > 0 else b['pdh']
            if lv is not None and ((b['l'] < lv < b['c']) if dr > 0 else (b['h'] > lv > b['c'])):
                pos = dict(i=i, t=b['tc'], d=dr, e=b['c'], risk=risk, sl=b['c'] - dr * risk, w=1.0, banked=0.0, part=False, meta={**meta, 'how': 'sweep'})
                pos['tp'] = pos['e'] + dr * P['tp'] * risk if P['tp'] else None
            elif P['entry'] == 'SD' and b['pdh'] is not None and ((b['pdh'] if dr > 0 else b['pdl']) - b['c']) * dr > 0:
                pend = dict(t0=b['tc'], wk=b['wk'], d=dr, e=b['pdh'] if dr > 0 else b['pdl'], risk=risk, life=4, meta={**meta, 'how': 'break'}, stop=True)
            elif P['entry'] == 'SWO' and (b['c'] - b['wko']) * dr > 0:
                pend = dict(t0=b['tc'], wk=b['wk'], d=dr, e=b['wko'], risk=risk, life=4, meta={**meta, 'how': 'week open'})
            else: wk_done.discard((pair, b['wk']))
        elif P['entry'] in ('SWP', 'SW6', 'SWW'):
            # liquidity sweep and reclaim in the trade's direction: the candle trades through the level and closes back on the right side
            lv = {'SWP': b['pdl'] if dr > 0 else b['pdh'], 'SW6': b['sw6l'] if dr > 0 else b['sw6h'], 'SWW': b['pwl'] if dr > 0 else b['pwh']}[P['entry']]
            ok = lv is not None and ((b['l'] < lv < b['c']) if dr > 0 else (b['h'] > lv > b['c']))
            if ok:
                depth = ((lv - b['l']) if dr > 0 else (b['h'] - lv)) / b['atr']
                rng = b['h'] - b['l']; clp = ((b['c'] - b['l']) if dr > 0 else (b['h'] - b['c'])) / rng if rng > 0 else 0
                ok = P['swdepth'][0] <= depth <= P['swdepth'][1] and clp >= P['swclose']
                meta = {**meta, 'depth': depth, 'clp': clp}
            if ok and P['swlimit']:
                ext = b['l'] if dr > 0 else b['h']
                pend = dict(t0=b['tc'], wk=b['wk'], d=dr, e=(b['c'] + ext) / 2, risk=risk, life=8, meta=meta)
            elif ok:
                ext = b['l'] if dr > 0 else b['h']
                rk = max(abs(b['c'] - ext) + 0.1 * b['atr'], 0.3 * b['atr']) if P['swsl'] else risk
                pos = dict(i=i, t=b['tc'], d=dr, e=b['c'], risk=rk, sl=b['c'] - dr * rk, w=1.0, banked=0.0, part=False, meta=meta)
                pos['tp'] = pos['e'] + dr * P['tp'] * rk if P['tp'] else None
                if P['tpmode'] != 'R':
                    lvl = {'pdh': b['pdh'] if dr > 0 else b['pdl'], 'pwh': b['pwh'] if dr > 0 else b['pwl']}[P['tpmode']]
                    pos['tp'] = lvl if lvl is not None and (lvl - b['c']) * dr >= 1.0 * rk else (pos['e'] + dr * max(P['tp'] or 2, 1) * rk)
            else: wk_done.discard((pair, b['wk']))
        elif P['entry'] in ('SR', 'SRS', 'YO'):
            if P['entry'] == 'YO': cands = [b['yop']]
            else: cands = [v for v in (b['sups'] if dr > 0 else b['ress'])]
            cands = [v for v in cands if v is not None and 0 < (b['c'] - v) * dr <= 1.5 * b['atr']]
            if not cands: wk_done.discard((pair, b['wk']))
            else:
                lv = max(cands) if dr > 0 else min(cands)
                if P['entry'] == 'SRS':
                    # sweep of the nearest support/resistance on this candle, close back on the right side
                    near = [v for v in (b['sups'] if dr > 0 else b['ress']) if v is not None and ((b['l'] < v < b['c']) if dr > 0 else (b['h'] > v > b['c']))]
                    if near:
                        pos = dict(i=i, t=b['tc'], d=dr, e=b['c'], risk=risk, sl=b['c'] - dr * risk, w=1.0, banked=0.0, part=False, meta=meta)
                        pos['tp'] = pos['e'] + dr * P['tp'] * risk if P['tp'] else None
                    else: wk_done.discard((pair, b['wk']))
                else: pend = dict(t0=b['tc'], wk=b['wk'], d=dr, e=lv, risk=risk, life=48 if P['entry'] == 'SR' else 120, meta=meta)
        elif P['entry'] in ('OB', 'FVG', 'OBFVG'):
            src = obz if P['entry'] == 'OB' else fvz if P['entry'] == 'FVG' else [z for z in obz if any(f_[0] == z[0] and f_[2] <= z[1] and f_[1] >= z[2] for f_ in fvz)]
            zs = [z for z in src if z[0] == dr and 0 < (b['c'] - (z[1] if dr > 0 else z[2])) * dr <= 2 * b['atr']]
            if zs:
                z = max(zs, key=lambda z: z[3]); e = z[1] if dr > 0 else z[2]
                pend = dict(t0=b['tc'], wk=b['wk'], d=dr, e=e, risk=risk, life=48, meta=meta)
            else: wk_done.discard((pair, b['wk']))
        elif P['entry'] == 'VT' and b['v1'] is not None:
            # limit at the tunnel edge on the trade's side (support for longs, resistance for shorts)
            e = max(b['v1'], b['v2']) if dr > 0 else min(b['v1'], b['v2'])
            if (b['c'] - e) * dr > 0: pend = dict(t0=b['tc'], wk=b['wk'], d=dr, e=e, risk=risk, life=24, meta=meta)
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
        elif P['entry'] == 'C':
            # stop order one tick beyond this candle's high (long) / low (short), alive for the next candle only
            pend = dict(t0=b['tc'], wk=b['wk'], d=dr, e=b['h'] if dr > 0 else b['l'], risk=risk, life=1, meta=meta, stop=True)
        elif P['entry'] in ('CB', 'CD', 'PB', 'C2', 'CE', 'AR'):
            A4 = b['atr4'] if P.get('atrsrc') == '4h' else b['atr']
            ok, e, life = True, (b['h'] if dr > 0 else b['l']), 1
            if P['entry'] == 'CB': e = e + dr * P.get('cbuf', 0.1) * A4                       # break with a buffer
            elif P['entry'] == 'CD': ok = (b['c'] - b['o']) * dr > 0                            # signal candle closed in the trade's direction
            elif P['entry'] == 'PB': ok = (b['c'] - b['o']) * dr < 0                            # signal candle is a pullback; break of its high/low
            elif P['entry'] == 'C2': e = max(b['h'], bars[i - 1]['h']) if dr > 0 else min(b['l'], bars[i - 1]['l'])   # break of the last two candles
            elif P['entry'] == 'CE': ok = b['ema'] is not None and (b['c'] - b['ema']) * dr > 0  # 4H close on the trade's side of the 4H EMA20
            elif P['entry'] == 'AR':                                                            # Asian range (00-08 Bucharest) broken in London/NY until 16:00
                ok = b['hl'] == 4 and bars[i - 1]['day'] == b['day']
                if ok: e = max(b['h'], bars[i - 1]['h']) if dr > 0 else min(b['l'], bars[i - 1]['l']); life = 8
            if ok: pend = dict(t0=b['tc'], wk=b['wk'], d=dr, e=e, risk=risk, life=life, meta=meta, stop=True)
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
