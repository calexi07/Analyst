# Quasimodo on EURUSD 5m / 15m / 30m / 1H, bias weeks W40-W47 only (engine bias direction).
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qm, ltf
from smc import prep, B, H
from harness import B1
B.clear(); B.update(B1)
import harness as _hh; h1 = _hh.D1['EURUSD']   # real 1H (prep() is patched to 4H once smc_3y is imported)
DATA = {'5m': ltf.load('EURUSD', '5'), '15m': ltf.load('EURUSD', '15'), '30m': ltf.load('EURUSD', '30'), '1H': h1}
CTX = {k: ltf.struct_ctx(h1, v) for k, v in DATA.items()}
def ev(tf, P):
    hs = [qm.run('EURUSD', DATA[tf], P, a, c) for a, c in H]
    t = sorted(hs[0] + hs[1], key=lambda x: x['tx']); eq = pk = dd = 0
    for x in t: eq += x['R']; pk = max(pk, eq); dd = min(dd, eq - pk)
    n = max(1, len(t))
    return f"{len(t):3}tr {len(t) / 8:.1f}/wk win {sum(x['R'] > 0 for x in t) / n:.0%} {eq / n:+.2f}R/tr | {sum(x['R'] for x in hs[0]):+5.1f}/{sum(x['R'] for x in hs[1]):+5.1f} = {eq:+5.1f}R dd {dd:+4.1f}"
V = [('shoulder limit, TP2', dict(tpR=2)), ('shoulder limit, TP3', dict(tpR=3)),
     ('shoulder limit, no +1R cancel, TP2', dict(tpR=2, cancel1R=False)), ('shoulder limit, no cancel, TP3', dict(tpR=3, cancel1R=False)),
     ('half way shoulder-break, TP2', dict(entry='half', tpR=2, cancel1R=False)), ('half way, TP3', dict(entry='half', tpR=3, cancel1R=False)),
     ('market at the break, TP2', dict(entry='break', tpR=2)), ('market at the break, TP3', dict(entry='break', tpR=3)),
     ('break TP2, risk <= 6 ATR', dict(entry='break', tpR=2, maxR=6)), ('break TP3 + 1H structure', dict(entry='break', tpR=3, ctx='1h')),
     ('shoulder no cancel TP3 + 1H structure', dict(tpR=3, cancel1R=False, ctx='1h')), ('break TP2, 06-22', dict(entry='break', tpR=2, hours=(6, 22))),
     ('L5 break TP3', dict(L=5, entry='break', tpR=3)), ('L5 shoulder no cancel TP3', dict(L=5, tpR=3, cancel1R=False)),
     ('break TP2, no bias', dict(entry='break', tpR=2, bias=False))]
for tf in ['5m', '15m', '30m', '1H']:
    print('==', tf)
    for n, P in V:
        P = dict(P); P['ctx'] = CTX[tf] if P.get('ctx') == '1h' else None
        print(f"  {n:<34} {ev(tf, P)}", flush=True)
