# Post-hoc feature study on the sweep + bias trades (8 USD pairs, W40-47): which trade traits separate winners from losers
# in BOTH halves. News days come from the archived Daily Observer JSON (W44-47 only).
import sys, os, json, glob, datetime as D, statistics as S
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
exec(open('usd_sweep_research.py').read().split('b0 = evalP')[0])
h = json.load(open('../../pine/history.json')); CC = {(W['y'], W['w']): W['ccy'] for W in h['weeks']}
news = {}
for f in glob.glob('../../engine/archive/dobs-*-final.json'):
    for n in json.load(open(f))['news']:
        if n['importance'] in ('CRITICAL', 'HIGH'): news.setdefault(n['currency'], set()).add(n['date'])
tr = []
for k, (a, c) in enumerate(H):
    for p in USD:
        for x in run(p, data[p], B, BASE, a, c, usd): x['half'] = k; tr.append(x)
for x in tr:
    wk = x['wk']; cc = CC.get(wk, {}); prev = B.get((x['pair'], (wk[0], wk[1] - 1)), ('-',))[0]
    other = x['pair'].replace('USD', '') or 'XAU'
    x['usd_abs'] = abs(cc.get('USD', 0)); x['oth_abs'] = abs(cc.get(other, 0))
    x['fresh'] = prev != x['bias']; x['usd_side'] = 'USD long' if (x['d'] > 0) == x['pair'].startswith('USD') else 'USD short'
    loc = x['t'] + D.timedelta(hours=2); x['dow'] = (x['t'] + D.timedelta(hours=7 - 5)).weekday()
    days = {(x['t'] + D.timedelta(days=j)).strftime('%Y-%m-%d') for j in (0, 1)}
    x['news'] = None if wk[1] < 44 else bool(days & (news.get('USD', set()) | news.get(other, set())))
    x['hold_d'] = (x['tx'] - x['t']).total_seconds() / 86400
def grp(name, f):
    print(name)
    keys = sorted({f(x) for x in tr if f(x) is not None}, key=str)
    for k in keys:
        s = [[x['R'] for x in tr if f(x) == k and x['half'] == hf] for hf in (0, 1)]
        a = s[0] + s[1]
        print(f"   {str(k):<16} {len(a):3}tr  {sum(s[0]):+5.1f} / {sum(s[1]):+5.1f} = {sum(a):+5.1f}R  avg {S.mean(a):+.2f}  win {sum(r > 0 for r in a) / len(a):.0%}")
print(f"{len(tr)} trades, {sum(x['R'] for x in tr):+.1f}R")
grp('entry day', lambda x: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][x['dow']])
grp('USD side', lambda x: x['usd_side'])
grp('direction', lambda x: 'long' if x['d'] > 0 else 'short')
grp('|gap|', lambda x: None if x['gap'] is None else ('3-5' if abs(x['gap']) <= 5 else '6-8' if abs(x['gap']) <= 8 else '9+'))
grp('|USD score|', lambda x: '0-2' if x['usd_abs'] <= 2 else '3-5' if x['usd_abs'] <= 5 else '6+')
grp('|other leg score|', lambda x: '0-2' if x['oth_abs'] <= 2 else '3-5' if x['oth_abs'] <= 5 else '6+')
grp('bias new this week vs repeated', lambda x: 'new' if x['fresh'] else 'repeated')
grp('conviction', lambda x: x['conv'])
grp('sweep depth (ATR)', lambda x: '<0.1' if x['depth'] < 0.1 else '0.1-0.3' if x['depth'] < 0.3 else '0.3+')
grp('HIGH/CRITICAL news today/tomorrow (W44-47)', lambda x: x['news'])
grp('pair', lambda x: x['pair'])
