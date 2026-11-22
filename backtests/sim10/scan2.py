from ideas import *
for p in ['EURUSD', 'GBPUSD', 'XAUUSD']:
    print(f"\n######## {p}")
    for s in [0.2, 0.3]:
        print(summary(run2(p, 'random', dict(dir='both', s=s, tp=2)), f"RANDOM s{s} tp2"))
        print(summary(run2(p, 'random', dict(dir='trend', s=s, tp=2)), f"RANDOM trend s{s} tp2"))
    for idea in ['mom', 'fade']:
        for (m0, m1) in [(540, 660), (540, 720), (540, 780), (480, 720), (540, 930), (540, 990)]:
            for f in [0.3, 0.4, 0.5]:
                for s, tp in [(0.3, 2), (0.3, None), (0.5, 1)]:
                    for dm in ['both', 'trend']:
                        r = run2(p, idea, dict(dir=dm, m0=m0, m1=m1, f=f, s=s, tp=tp))
                        if len(r) > 60 and sum(x[1] for x in r) / len(r) > 0.08:
                            print(summary(r, f"{idea} {m0//60}:{m0%60:02d}-{m1//60}:{m1%60:02d} f{f} s{s} tp{tp} {dm}"))
