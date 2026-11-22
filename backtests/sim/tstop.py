# BE Intraday: does the 4h time stop hurt? tmax (5m bars) × TP, same entries
import sys, datetime as D, statistics as st
import intraday as T
UTC = D.timezone.utc
CF = [('EURUSD', 'EU ORB · bias', dict(idea='orb', r0=540, r1=600, until=780, dirm='bias')),
      ('GBPUSD', 'EU ORB · bias', dict(idea='orb', r0=540, r1=600, until=780, dirm='bias')),
      ('GBPUSD', 'NY ORB · bias', dict(idea='orb', r0=930, r1=960, until=1080, dirm='bias')),
      ('XAUUSD', 'EU ORB · bias', dict(idea='orb', r0=540, r1=600, until=780, dirm='bias')),
      ('XAUUSD', 'NY ORB · bias', dict(idea='orb', r0=930, r1=960, until=1080, dirm='bias')),
      ('XAUUSD', 'EMA20 pb TP3 · bias', dict(idea='ema_pb', dirm='bias', tp=3.0, start=(9, 0), last=(18, 0))),
      ('GER40', 'US ORB · SMA20 trend', dict(idea='orb', r0=990, r1=1020, until=1140, dirm='trend'))]
TM = [('2h', 24), ('3h', 36), ('4h', 48), ('5h', 60), ('6h', 72), ('8h', 96), ('day end', 999)]
for p, name, P in CF:
    data = T.prep(p); b5 = data[0]; a, c = b5[0]['t'], b5[-1]['t'] + D.timedelta(minutes=5)
    mid = a + (c - a) / 2
    print(f"\n== {p} · {name} · {b5[0]['t']:%d %b} – {b5[-1]['t']:%d %b}")
    for tp in ([P['tp']] if 'tp' in P else [2.0, 3.0, 99]):
        row = []
        for lab, tm in TM:
            r = T.run(p, data, {**P, 'tp': tp, 'tmax': tm}, a, c)
            R = [x['R'] for x in r]; h1 = sum(x['R'] for x in r if x['t'] < mid); h2 = sum(R) - h1
            row.append(f"{lab:>7}: {sum(R):+5.1f}R ({len(R)}tr, {h1:+.1f}/{h2:+.1f})")
        print(f"  TP {'none' if tp == 99 else tp:>4}  " + " | ".join(row[:4]) + "\n            " + " | ".join(row[4:]))
