# Exit research on the sweep + bias baseline (8 USD pairs, W40-47), with the 3-year trend-direction run as a mechanics check.
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from usd_sweep_research import evalP, line, b0, data, B, usd, H, BASE, run, USD
# 1) how far do trades go? (no target, no partial, stop only, Friday close)
raw = sum([run(p, data[p], B, {**BASE, 'partial': False, 'tp': 0}, a, c, usd) for p in USD for a, c in H], [])
print(f"\nMFE (no target, SL 1 ATR, Friday close): {len(raw)} trades")
for lv in (0.5, 1, 1.5, 2, 3, 4, 5): print(f"  reached +{lv}R: {sum(x['mfe'] >= lv for x in raw) / len(raw):.0%}")
print("  exits:", collections.Counter(x['why'] for x in raw), f"total {sum(x['R'] for x in raw):+.1f}R")
T = [
 ('--- fixed single target, no partial', None),
 *[(f'TP {r}R all-in', dict(partial=False, tp=r)) for r in (1.5, 2, 2.5, 3, 4)],
 ('--- structural targets (fallback 2R if <1R away)', None),
 ('2nd half to prev-day high/low', dict(tpmode='pdh')), ('2nd half to prev-week high/low', dict(tpmode='pwh')),
 ('all-in to prev-week high/low', dict(tpmode='pwh', partial=False)),
 ('--- second half trailed (no TP)', None),
 *[(f'chandelier {k}×ATR from best', dict(tp=0, trailm='chand', trailk=k, trailfrom=1)) for k in (0.75, 1.0, 1.5, 2.0)],
 *[(f'trail last {n} 4H candles', dict(tp=0, trailm='nbar', trailn=n, trailfrom=1)) for n in (3, 6, 12)],
 ('trail prev-day low/high', dict(tp=0, trailm='pday', trailfrom=1)),
 ('trail 4H EMA20 close', dict(tp=0, restx='ema20')),
 ('--- TP 3R kept + trail', None),
 ('TP3 + chandelier 1.5', dict(trailm='chand', trailk=1.5, trailfrom=1)),
 ('TP4 + chandelier 1.5', dict(tp=4, trailm='chand', trailk=1.5, trailfrom=1)),
 ('TP3 + trail 6 candles', dict(trailm='nbar', trailn=6, trailfrom=1)),
 ('--- lock steps', None),
 ('lock +1R at +2R', dict(steps=((2, 1),))), ('lock +1R at +2R, +2R at +3R', dict(tp=4, steps=((2, 1), (3, 2)))),
 ('--- thirds', None),
 ('1/3 at 1R, 1/3 at 2R (lock 1R), rest 3R', dict(pf=1/3, p2=(2, 1), p2f=1/3)),
 ('1/3 at 1R, 1/3 at 2R (lock 1R), rest trail 1.5ATR', dict(pf=1/3, p2=(2, 1), p2f=1/3, tp=0, trailm='chand', trailk=1.5, trailfrom=2)),
 ('--- time', None),
 *[(f'max hold {h} days', dict(hold=h)) for h in (1, 2, 3)],
 ('no Friday close + chandelier 1.5', dict(fri=False, hold=1000, tp=0, trailm='chand', trailk=1.5, trailfrom=1)),
 ('no Friday close, TP3, max 7 days', dict(fri=False, hold=7)),
]
print()
for n, P in T:
    if P is None: print(n); continue
    line('  ' + n, evalP(P), b0)
