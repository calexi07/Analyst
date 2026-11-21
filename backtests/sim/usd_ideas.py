# Tests improvement ideas for BE Swing on the USD pairs. (a) fundamental bias, weeks W40-W47, split in halves;
# (b) the same mechanics with the trend (SMA20) as direction on the full 4H history (2024-2026), split by year.
import sys, os, datetime as D
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from swing2 import *
U = lambda *a: D.datetime(*a, tzinfo=D.timezone.utc)
B = bias_table(); data = {p: load(p) for p in USD}; usd = usd_strength(data)
H1 = (U(2026, 9, 27, 21), U(2026, 10, 25, 21)); H2 = (U(2026, 10, 25, 21), U(2026, 11, 22))
LONG = ['GBPUSD', 'AUDUSD', 'USDJPY', 'USDCHF', 'USDCAD', 'XAUUSD']
YRS = [(U(2024, 3, 1), U(2025, 1, 1)), (U(2025, 1, 1), U(2026, 1, 1)), (U(2026, 1, 1), U(2026, 11, 22))]
def bias_run(P, port={}):
    out = []
    for a, b in (H1, H2):
        tr = sum([run(p, data[p], B, P, a, b, usd) for p in USD], [])
        out.append(summ(portfolio(tr, **port)))
    return out
def trend_run(P, port={}):
    out = []
    for a, b in YRS:
        tr = sum([run(p, data[p], B, {**P, 'dirm': 'trend'}, a, b, usd) for p in LONG], [])
        out.append(summ(portfolio(tr, **port)))
    return out
IDEAS = [
 ('Baseline (bias + WTD, 1×ATR, TP 2R, 4 days)', {}, {}),
 ('No confirmation', {'cf': 'none'}, {}),
 ('Entry B: limit at 50% of the candle', {'entry': 'B'}, {}),
 ('Entry E: limit at 4H EMA20 (24h)', {'entry': 'E'}, {}),
 ('London/NY candles only', {'sess': True}, {}),
 ('First confirmation of the week only', {'first': True}, {}),
 ('Exhaustion: skip if WTD > 1.5 ATR', {'exh': 1.5}, {}),
 ('Exhaustion: skip if WTD > 1.0 ATR', {'exh': 1.0}, {}),
 ('USD basket must confirm', {'usdcf': True}, {}),
 ('Exit: hold to Friday (no 4-day stop)', {'hold': 'fri'}, {}),
 ('Exit: thesis (close back across week open)', {'thesis': True}, {}),
 ('Exit: half at 1R, rest BE, TP 3R, to Friday', {'partial': True, 'tp': 3, 'hold': 'fri'}, {}),
 ('Exit: half at 1R, rest BE, TP 2R', {'partial': True}, {}),
 ('Exit: BE after 1R', {'be': True}, {}),
 ('Exit: no TP, to Friday', {'tp': 0, 'hold': 'fri'}, {}),
 ('Exit: TP 3R, to Friday', {'tp': 3, 'hold': 'fri'}, {}),
 ('SL 1.5×ATR', {'k': 1.5}, {}),
 ('SL 0.75×ATR', {'k': 0.75}, {}),
 ('Fundamental: conviction medium/high', {'conv': 'mh'}, {}),
 ('Fundamental: |gap| ≥ 5', {'mingap': 5}, {}),
 ('Fundamental: |gap| ≥ 8', {'mingap': 8}, {}),
 ('Fundamental: top 3 USD pairs by |gap| each week', {}, {'topn': 3}),
 ('Fundamental: top 2 USD pairs by |gap| each week', {}, {'topn': 2}),
 ('Fundamental + trend agree', {'dirm': 'both'}, {}),
 ('Max 1 open trade across USD pairs', {}, {'cap': 1}),
 ('Max 2 open trades across USD pairs', {}, {'cap': 2}),
 ('Max 3 open trades across USD pairs', {}, {'cap': 3}),
]
fmt = lambda s: f"{s['n']:3}tr {s['R']:+6.1f}R ({s['exp']:+.2f})"
print(f"{'idea':<48} | bias W40-43 | bias W44-47 | trend 2024 | trend 2025 | trend 2026")
for name, P, port in IDEAS:
    b = bias_run(P, port)
    t = trend_run(P, port) if not name.startswith('Fundamental') else None
    print(f"{name:<48} | {fmt(b[0])} | {fmt(b[1])} | " + (' | '.join(fmt(x) for x in t) if t else '(fundamental only)'))
