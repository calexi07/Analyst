from ideas import *
import time
T0 = time.time()
for p in ['EURUSD', 'GBPUSD', 'XAUUSD']:
    load(p); print(f"\n######## {p}  (loaded {time.time()-T0:.0f}s)")
    for dm in ['trend', 'both']:
        for tp in [1.5, 2, 3]:
            print(summary(run(p, 'asia_sweep', dict(dir=dm, w0=480, w1=720, tp=tp)), f"asia_sweep 08-12 {dm} tp{tp}"))
        print(summary(run(p, 'asia_sweep', dict(dir=dm, w0=480, w1=720, tp='opp')), f"asia_sweep 08-12 {dm} tp opp"))
        for tp in [1.5, 2, 3]:
            print(summary(run(p, 'pd_sweep', dict(dir=dm, w0=540, w1=1080, tp=tp)), f"pd_sweep 09-18 {dm} tp{tp}"))
        for tp in [2, 3]:
            print(summary(run(p, 'ema_pb', dict(dir=dm, w0=540, w1=1080, tp=tp)), f"ema_pb 09-18 {dm} tp{tp}"))
        for (r0, r1, u, nm) in [(540, 600, 780, 'EU 9-10'), (480, 540, 720, 'LON 8-9'), (930, 960, 1080, 'NY 15:30-16')]:
            for tp in [2, 3]:
                print(summary(run(p, 'orb', dict(dir=dm, r0=r0, r1=r1, until=u, tp=tp)), f"orb {nm} {dm} tp{tp}"))
        for (m0, m1) in [(540, 720), (480, 900)]:
            for f in [0.3, 0.5]:
                print(summary(run(p, 'mom', dict(dir=dm, m0=m0, m1=m1, f=f, s=0.3, tp=2)), f"mom {m0//60}-{m1//60} f{f} {dm}"))
print(f"done {time.time()-T0:.0f}s")
