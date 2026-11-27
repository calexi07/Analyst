import pandas as pd, numpy as np, sys
P = sys.argv[1] if len(sys.argv) > 1 else 'EURUSD'
R = pd.read_csv(f'{P}_trades.csv')
R = R.drop_duplicates(subset=['t', 'dir', 'zone_tf'], keep='first')     # a 4H zone used by both 1H and 4H setups counts once
def st(v):
    v = v.dropna()
    if len(v) < 3: return f'n={len(v)}'
    t = v.mean() / (v.std(ddof=1) / np.sqrt(len(v)))
    return f'n={len(v):4d} avg {v.mean():+.3f}R win {100*(v>0).mean():3.0f}% t {t:+.1f}'
def yr(x, c='r_2R'): return ' | ' + ' '.join(f"{y}: {x[x.year==y][c].mean():+.2f} (n={len(x[x.year==y])})" for y in (2025, 2026))
print(f'{P}: {len(R)} unique zone touches, exit 2R\n')
print('ALL', st(R.r_2R), yr(R))
for name, m in [('Q2 zone born from a sweep (extreme took the 48-bar high/low)', R.sweep), ('Q2b sweep + close back inside (wick sweep)', R.sweep_back),
                ('Q1 liquidity taken before entering the zone (inducement)', R.ind), ('Q1 + Q2', R.ind & R.sweep), ('neither', ~R.ind & ~R.sweep)]:
    print(f'\n{name}\n  yes', st(R[m].r_2R), yr(R[m]), '\n  no ', st(R[~m].r_2R), yr(R[~m]))
print('\n-- other cuts (exit 2R) --')
R['age_b'] = pd.cut(R.age, [0, 6, 24, 72, 1e9], labels=['<6h', '6-24h', '1-3d', '>3d'])
R['size_b'] = pd.cut(R.zone_atr, [0, 1, 2, 4, 1e9], labels=['<1ATR', '1-2', '2-4', '>4'])
R['pos_b'] = pd.cut(R.pos, [-1e9, 25, 50, 75, 1e9], labels=['deep wrong side', 'wrong side', 'right side', 'deep right side'])
R['pos_ok'] = np.where(R.dir < 0, R.pos > 50, R.pos < 50)
for g in ['sess', 'age_b', 'size_b', 'dow', 'pro', 'p2', 'pos_ok', 'zone_tf']:
    print(f'  by {g}:')
    for k, x in R.groupby(g, observed=True): print(f'     {str(k):16s}', st(x.r_2R), yr(x))
