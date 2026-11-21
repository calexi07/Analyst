# One-factor-at-a-time research around the sweep + bias baseline. A change is only interesting if it helps BOTH halves of the
# bias weeks; exit-type changes are also checked on 3 years (trend direction) where the mechanics get hundreds of trades.
import sys, os, datetime as D, statistics as S, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from swing2 import *
U = lambda *a: D.datetime(*a, tzinfo=D.timezone.utc)
data = {p: load(p) for p in USD}; usd = usd_strength(data); B = bias_table()
LONG = ['GBPUSD', 'AUDUSD', 'USDJPY', 'USDCHF', 'USDCAD', 'XAUUSD']
YRS = [(U(2024, 3, 1), U(2025, 1, 1)), (U(2025, 1, 1), U(2026, 1, 1)), (U(2026, 1, 1), U(2026, 11, 22))]
H = [(U(2026, 9, 27, 21), U(2026, 10, 25, 21)), (U(2026, 10, 25, 21), U(2026, 11, 22))]
BASE = dict(entry='SWP', cf='none', dirm='bias', partial=True, tp=3, hold='fri')
def evalP(P, port={}, trend=True):
    Q = {**BASE, **P}
    hs = [portfolio(sum([run(p, data[p], B, Q, a, b, usd) for p in USD], []), **port) for a, b in H]
    allt = sorted(hs[0] + hs[1], key=lambda x: x['tx']); eq = pk = dd = 0; wk = collections.defaultdict(float)
    for x in allt: eq += x['R']; pk = max(pk, eq); dd = min(dd, eq - pk); wk[x['wk'][1]] += x['R']
    w = [wk.get(k, 0) for k in range(40, 48)]; b2 = [w[i] + w[i + 1] for i in range(0, 8, 2)]
    t = None
    if trend:
        t = [sum(x['R'] for x in portfolio(sum([run(p, data[p], B, {**Q, 'dirm': 'trend'}, a, b, usd) for p in LONG], []), **port)) for a, b in YRS]
    Rs = [x['R'] for x in allt]
    return dict(n=len(allt), h1=sum(x['R'] for x in hs[0]), h2=sum(x['R'] for x in hs[1]), R=sum(Rs), dd=dd, b2=b2,
                tstat=(S.mean(Rs) / (S.stdev(Rs) / len(Rs) ** .5)) if len(Rs) > 2 else 0, t=t)
def line(name, r, base=None):
    flag = ''
    if base: flag = '  ✓ both halves better' if r['h1'] > base['h1'] and r['h2'] > base['h2'] else ''
    tr = f" | 3y trend {sum(r['t']):+6.1f}R [{', '.join(f'{v:+.0f}' for v in r['t'])}]" if r['t'] else ''
    print(f"{name:<44} {r['n']:3}tr {r['h1']:+5.1f}/{r['h2']:+5.1f} = {r['R']:+5.1f}R  dd{r['dd']:+5.1f}  2wk[{', '.join(f'{v:+.1f}' for v in r['b2'])}]{tr}{flag}")
b0 = evalP({}); line('BASELINE sweep + bias', b0); print(f"   per-trade t-stat {b0['tstat']:.2f}")
TESTS = [
 ('--- stop', None), ('SL 0.75×ATR', dict(k=0.75)), ('SL 1.25×ATR', dict(k=1.25)), ('SL 1.5×ATR', dict(k=1.5)),
 ('--- target of the 2nd half', None), ('TP 2R', dict(tp=2)), ('TP 4R', dict(tp=4)), ('No TP (Friday)', dict(tp=0)),
 ('--- partial', None), ('partial 30% at 1R', dict(pf=0.3)), ('partial 70% at 1R', dict(pf=0.7)), ('partial 50% at 0.75R', dict(pl=0.75)),
 ('partial 50% at 1.5R', dict(pl=1.5)), ('no BE move after partial', dict(bemove=False)), ('BE +0.25R after partial', dict(belock=0.25)),
 ('no partial (one TP 2R)', dict(partial=False, tp=2)),
 ('--- trade frequency', None), ('no cooldown after exit', dict(cool=0)), ('48h cooldown', dict(cool=48)), ('max 1 trade/pair/week', dict(maxwk=1)), ('max 2 trades/pair/week', dict(maxwk=2)),
 ('--- sweep quality', None), ('shallow sweep (≤0.25 ATR)', dict(swdepth=(0, 0.25))), ('deep sweep (≥0.25 ATR)', dict(swdepth=(0.25, 99))),
 ('sweep ≥0.1 ATR', dict(swdepth=(0.1, 99))), ('close in top 50% of candle', dict(swclose=0.5)), ('close in top 70% of candle', dict(swclose=0.7)),
 ('limit at 50% of the sweep candle', dict(swlimit=True)),
 ('--- time of the sweep candle (Bucharest)', None), ('Asia 00-08', dict(hours=(0, 8))), ('London 08-15', dict(hours=(8, 15))), ('New York 15-24', dict(hours=(15, 24))), ('08-24 (no Asia)', dict(hours=(8, 24))),
 ('--- fundamental', None), ('|gap| ≥ 5', dict(mingap=5)), ('|gap| ≥ 8', dict(mingap=8)), ('conviction medium/high', dict(conv='mh')),
 ('bias + trend agree', dict(dirm='both')), ('+ week-to-date confirmation', dict(cf='wtd')),
 ('--- weekend', None), ('no Friday close', dict(fri=False, hold=1000)),
]
for name, P in TESTS:
    if P is None: print(name); continue
    exitish = any(k in P for k in ('k', 'tp', 'pf', 'pl', 'bemove', 'belock', 'partial', 'cool', 'maxwk', 'fri', 'hours', 'swdepth', 'swclose', 'swlimit'))
    line('  ' + name, evalP(P, trend=exitish), b0)
print('--- portfolio (all 8 USD pairs)')
for name, port in [('max 2 open', dict(cap=2)), ('max 3 open', dict(cap=3)), ('max 4 open', dict(cap=4)), ('stop the week at -2R', dict(wkstop=2))]:
    line('  ' + name, evalP({}, port, trend=False), b0)
