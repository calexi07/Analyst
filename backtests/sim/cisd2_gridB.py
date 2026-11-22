# Stage B: around the best stage-A configurations, vary the remaining indicator settings.
import sys, os, itertools, json, multiprocessing as MP
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cisd2_grid import ev, TFS, TPS
BASES = {
 '15m': [dict(entry='fvgC', stop='piv', entryMode='Market', be=False, _tp='TP4'), dict(entry='ifXHL', stop='piv', entryMode='Market', be=False, _tp='TP4'),
         dict(entry='fvgCE', stop='brk', entryMode='Market', be=False, _tp='TP4')],
 '30m': [dict(entry='obXC', stop='cross', entryMode='Market', be=False, _tp='liq1.5R'), dict(entry='obXC', stop='cross', entryMode='Market', be=False, _tp='TP4')],
 '1H':  [dict(entry='obXC', stop='cross', entryMode='Market', be=True, _tp='liqNear'), dict(entry='obXC', stop='cross', entryMode='Market', be=False, _tp='liq1.5R'),
         dict(entry='fvgCE', stop='ifvg', entryMode='Market', be=True, _tp='liq1.5R')],
}
VAR = dict(disp=[0.3, 0.5, 0.7], piv=[2, 3, 5], waitClose=[False, True], pd=['Off', 'HTF range'], kz=[(), ('london', 'nyam')],
           sweep=['prev+any', 'any', 'prev', 'prev+any+body'], risk=[(0.25, 3.0), (0.25, 6.0), (0.5, 3.0)])
if __name__ == '__main__':
    tfs = sys.argv[1].split(','); J = []
    for tf in tfs:
        for base in BASES[tf]:
            for disp, piv, wc, pd, kz, sw, rk in itertools.product(*VAR.values()):
                P = {k: v for k, v in base.items()}; P.update(TPS[base['_tp']])
                P.update(disp=disp, piv=piv, waitClose=wc, pd=pd, kz=kz, minRisk=rk[0], maxRisk=rk[1],
                         sweepPrev='prev' in sw, sweepAny='any' in sw, sweepBody='body' in sw)
                P['_sw'] = sw; J.append((tf, P))
    with MP.Pool(2) as pool: R = pool.map(ev, J, chunksize=40)
    json.dump(R, open(f'/tmp/cisdB_{"_".join(tfs)}.json', 'w')); print(len(R), 'runs')
