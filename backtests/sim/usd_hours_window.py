# Trader's hours 06:00-22:00 Bucharest. On 4H candles (00,04,...,20) the edges fall inside the 04-08 and 20-24 candles,
# so two bounds: strict = fills only in the 08, 12, 16 candles; loose = 04 to 20 candles (04-24). Market entries are not used (entry C).
exec(open('usd_c_ideas.py').read().split("b0 = evalP(BASE_C)")[0])
b0 = evalP(BASE_C)
TI = dict(trailk2=0.5, trailat=2, tp=4)
for n, P in [('current settings, all hours', {}), ('  hours strict 08-20', dict(fillhrs=(8, 12, 16))), ('  hours loose 04-24', dict(fillhrs=(4, 8, 12, 16, 20))),
             ('tighten 0.5 after 2R + TP 4R, all hours', TI), ('  hours strict 08-20', {**TI, 'fillhrs': (8, 12, 16)}), ('  hours loose 04-24', {**TI, 'fillhrs': (4, 8, 12, 16, 20)})]:
    line(n, evalP({**BASE_C, **P}), b0)
