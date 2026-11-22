from ideas import *
import collections
PAIRS = ['EURUSD','GBPUSD','XAUUSD','AUDUSD','USDCAD','USDCHF','USDJPY','EURGBP','EURJPY','EURCHF','GBPJPY','AUDJPY']
for (m0, m1, f, s, tp) in [(540, 720, 0.4, 0.3, 2), (540, 780, 0.4, 0.3, 2), (540, 780, 0.5, 0.5, 1), (540, 720, 0.5, 0.3, None)]:
    for dm in ['both', 'trend']:
        allt = []; print(f"\n=== mom {m0//60}-{m1//60} f{f} s{s} tp{tp} {dm}")
        for p in PAIRS:
            r = run2(p, 'mom', dict(dir=dm, m0=m0, m1=m1, f=f, s=s, tp=tp)); allt += r
            print("  " + summary(r, p))
        print("  " + summary(allt, "PORTFOLIO (12)"))
