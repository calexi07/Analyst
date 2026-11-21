# Multi-timeframe BE Swing: the 4H chart finds the setup (sweep of yesterday's low/high + reclaim, in the bias direction),
# the 1H chart refines the entry and/or manages the exit. Usage: python3 backtests/sim/mtf.py EURUSD [EURUSD ...]
import sys, os, csv, datetime as D, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from swing2 import *
HERE = os.path.dirname(os.path.abspath(__file__))

def load1h(pair):
    out = []
    for r in csv.DictReader(open(os.path.join(HERE, f'../ohlc/FOREXCOM_{pair}_60.csv'))):
        t = D.datetime.fromisoformat(r['time']).astimezone(D.timezone.utc)
        b = dict(t=t, tc=t + D.timedelta(hours=1), o=float(r['open']), h=float(r['high']), l=float(r['low']), c=float(r['close']))
        ny = (t + D.timedelta(hours=7)).astimezone(NY); b['day'] = ny.date(); b['dow'] = ny.weekday(); b['wk'] = ny.date().isocalendar()[:2]
        out.append(b)
    out.sort(key=lambda b: b['t'])
    for i, b in enumerate(out): b['last_of_day'] = i + 1 == len(out) or out[i + 1]['day'] != b['day']
    return out

def setups(pair, b4, B, start, end, dirm='bias'):
    # 4H sweep candles in the trade direction (same rules as entry S)
    res = []
    for b in b4:
        if b['t'] < start or b['t'] >= end or b['atr'] is None or b['pdl'] is None or b['dow'] > 3: continue
        bi = B.get((pair, b['wk']), ('-', '-', None)); dr = 1 if bi[0] == 'U' else -1 if bi[0] == 'D' else 0
        if dirm == 'trend': dr = 0 if b['sma20'] is None else (1 if b['c'] > b['sma20'] else -1)
        if dr == 0: continue
        lv = b['pdl'] if dr > 0 else b['pdh']
        if (b['l'] < lv < b['c']) if dr > 0 else (b['h'] > lv > b['c']):
            res.append(dict(t=b['tc'], d=dr, atr=b['atr'], c=b['c'], h=b['h'], l=b['l'], wk=b['wk'], ext=b['l'] if dr > 0 else b['h'], gap=bi[2]))
    return res

def simulate(pair, h1, S, mode, exitm='be', slmode='atr', tp=3.0, cost_pips=1.0, wait_h=24):
    pip = pip_of(pair); cost = cost_of(pair) * pip
    idx = {b['t']: i for i, b in enumerate(h1)}
    out, busy_until = [], None
    for s in S:
        if busy_until and s['t'] < busy_until + D.timedelta(hours=24): continue
        i0 = idx.get(s['t'])
        if i0 is None: continue
        d = s['d']; base_sl = s['c'] - d * s['atr']
        # ---- entry on 1H
        ent = None
        if mode == 'close4h': ent = (i0, s['c'])
        else:
            pend = None
            for j in range(i0, min(len(h1), i0 + wait_h)):
                b = h1[j]
                if b['wk'] != s['wk'] or (b['dow'] == 4 and b['last_of_day']): break
                if (b['l'] <= base_sl) if d > 0 else (b['h'] >= base_sl): break          # setup failed before an entry
                if pend is not None and ((b['l'] <= pend) if d > 0 else (b['h'] >= pend)): ent = (j + 1, pend); break
                if mode == 'bos' and j >= 3:
                    lvl = max(x['h'] for x in h1[j - 3:j]) if d > 0 else min(x['l'] for x in h1[j - 3:j])
                    if (b['c'] - lvl) * d > 0: ent = (j + 1, b['c']); break
                if mode == 'mid':
                    mid = (s['h'] + s['l']) / 2
                    if (b['c'] - mid) * d > 0: ent = (j + 1, b['c']); break
                if mode == 'fvg' and pend is None and j >= i0 + 2:
                    if d > 0 and b['l'] > h1[j - 2]['h']: pend = b['l']
                    if d < 0 and b['h'] < h1[j - 2]['l']: pend = b['h']
        if ent is None: continue
        j0, e = ent
        if slmode == 'atr': risk = s['atr']
        else: risk = max(abs(e - s['ext']) + 0.5 * s['atr'], 0.3 * s['atr'])
        sl = e - d * risk; tpl = e + d * tp * risk if tp else None
        banked, w, part, why, xt = 0.0, 1.0, False, None, None
        for j in range(j0, len(h1)):
            b = h1[j]
            if (b['l'] <= sl) if d > 0 else (b['h'] >= sl):
                px = b['o'] if ((b['o'] < sl) if d > 0 else (b['o'] > sl)) else sl; why = 'SL'
            elif not part and ((b['h'] >= e + d * risk) if d > 0 else (b['l'] <= e - risk)):
                banked += 0.5; w = 0.5; part = True; sl = e
                if tpl is not None and ((b['h'] >= tpl) if d > 0 else (b['l'] <= tpl)): px = tpl; why = 'TP'
                else: continue
            elif tpl is not None and ((b['h'] >= tpl) if d > 0 else (b['l'] <= tpl)): px = tpl; why = 'TP'
            elif b['dow'] == 4 and b['last_of_day']: px = b['c']; why = 'Fri'
            else:
                if part and exitm == 'swing1h' and j >= 5:
                    sw = min(x['l'] for x in h1[j - 5:j + 1]) if d > 0 else max(x['h'] for x in h1[j - 5:j + 1])
                    sl = max(sl, sw) if d > 0 else min(sl, sw)
                continue
            R = banked + w * (px - e) * d / risk - cost / risk
            out.append(dict(pair=pair, t=b['tc'], d=d, R=R, why=why, wk=s['wk'], gap=s['gap'], tin=h1[j0 - 1]['tc'] if j0 > 0 else None)); xt = b['tc']; break
        busy_until = xt
    return out

if __name__ == '__main__':
    pairs = sys.argv[1:] or ['EURUSD']
    U = lambda *a: D.datetime(*a, tzinfo=D.timezone.utc)
    B = bias_table(); H = [(U(2026, 9, 27, 21), U(2026, 10, 25, 21)), (U(2026, 10, 25, 21), U(2026, 11, 22))]
    V = [('4H close (current)', 'close4h', 'be', 'atr'), ('1H BOS after the sweep', 'bos', 'be', 'atr'), ('1H FVG retest (limit)', 'fvg', 'be', 'atr'),
         ('1H close over the sweep candle middle', 'mid', 'be', 'atr'), ('4H close + 1H swing trail after +1R', 'close4h', 'swing1h', 'atr'),
         ('1H BOS + SL beyond sweep +0.5 ATR', 'bos', 'be', 'sweep')]
    for dirm, rng in [('bias', H), ('trend', [(U(2026, 9, 1), U(2026, 11, 22))])]:
        print(f'\n== direction: {dirm} ==')
        for name, mode, ex, slm in V:
            parts = []
            for a, b in rng:
                tr = []
                for p in pairs:
                    b4 = load(p); h1 = load1h(p); S = setups(p, b4, B, a, b, dirm); tr += simulate(p, h1, S, mode, ex, slm)
                parts.append(tr)
            allt = sum(parts, []); R = sum(x['R'] for x in allt)
            print(f"{name:<40} {len(allt):3}tr " + ' / '.join(f"{sum(x['R'] for x in t):+5.1f}" for t in parts) + f" = {R:+5.1f}R  per trade {R/max(len(allt),1):+.2f}")
