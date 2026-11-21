# Robustness: the same structure strategies on 4H candles over ~3 years (6 long-history pairs), SMA20 trend as direction.
import sys, os, csv, datetime as D, collections, statistics as St
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mtf, smc
from swing2 import NY
HERE = os.path.dirname(os.path.abspath(__file__))
def load4(pair):
    out = []
    for r in csv.DictReader(open(os.path.join(HERE, f'../ohlc/FOREXCOM_{pair}_240.csv'))):
        t = D.datetime.fromisoformat(r['time']).astimezone(D.timezone.utc)
        b = dict(t=t, tc=t + D.timedelta(hours=4), o=float(r['open']), h=float(r['high']), l=float(r['low']), c=float(r['close']))
        ny = (t + D.timedelta(hours=7)).astimezone(NY); b['day'] = ny.date(); b['dow'] = ny.weekday(); b['wk'] = ny.date().isocalendar()[:2]
        out.append(b)
    out.sort(key=lambda b: b['t'])
    for i, b in enumerate(out): b['last_of_day'] = i + 1 == len(out) or out[i + 1]['day'] != b['day']
    return out
smc.load1h = load4
U = smc.U; YRS = [(U(2024, 3, 1), U(2025, 1, 1)), (U(2025, 1, 1), U(2026, 1, 1)), (U(2026, 1, 1), U(2026, 11, 22))]
LONG = ['GBPUSD', 'AUDUSD', 'USDJPY', 'USDCHF', 'USDCAD', 'XAUUSD']; DATA = {p: smc.prep(p) for p in LONG}
for S, ex in [('bos_discount', 'tp3'), ('bos_discount', 'tp2'), ('sweep_choch', 'tp2'), ('weekly_draw', 'liq'), ('fvg_disp', 'tp3')]:
    P = dict(strat=S, exit=ex, dirm='trend', hours=(0, 24), swL=6, inL=2, trL=3, cool=24)
    ys = [sum([smc.run(p, DATA[p], P, a, c) for p in LONG], []) for a, c in YRS]
    allr = [x['R'] for y in ys for x in y]
    yr = ', '.join('%+.0f' % sum(x['R'] for x in y) for y in ys)
    print(f"{S:<13} {ex:<4} 4H, 3y, trend dir: {len(allr)}tr {sum(allr):+6.1f}R win {sum(r > 0 for r in allr) / max(1, len(allr)):.0%} by year [{yr}]")
