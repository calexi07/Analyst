# Entry-hour study for the user's settings (entry C on 4H, TP 3R, trail close 0.75): by the 4H candle the entry fills in (Bucharest time)
exec(open('usd_screenshot2.py').read().split('for n, P in')[0])
import datetime as D, statistics as St
SH = {**SHOT, 'tp': 3}
tr = []
for k, (a, c) in enumerate(H):
    for p in USD:
        for x in run(p, data[p], B, SH, a, c, usd): x['half'] = k; tr.append(x)
def buc(t):  # Bucharest = UTC+3 until 25 Oct 2026, then UTC+2
    return t + D.timedelta(hours=3 if t < D.datetime(2026, 10, 25, 1, tzinfo=D.timezone.utc) else 2)
print(len(tr), 'trades', round(sum(x['R'] for x in tr), 1), 'R')
by = {}
for x in tr: by.setdefault(buc(x['t']).hour // 4 * 4, []).append(x)
for h in sorted(by):
    s = by[h]; h0 = sum(x['R'] for x in s if x['half'] == 0); h1 = sum(x['R'] for x in s if x['half'] == 1)
    print(f"  fill candle {h:02d}:00-{h+4:02d}:00  {len(s):3}tr  {h0:+5.1f} / {h1:+5.1f} = {h0+h1:+5.1f}R  avg {St.mean(x['R'] for x in s):+.2f}  win {sum(x['R']>0 for x in s)/len(s):.0%}")
b0 = evalP({}, trend=False)
# hours filter in the sim applies to the SIGNAL candle (b['hl'] = its Bucharest open hour); the C order fills in the next candle
for n, hrs in [('all hours', None), ('no fills 00-04 (signal candle 20-24 skipped)', (0, 20)), ('signals 04-20 only (fills 08-24)', (4, 20)), ('signals 00-16 (fills 04-20)', (0, 16))]:
    line('  ' + n, evalP({**SH, 'hours': hrs}), b0)
