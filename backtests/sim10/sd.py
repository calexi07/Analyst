# Supply / demand zones on the higher timeframe (1H / 4H) + confirmation on the lower timeframe (15m / 5m).
# Zone: 1-6 base candles (small bodies) followed by a departure candle (big body) — DBR/RBR demand, RBD/DBD supply.
#   proximal = edge of the base bodies (entry side), distal = extreme wick of base + departure (stop side).
#   Zone is known only after the departure candle closes. Fresh = not touched yet; invalid after a HTF close beyond distal.
# Trade (first touch only): price touches proximal on the LTF → wait for a LTF CHoCH in the zone direction (or enter directly).
# All checks use closed bars only; when stop and target are in the same LTF bar, the stop counts first.
import sys, bisect
sys.path.append('/home/claude/analyst/backtests/sim')
from lux5 import structure

def atr_(b, n=14):
    A = None
    for i, x in enumerate(b):
        tr = x['h'] - x['l'] if i == 0 else max(x['h'], b[i-1]['c']) - min(x['l'], b[i-1]['c'])
        A = tr if A is None else (A * (n - 1) + tr) / n; x['atr'] = A if i >= n else None

def zones(h, dep=1.2, base_max=6, base_body=0.5, bos_n=20):
    """h: HTF bars with t, tc (close time), o,h,l,c, atr. Returns list of zone dicts."""
    out = []
    for k in range(bos_n + base_max + 1, len(h)):
        x = h[k]; A = x['atr']
        if not A: continue
        body = x['c'] - x['o']; rng = x['h'] - x['l']
        if abs(body) < dep * A or rng <= 0 or abs(body) / rng < 0.6: continue
        d = 1 if body > 0 else -1
        j = k - 1; base = []
        while j >= 0 and len(base) < base_max and abs(h[j]['c'] - h[j]['o']) <= base_body * h[j]['atr'] if h[j]['atr'] else False:
            base.append(h[j]); j -= 1
        if not base: continue
        tops = [max(y['o'], y['c']) for y in base]; bots = [min(y['o'], y['c']) for y in base]
        if d > 0: prox = max(tops); dist = min(min(y['l'] for y in base), x['l'])
        else: prox = min(bots); dist = max(max(y['h'] for y in base), x['h'])
        if (prox - dist) * d <= 0: continue
        prior = h[k - bos_n - len(base):k - len(base)]
        bos = (x['c'] > max(y['h'] for y in prior)) if d > 0 else (x['c'] < min(y['l'] for y in prior))
        legin = h[j] if j >= 0 else None
        kind = ('DBR' if legin and legin['c'] < legin['o'] else 'RBR') if d > 0 else ('RBD' if legin and legin['c'] > legin['o'] else 'DBD')
        out.append(dict(d=d, prox=prox, dist=dist, t=x['tc'], k=k, strength=abs(x['c'] - prox) / A, nbase=len(base), bos=bos,
                        kind=kind, width=abs(prox - dist) / A, hatr=A))
    return out

def run(l, h, Z, dirf, cost, conf='choch', entry='mkt', sl='ltf', tp=3.0, maxh=288, arm=96, s=5,
        need_bos=False, min_str=0.0, max_base=6, rev_only=False, max_age=120, max_width=3.0):
    """l: LTF bars (t, o,h,l,c, atr); h: HTF bars (for invalidation by HTF close); Z: zones.
    dirf(bar) -> allowed directions. Returns [(time, R, zone)]."""
    ev = structure(l, s) if conf == 'choch' else []
    evi = [e[0] for e in ev]
    ht = [x['tc'] for x in h]
    lt = [x['t'] for x in l]
    out = []; busy_until = -1
    zs = [z for z in Z if (not need_bos or z['bos']) and z['strength'] >= min_str and z['nbase'] <= max_base
          and (not rev_only or z['kind'] in ('DBR', 'RBD')) and z['width'] <= max_width]
    for z in zs:
        d = z['d']; i0 = bisect.bisect_left(lt, z['t'])          # first LTF bar after the departure closed
        if i0 >= len(l): continue
        # first touch of proximal; zone dies if a HTF candle closes beyond distal before that or it gets too old
        kz = z['k']; touch = None
        for i in range(i0, len(l)):
            x = l[i]
            hk = bisect.bisect_right(ht, x['t']) - 1                # last closed HTF bar
            if hk - kz > max_age: break
            if hk > kz and (h[hk]['c'] - z['dist']) * d < 0: break
            if (x['l'] <= z['prox']) if d > 0 else (x['h'] >= z['prox']):
                touch = i; break
        if touch is None: continue
        D_ = dirf(l[touch])
        if not D_ or d not in D_: continue
        A = l[touch]['atr'] or 0
        if entry == 'limit':                                         # classic: limit at proximal, SL beyond distal
            e = z['prox']; stop = z['dist'] - d * 0.1 * z['hatr']; j0 = touch; first_bar_tp = False
            # if the touch bar also went through the stop: stop first
        else:
            # wait for a LTF CHoCH in direction d after the touch, while price has not closed beyond distal
            q = bisect.bisect_right(evi, touch - 1); e = None
            while q < len(ev) and ev[q][0] <= touch + arm:
                i, kind, dd, pv = ev[q]
                if any((l[m]['c'] - z['dist']) * d < 0 for m in range(touch, i + 1)): break
                if kind == 'CHoCH' and dd == d: e = l[i]['c']; ci = i; pvi = pv; break
                q += 1
            if e is None: continue
            leg = l[min(touch, pvi):ci + 1]
            ext = min(y['l'] for y in leg) if d > 0 else max(y['h'] for y in leg)
            stop = ext - d * 0.1 * (l[ci]['atr'] or A) if sl == 'ltf' else z['dist'] - d * 0.1 * z['hatr']
            j0 = ci + 1; first_bar_tp = True
        r = abs(e - stop)
        if r <= 0 or (e - stop) * d <= 0 or (A and r < 0.3 * A): continue
        t = e + d * tp * r; res = None
        for j in range(j0, min(len(l), j0 + maxh)):
            y = l[j]
            if (y['l'] <= stop) if d > 0 else (y['h'] >= stop): res = -1.0; break
            if (first_bar_tp or j > j0) and ((y['h'] >= t) if d > 0 else (y['l'] <= t)): res = tp; break
        else:
            j = min(len(l) - 1, j0 + maxh - 1); res = d * (l[j]['c'] - e) / r
        out.append((l[touch]['t'], res - cost / r, z, touch, j))
    out.sort(key=lambda x: x[3]); keep = []; busy = -1
    for x in out:                                   # one trade at a time per instrument
        if x[3] > busy: keep.append(x[:3]); busy = x[4]
    return keep
