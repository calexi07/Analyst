# Mechanical backtest of the MTF analysis rules (ANALYST.md v1.3), technical part only (no fundamental history before Oct 2026).
# Uses only information available at each 1H candle close (the export columns are computed bar by bar, no repaint).
import pandas as pd, numpy as np, sys
P = sys.argv[1] if len(sys.argv) > 1 else 'EURUSD'
SPREAD = {'EURUSD': 0.00008, 'GBPUSD': 0.00012}.get(P, 0.0001)
d = pd.read_csv(f'/home/claude/mtfbt/{P}.csv')
d['t'] = pd.to_datetime(d.time, utc=True)
n = len(d); O, H, L, C = (d[c].values for c in ['open', 'high', 'low', 'close'])
pc = np.r_[np.nan, C[:-1]]
tr = np.nanmax(np.vstack([H - L, np.abs(H - pc), np.abs(L - pc)]), axis=0)
atr1 = pd.Series(tr).rolling(14).mean().values
# 4H ATR from 4H bins (local time bins of 4 hours)
loc = d.time.str.slice(0, 13)
key4 = d.time.str.slice(0, 10) + '|' + (d.time.str.slice(11, 13).astype(int) // 4).astype(str)
g = pd.DataFrame({'k': key4, 'h': H, 'l': L, 'c': C}).groupby('k', sort=False).agg(h=('h', 'max'), l=('l', 'min'), c=('c', 'last'))
g['pc'] = g.c.shift(1); g['tr'] = np.maximum(g.h - g.l, np.maximum((g.h - g.pc).abs(), (g.l - g.pc).abs()))
g['atr'] = g.tr.rolling(14).mean().shift(1)          # ATR of closed 4H candles only
atr4 = key4.map(g.atr).values
col = lambda c: d[c].values
LV = [c for c in d.columns if c.endswith(' CHoCH') or c.endswith(' BOS') or 'zone full' in c or 'zone refined' in c]

def zones(tf):
    """segments of the fractal zone columns of a timeframe: (start_row, dir, full_lo, full_hi, ref_lo, ref_hi)"""
    k = list(zip(col(f'{tf} zone dir (1 demand, -1 supply)'), col(f'{tf} zone full low'), col(f'{tf} zone full high'), col(f'{tf} zone refined low'), col(f'{tf} zone refined high')))
    out = []; prev = None
    for i, z in enumerate(k):
        zz = tuple(None if pd.isna(x) else round(float(x), 6) for x in z)
        if zz != prev:
            if zz[0] in (1, -1) and None not in zz: out.append((i,) + zz)
            prev = zz
    return out

def sim(i0, dirn, entry, sl, tp, maxbars, limit=True, start=None):
    """fill a limit at entry from bar i0 (inclusive) within maxbars; then SL first; returns dict"""
    risk = abs(entry - sl)
    fill = None
    for i in range(i0, min(n, i0 + maxbars)):
        hit = L[i] <= entry if dirn < 0 and False else (H[i] >= entry if dirn < 0 else L[i] <= entry)
        if hit: fill = i; break
    if fill is None: return None
    res = {}
    for name, T in tp.items():
        r = None; mfe = 0
        for i in range(fill, min(n, fill + 120)):
            if dirn < 0:
                if H[i] >= sl + SPREAD: r = -1; break
                if i > fill or C[i] < entry:   # target on the fill candle only if the candle closed in favour
                    if L[i] <= T: r = (entry - T) / risk; break
            else:
                if L[i] <= sl - SPREAD: r = -1; break
                if i > fill or C[i] > entry:
                    if H[i] >= T: r = (T - entry) / risk; break
        if r is None: r = (C[min(n, fill + 120) - 1] - entry) / risk * (1 if dirn > 0 else -1)
        res[name] = r - SPREAD / risk
    return fill, res

rows = []
for TF, REF, ATR, LIFE in [('1H', '4H', atr1, 48), ('4H', 'D', atr4, 120)]:
    zone_tfs = ['4H', '1H'] if TF == '1H' else ['D', '4H']
    for ztf in zone_tfs:
        for (s, dirn, flo, fhi, rlo, rhi) in zones(ztf):
            if s + 2 >= n: continue
            dirn = -1 if dirn < 0 else 1
            prox = rlo if dirn < 0 else rhi
            distal = fhi if dirn < 0 else flo
            # walk forward: count touches; invalidated on close beyond distal
            tests = 0; inside = False
            for i in range(s + 1, min(n, s + LIFE * 3)):
                touch = H[i] >= prox if dirn < 0 else L[i] <= prox
                if (C[i] > distal) if dirn < 0 else (C[i] < distal): break
                if not touch: inside = False; continue
                if inside: continue
                inside = True; tests += 1
                if tests > 2: break
                if i - s > LIFE: break
                # setup state as the analysis would see it at the close of the previous candle
                j = i - 1
                a = ATR[j]
                if not np.isfinite(a): continue
                p1 = col('D swing trend')[j] == dirn
                p2 = col('4H swing trend')[j] == dirn
                posc = col(f'{REF} swing pos %')[j]
                p4 = np.isfinite(posc) and ((posc > 50) if dirn < 0 else (posc < 50))
                pro = p1
                sl = distal + (a * 0.1 if dirn < 0 else -a * 0.1)
                entry = prox
                risk = abs(entry - sl)
                if risk <= 0: continue
                lv = np.array([d[c].values[j] for c in LV], dtype=float); lv = lv[np.isfinite(lv)]
                beyond = lv[(lv <= entry - 1.5 * risk)] if dirn < 0 else lv[(lv >= entry + 1.5 * risk)]
                beyond = beyond[np.abs(beyond - entry) <= 6 * risk]
                tp_struct = (beyond.max() if dirn < 0 else beyond.min()) if len(beyond) else None
                tps = {'2R': entry - 2 * risk * (1 if dirn < 0 else -1) * 1, '3R': entry + 3 * risk * dirn}
                tps['2R'] = entry + 2 * risk * dirn
                if tp_struct is not None: tps['struct'] = tp_struct
                # limit variant: fills at the touch candle (i) by construction
                fr = sim(i, dirn, entry, sl, tps, 1)
                if fr is None: continue
                fill, res = fr
                npill = int(p1) + int(p2) + int(p4)
                # --- quality features ---
                # Q2 origin sweep: the zone's extreme candle took the highest high (supply) / lowest low (demand) of the 48 candles before it
                xi = None
                for k in range(s, max(0, s - 400), -1):
                    if (dirn < 0 and abs(H[k] - distal) < 1e-9) or (dirn > 0 and abs(L[k] - distal) < 1e-9): xi = k; break
                sweep = False; swept_close_back = False
                if xi is not None and xi > 50:
                    prev_ext = H[xi-48:xi].max() if dirn < 0 else L[xi-48:xi].min()
                    sweep = distal > prev_ext if dirn < 0 else distal < prev_ext
                    swept_close_back = sweep and ((C[xi] < prev_ext) if dirn < 0 else (C[xi] > prev_ext))
                # Q1 inducement: a 1H fractal high (supply) / low (demand) formed after the zone, between price and the zone, was taken before the touch
                ind = False
                for k in range(s + 2, i - 1):
                    if dirn < 0 and H[k] > H[k-1] and H[k] > H[k-2] and H[k] > H[k+1] and H[k] < prox and H[k+2:i+1].max() > H[k]: ind = True; break
                    if dirn > 0 and L[k] < L[k-1] and L[k] < L[k-2] and L[k] < L[k+1] and L[k] > prox and L[k+2:i+1].min() < L[k]: ind = True; break
                hr = int(d.time[i][11:13])
                sess = 'Asia' if hr < 9 else 'London' if hr < 15 else 'NY' if hr < 20 else 'Late'
                rows.append(dict(t=d.t[i], tf=TF, zone_tf=ztf, dir=dirn, test=tests, pro=pro, p1=p1, p2=p2, p4=p4, pillars=npill,
                                 risk_pips=risk / 0.0001 if 'JPY' not in P else risk / 0.01, has_struct=tp_struct is not None,
                                 r_2R=res['2R'], r_3R=res['3R'], r_struct=res.get('struct', np.nan), year=d.t[i].year,
                                 sweep=sweep, sweep_back=swept_close_back, ind=ind, sess=sess, age=i - s, zone_atr=risk / a,
                                 dow=d.t[i].dayofweek, pos=posc))
                break   # one trade per zone (the first qualifying touch)
R = pd.DataFrame(rows)
R.to_csv(f'/home/claude/mtfbt/{P}_trades.csv', index=False)
print(P, 'trades', len(R))
