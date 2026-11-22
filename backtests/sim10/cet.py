# CET (Contraction → Expansion) indicator as an entry: 3-candle body contraction (middle body largest, both neighbours'
# bodies inside it) inside a time window; trade the first CLOSE beyond the zone high/low; SL other side of the zone
# (or the middle); TP in R; close at 21:45. One trade per day per instrument.
import collections
def cet_trades(bars, dir_of_day, cost, w0=300, w1=780, tp=2.0, sl='opp', xm=1305, maxper=1, need_dir=True, maxw=None, fade=False):
    out = []; days = collections.OrderedDict()
    for i, b in enumerate(bars): days.setdefault(b['d'], []).append(i)
    for d0, ix in days.items():
        D_ = dir_of_day(d0, bars[ix[len(ix)//2]])
        if need_dir and not D_: continue
        zone = None; n = 0; pos = None
        for k, i in enumerate(ix):
            b = bars[i]
            if pos:
                e, s, t, dd, r = pos
                if (b['l'] <= s) if dd > 0 else (b['h'] >= s): out.append((b['t'], dd * (s - e) / r - cost / r)); pos = None
                elif t and ((b['h'] >= t) if dd > 0 else (b['l'] <= t)): out.append((b['t'], dd * (t - e) / r - cost / r)); pos = None
                elif b['m'] >= xm: out.append((b['t'], dd * (b['c'] - e) / r - cost / r)); pos = None
                continue
            if n >= maxper: break
            if k >= 2:
                a, m, c = bars[ix[k-2]], bars[ix[k-1]], b
                bt = lambda x: (max(x['o'], x['c']), min(x['o'], x['c']))
                (at, ab), (mt, mb), (ct, cb) = bt(a), bt(m), bt(c)
                if (mt - mb) > (ct - cb) and (mt - mb) > (at - ab) and at <= mt and ab >= mb and ct <= mt and cb >= mb and w0 <= b['m'] < w1:
                    zone = [max(a['h'], m['h'], c['h']), min(a['l'], m['l'], c['l']), 0]; continue
            if zone and zone[2] == 0 and b['m'] < xm - 60:
                dd = 1 if b['c'] > zone[0] else -1 if b['c'] < zone[1] else 0
                if fade: dd = -dd
                if dd:
                    zone[2] = dd
                    if D_ and dd not in D_: continue
                    if maxw and b['m'] >= maxw: continue
                    e = b['c']; s = ((zone[1] if dd > 0 else zone[0]) if sl == 'opp' else (zone[0] + zone[1]) / 2) if not fade else (b['l'] - 0.0 if dd > 0 else b['h'])
                    r = abs(e - s)
                    if r <= 0: continue
                    pos = (e, s, e + dd * tp * r if tp else None, dd, r); n += 1
        if pos: b = bars[ix[-1]]; e, s, t, dd, r = pos; out.append((b['t'], dd * (b['c'] - e) / r - cost / r))
    return out
