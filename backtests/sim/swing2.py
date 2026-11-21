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
    trs, cl, prev, atr, sma = [], [], None, {}, {}
    for k in sorted(days):
        atr[k] = sum(trs[-14:]) / 14 if len(trs) >= 14 else None
        sma[k] = {n: (sum(cl[-n:]) / n if len(cl) >= n else None) for n in (20, 50)}
        d = days[k]; trs.append(d['h'] - d['l'] if prev is None else max(d['h'], prev) - min(d['l'], prev)); cl.append(d['c']); prev = d['c']
    wko, wk = None, None; ema = None; a = 2 / 21
    for b in bars:
        if b['wk'] != wk: wk = b['wk']; wko = b['o']
        b['wko'] = wko; b['atr'] = atr.get(b['day']); b['sma20'] = sma[b['day']][20]; b['sma50'] = sma[b['day']][50]
        b['ema_prev'] = ema; ema = b['c'] if ema is None else ema + a * (b['c'] - ema)
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
           partial=False, be=False, thesis=False, usdcf=False, trlen=20)

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
        s = b['sma20'] if P['trlen'] == 20 else b['sma50']
        td = 0 if s is None else (1 if b['c'] > s else -1)
        dr = bd if P['dirm'] == 'bias' else td if P['dirm'] == 'trend' else (bd if bd == td else 0)
        # pending limit order (entry B / E) fills on this bar?
        if pend and pos is None:
            if (b['t'] - pend['t0']).total_seconds() > pend['life'] * 3600 or b['wk'] != pend['wk']: pend = None
            elif (b['l'] <= pend['e'] if pend['d'] > 0 else b['h'] >= pend['e']):
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
                if pos['tp'] is not None and ((b['h'] >= pos['tp']) if d > 0 else (b['l'] <= pos['tp'])): ex = (pos['tp'], 'TP')
                else:
                    lastbar = b['dow'] == 4 and (i + 1 == len(bars) or bars[i + 1]['day'] != b['day'])
                    held = (b['tc'] - pos['t']).total_seconds() / 86400
                    if lastbar: ex = (b['c'], 'Fri')
                    elif P['hold'] != 'fri' and held >= P['hold']: ex = (b['c'], 'Time')
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
        if P['sess'] and not (8 <= b['hl'] < 20): continue                # candle opening 08:00–19:59 Bucharest
        if P['first'] and (pair, b['wk']) in wk_done: continue
        wtd = (b['c'] - b['wko']) * dr
        if P['cf'] == 'wtd' and wtd <= 0: continue
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
        elif P['entry'] == 'E' and b['ema_prev'] is not None:
            e = b['ema_prev']
            if (b['c'] - e) * dr > 0: pend = dict(t0=b['tc'], wk=b['wk'], d=dr, e=e, risk=risk, life=24, meta=meta)
    return res

def portfolio(trades, cap=None, topn=None, B=None):
    # cap: max open trades at once across the list; topn: per week keep only the N pairs with the largest |gap|
    tr = sorted(trades, key=lambda x: x['t'])
    if topn:
        by = {}
        for x in tr:
            if x['gap'] is not None: by.setdefault(x['wk'], set()).add((abs(x['gap']), x['pair']))
        keep = {w: {p for _, p in sorted(v, reverse=True)[:topn]} for w, v in by.items()}
        tr = [x for x in tr if x['pair'] in keep.get(x['wk'], set())]
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
