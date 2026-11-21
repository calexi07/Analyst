# Entry search for BE Swing: levels (yesterday H/L, day/week/month open, last week H/L) and liquidity sweeps, exit fixed at the default.
# Scored on 3 years (trend direction, 6 USD pairs, per year) and on the bias weeks (bias + trend agree, 8 USD pairs, two halves).
import sys, os, datetime as D, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from swing2 import *
U = lambda *a: D.datetime(*a, tzinfo=D.timezone.utc)
data = {p: load(p) for p in USD}; usd = usd_strength(data); B = bias_table()
LONG = ['GBPUSD', 'AUDUSD', 'USDJPY', 'USDCHF', 'USDCAD', 'XAUUSD']
YRS = [(U(2024, 3, 1), U(2025, 1, 1)), (U(2025, 1, 1), U(2026, 1, 1)), (U(2026, 1, 1), U(2026, 11, 22))]
H = [(U(2026, 9, 27, 21), U(2026, 10, 25, 21)), (U(2026, 10, 25, 21), U(2026, 11, 22))]
EX = dict(partial=True, tp=3, hold='fri')
def dd(t):
    eq = pk = m = 0
    for x in sorted(t, key=lambda x: x['tx']): eq += x['R']; pk = max(pk, eq); m = min(m, eq - pk)
    return m
E = [('A  at the confirming close (current)', dict(entry='A')), ('D  break of yesterday high/low', dict(entry='D')),
     ('PDL limit at yesterday low (long) / high (short)', dict(entry='PDL')), ('DO  limit at the day open', dict(entry='DO')),
     ('WO  limit at the week open', dict(entry='WO')), ('MO  limit at the month open', dict(entry='MO')),
     ('PWL limit at last week low/high', dict(entry='PWL')),
     ('SWP sweep of yesterday low/high + reclaim', dict(entry='SWP')), ('SWP + stop beyond the sweep', dict(entry='SWP', swsl=True)),
     ('SW6 sweep of the 24h 4H low/high + reclaim', dict(entry='SW6')), ('SW6 + stop beyond the sweep', dict(entry='SW6', swsl=True)),
     ('SWW sweep of last week low/high + reclaim', dict(entry='SWW')), ('SWW + stop beyond the sweep', dict(entry='SWW', swsl=True))]
print(f"{'entry':<48}| 3y trend: trades, R, R/tr, per year, maxDD | bias weeks: H1, H2, R/tr, maxDD")
for cf in ['wtd', 'none']:
    print(f'--- confirmation: {cf}')
    for n, P in E:
        Q = {**EX, **P, 'cf': cf}
        yr = [sum([run(p, data[p], B, {**Q, 'dirm': 'trend'}, a, b, usd) for p in LONG], []) for a, b in YRS]
        t3 = sum(yr, []); hb = [sum([run(p, data[p], B, {**Q, 'dirm': 'both'}, a, b, usd) for p in USD], []) for a, b in H]; tb = sum(hb, [])
        R3 = sum(x['R'] for x in t3); Rb = sum(x['R'] for x in tb)
        print(f"{n:<48}| {len(t3):4} {R3:+6.1f}R {R3/max(len(t3),1):+.2f} [{', '.join(f'{sum(x['R'] for x in y):+.0f}' for y in yr)}] {dd(t3):+5.1f} | {sum(x['R'] for x in hb[0]):+5.1f} {sum(x['R'] for x in hb[1]):+5.1f} ({len(tb)}tr {Rb/max(len(tb),1):+.2f}) {dd(tb):+5.1f}")
