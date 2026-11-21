# Levers for more trades / higher win rate on the current best exit (entry C, tighten 0.5 after +2R, TP 4R). 8 USD pairs W40-W47.
exec(open('usd_c_ideas.py').read().split("b0 = evalP(BASE_C)")[0])
import statistics as St
B2 = {**BASE_C, 'trailk2': 0.5, 'trailat': 2, 'tp': 4}
b0 = evalP(B2)
def wr(P):
    t = sum([run(p, data[p], B, {**B2, **P}, a, c, usd) for p in USD for a, c in H], [])
    return f"win {sum(x['R'] > 0 for x in t) / len(t):.0%}"
for n, P in [('BASE (C, tighten after 2R, TP 4R)', {}), ('cooldown 12h', dict(cool=12)), ('cooldown 4h', dict(cool=4)), ('no cooldown', dict(cool=0)),
             ('Thursday entries allowed', dict(maxdow=3)), ('bias only (no SMA20 agreement)', dict(dirm='bias')),
             ('break-even at +1R', dict(be=True)), ('half at +1R + BE, rest as base', dict(partial=True, pl=1, pf=0.5)),
             ('trail 0.5 from the start', dict(trailk=0.5)), ('TP 2R', dict(tp=2))]:
    r = evalP({**B2, **P}); line(f"{n} ({wr(P)})", r, b0)
