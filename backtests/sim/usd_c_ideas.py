# Five new entries plus trailing and target variants around the user's settings (entry C, TP 3R, trail close 0.75 x 4H ATR).
# 8 USD pairs, bias weeks W40-W47 (worst-case same-bar fills); 3-year column = same mechanics with the SMA20 trend as direction.
exec(open('usd_screenshot2.py').read().split('for n, P in')[0])
BASE_C = {**SHOT, 'tp': 3}
b0 = evalP(BASE_C)
line('BASE: entry C, TP 3R, trail close 0.75', b0)
T = [
 ('--- entries', None),
 ('C + buffer 0.1 ATR', dict(entry='CB', cbuf=0.1)), ('C + buffer 0.25 ATR', dict(entry='CB', cbuf=0.25)),
 ('C only after a candle closing in direction', dict(entry='CD')), ('break of a pullback candle', dict(entry='PB')),
 ('break of the last 2 candles', dict(entry='C2')), ('C with 4H close beyond 4H EMA20', dict(entry='CE')),
 ('Asian range (00-08) break until 16:00', dict(entry='AR')), ('break of yesterday high/low (D)', dict(entry='D')),
 ('--- trailing (entry C, TP 3R)', None),
 ('trail close 0.75, tighten to 0.5 after +2R', dict(trailk2=0.5, trailat=2)), ('trail close 0.75 only after +1R', dict(trailfrom=1)),
 ('trail close 1.0, tighten to 0.5 after +1.5R', dict(trailk=1.0, trailk2=0.5, trailat=1.5)),
 ('chandelier 1.0 x 4H ATR from entry', dict(trailm='chand', trailk=1.0)), ('chandelier 1.5 x 4H ATR from entry', dict(trailm='chand', trailk=1.5)),
 ('low/high of last 2 candles', dict(trailm='nbar', trailn=2)), ('low/high of last 3 candles', dict(trailm='nbar', trailn=3)),
 ('--- target', None),
 ('TP 2R', dict(tp=2)), ('TP 2.5R', dict(tp=2.5)), ('TP 4R', dict(tp=4)), ('no TP', dict(tp=0)),
 ('TP at yesterday high/low (min 1R, else 3R)', dict(tpmode='pdh')), ('TP at last week high/low (min 1R, else 3R)', dict(tpmode='pwh')),
 ('half at 2R, rest trailed, no TP', dict(partial=True, pl=2, pf=0.5, bemove=False, tp=0)),
 ('half at 1.5R, rest trailed, TP 4R', dict(partial=True, pl=1.5, pf=0.5, bemove=False, tp=4)),
]
for n, P in T:
    if P is None: print(n); continue
    line('  ' + n, evalP({**BASE_C, **P}), b0)
print('--- combinations')
TI = dict(trailk2=0.5, trailat=2)
for n, P in [('tighten 0.5 after +2R + TP 4R', {**TI, 'tp': 4}), ('tighten + no TP', {**TI, 'tp': 0}),
             ('candle in direction + tighten', {**TI, 'entry': 'CD'}), ('candle in direction + tighten + TP 4R', {**TI, 'entry': 'CD', 'tp': 4}),
             ('EMA20 side + tighten', {**TI, 'entry': 'CE'}), ('EMA20 side + tighten + TP 4R', {**TI, 'entry': 'CE', 'tp': 4})]:
    line('  ' + n, evalP({**BASE_C, **P}), b0)
