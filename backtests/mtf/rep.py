import pandas as pd, numpy as np, sys
P = sys.argv[1] if len(sys.argv) > 1 else 'EURUSD'
R = pd.read_csv(f'{P}_trades.csv')
R['cls'] = np.where(R.pillars == 3, 'A', np.where(R.pillars == 2, 'B', 'C'))
q = R[R.has_struct]                                  # quality: a structural target at >= 1.5R
q = q[~((~q.pro) & ~((q.zone_tf.isin(['D', '4H'])) & (q.test == 1)))]   # counter-trend only from a fresh D/4H zone
def st(x, c='r_struct'):
    v = x[c].dropna()
    if len(v) == 0: return '  n=0'
    t = v.mean() / (v.std(ddof=1) / np.sqrt(len(v))) if len(v) > 2 and v.std() > 0 else np.nan
    return f'n={len(v):4d}  avg {v.mean():+.3f}R  win {100*(v>0).mean():3.0f}%  total {v.sum():+7.1f}R  t {t:+.1f}'
print(f'== {P}: all zone touches (limit at the zone edge), no filters ==')
for c in ['r_2R', 'r_3R']: print(f'  exit {c[2:]:6s}', st(R, c))
print(f'\n== after the quality gate (structural target >= 1.5R, counter-trend only from fresh D/4H zone): {len(q)} ==')
for c in ['r_struct', 'r_2R', 'r_3R']: print(f'  exit {c[2:]:6s}', st(q, c))
for name, grp in [('class (technical pillars)', 'cls'), ('execution TF', 'tf'), ('zone TF', 'zone_tf'), ('pro-trend (D swing)', 'pro'), ('touch #', 'test'), ('year', 'year')]:
    print(f'\n-- by {name} (exit: structural target) --')
    for k, x in q.groupby(grp): print(f'  {str(k):6s}', st(x))
print('\n-- class A only, by year --')
for k, x in q[q.cls == 'A'].groupby('year'): print(f'  {k}', st(x), '| 2R:', st(x, 'r_2R'))
