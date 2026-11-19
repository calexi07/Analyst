# Reference implementation of TradingView posts, Week 46 (see claude/prompts/TV_POSTS.md).
# Part 1: daily.py (daily notes). Part 2: build_tv2.py (weekly ideas + page). Inputs: archive/dobs-YYYY-Www-final.json.
# ===== daily.py =====
import datetime
DAY = datetime.date(2026, 11, 11)  # note written from Check 11 (Tue 10 Nov end-of-day), for Wed 11 Nov
DAYLBL = "Wed 11 Nov"
EM = dict(USD='💵',EUR='💶',GBP='💷',JPY='💴',CHF='🏔️',CAD='🛢️',AUD='🦘',NZD='🥝',XAU='🥇')
CHG = {
 'USD': "The plot thickened for the dollar. October CPI came in hot (core +0.3% vs +0.2% expected) and Fed Governor Waller said even a 50bp hike should be on the table. Our shadow score ticks up from +7 to +8.",
 'JPY': "The Bank of Japan's meeting summary (10 Nov) leaned hawkish. If markets price a December hike the way one measure already does (~80%), the yen could be much stronger than its +2 (up to +6 in our shadow math). Still unresolved.",
 'CAD': "The Bank of Canada's meeting notes said rates may need to go higher, but carefully, one meeting at a time. It fits the story we already had, so no change.",
 'XAU': "The hot US CPI is exactly gold's enemy: it pushes real yields up. Gold's own score could slip from +7 to around +4. Still positive, but the shine is under pressure.",
 'EUR': "Quiet day for the euro. No new French headlines that change the story.",
 'GBP': "Quiet before the storm. UK Q3 GDP lands Thursday 12 Nov.",
 'CHF': "Quiet day. The franc's tug-of-war continues, nothing new to tip it.",
 'AUD': "Quiet day. Nothing new that moves the needle for the Aussie.",
 'NZD': "Quiet day. Next real test is the dairy auction on 17 Nov.",
}
NEXT = {
 'USD': "Fri 13 Nov: US PPI (October)", 'XAU': "Fri 13 Nov: US PPI (October)",
 'EUR': "Fri 13 Nov: Euro-area Q3 GDP + Fitch Germany / S&P Italy ratings",
 'GBP': "Thu 12 Nov: UK Q3 GDP (first estimate)",
 'JPY': "Any fresh pricing of a December BoJ hike",
 'CAD': "Fri 13 Nov: IEA oil market report",
 'CHF': "Risk mood: a deeper sell-off helps the franc",
 'AUD': "Risk mood and China headlines",
 'NZD': "Tue 17 Nov: Global Dairy Trade auction",
}
SHADOW = {'USD': 8}
STRONGER = {'EURUSD','GBPUSD','USDCHF','USDCAD','AUDUSD','NZDUSD'}
JPYUP = {'EURJPY','GBPJPY','NZDJPY','CADJPY'}
JPYWATCH = {'AUDJPY','CHFJPY'}
FRAGILE = {'EURCHF','EURAUD','EURCAD','GBPCHF','GBPAUD','GBPCAD','AUDNZD','NZDCHF','NZDCAD'}
STAT = {
 'stronger': ("✅ CONFIRMED · getting stronger", "The story is holding, and today it got louder."),
 'jpyup': ("✅ CONFIRMED · could get even stronger", "The story is holding. A plot twist in Tokyo could even make it stronger."),
 'usdjpy': ("👀 UNDER WATCH", "Both characters in this story got louder today. Who wins the shouting match?"),
 'jpywatch': ("👀 UNDER WATCH · could turn bearish", "No edge yet, but Tokyo might be writing one."),
 'xau': ("⚠️ UNDER PRESSURE · still bullish", "Gold's biggest enemy showed up today. The story bends, but it hasn't broken."),
 'fragile': ("🟡 CONFIRMED · but fragile", "The story still holds, but the margin is thin. One headline could tip it."),
 'two': ("⚪ STILL TWO-SIDED", "Still a stand-off. Nobody blinked today."),
 'ok': ("✅ CONFIRMED", "Nothing in today's news changes the plot. The story holds."),
}
def kind(pair, bias):
    if pair in STRONGER: return 'stronger'
    if pair in JPYUP: return 'jpyup'
    if pair == 'USDJPY': return 'usdjpy'
    if pair in JPYWATCH: return 'jpywatch'
    if pair == 'XAUUSD': return 'xau'
    if pair in FRAGILE: return 'fragile'
    if bias == 'two-sided': return 'two'
    return 'ok'
def sg(n): return f"+{n}" if n > 0 else ("0" if n == 0 else f"−{abs(n)}")
def read_line(pair, b, q, bs, qs):
    gap = bs - qs
    if pair == 'XAUUSD': return f"Published gap {sg(gap)} → today's read {'+4 to +7'} (gold's own score)"
    if 'JPY' in (b, q):
        base = SHADOW.get(b, bs); quote = SHADOW.get(q, qs)
        g2 = (base - 2) if q == 'JPY' else (2 - quote)
        g6 = (base - 6) if q == 'JPY' else (6 - quote)
        return f"Published gap {sg(gap)} → today's read {sg(g2)} (yen +2) or {sg(g6)} (yen +6)"
    g = SHADOW.get(b, bs) - SHADOW.get(q, qs)
    return f"Published gap {sg(gap)} → today's read {sg(g)}" + ("" if g != gap else " (unchanged)")
def daily_posts(D, SEP):
    out = []
    for p in D['pairs']:
        pair, b, q = p['pair'], p['pair'][:3], p['pair'][3:]
        k = kind(pair, p['bias']); st, hook = STAT[k]
        bias = p['bias'].upper() if p['bias'] != 'two-sided' else 'TWO-SIDED'
        nxt = []
        for c in (b, q):
            if NEXT[c] not in nxt: nxt.append(NEXT[c])
        parts = [
            f"[b]📍 DAILY CHECK · {DAYLBL}[/b]",
            hook,
            f"[quote][b]{st}[/b]\nWeek bias: {bias} · {EM[b]} {b} {sg(p['base_score'])} vs {EM[q]} {q} {sg(p['quote_score'])}\n{read_line(pair,b,q,p['base_score'],p['quote_score'])}[/quote]",
            "📸 >>> PASTE CHART HERE <<<",
            SEP,
            "[b]🔄 WHAT CHANGED[/b]\n[list]\n" + f"[*]{EM[b]} {b}: {CHG[b]}\n[*]{EM[q]} {q}: {CHG[q]}\n[/list]",
            "[b]👀 NEXT UP[/b]\n[list]\n" + "".join(f"[*]{x}\n" for x in nxt) + "[/list]",
            "[i]⚠️ Fundamental check, not a trade signal.[/i]",
        ]
        out.append(dict(pair=pair, status=st, text="\n\n".join(parts), cls={'stronger':'bull','jpyup':'bull','ok':'bull','fragile':'neu','two':'neu'}.get(k,'bear')))
    return out

# ===== build_tv2.py =====
import json, html, datetime, re

D = json.load(open('/home/claude/w46/p2/dobs-2026-W46-final.json'))
W = D['valid_week']['week']
WEEK_DATES = "9–13 Nov 2026"
TODAY = datetime.date(2026, 11, 11)

# Storytelling version. Every number comes from the W46 FINAL vintage/JSON or the checks-log (Checks 7–11).
SHORT = dict(USD='Comeback kid', EUR='French headache', GBP='Warning-label hike', JPY='Quiet safe harbour',
             CHF='Calm tug-of-war', CAD='Perfect storm', AUD='Lost swagger', NZD='Missing feathers', XAU='Safe-haven moment')
C = {
 'USD': dict(short=SHORT['USD'], flag='💵', oldflag='🇺🇸', title='The comeback kid',
   hook='The dollar walks into this week with its chest out.',
   story="A month ago the dollar looked tired. Then the data started punching back. October payrolls landed at +165k, way above what anyone expected, and suddenly the Fed doesn't look done hiking. Markets give a December hike roughly a 75–78% chance... and here's the part we're watching: we think they may still be pricing too little. Add a nervous, risk-off market where investors run for safety, and the greenback has the wind at its back.",
   up='Hot inflation and Fed speakers backing a December hike',
   down='Soft core inflation (under 0.2% m/m) or Fed speakers cooling the December talk',
   update="Fresh twist (11 Nov): October CPI came in hot, core +0.3% vs +0.2% expected, and Fed Governor Waller even floated a bigger 50bp hike. The dollar's story just got louder."),
 'EUR': dict(short=SHORT['EUR'], flag='💶', oldflag='🇪🇺', title='The French headache',
   hook='The euro is walking around with a heavy French backpack.',
   story="The euro's problem this week isn't Frankfurt. It's Paris. Investors want about 1.54 percentage points more to hold French 10-year bonds than German ones (the OAT–Bund spread, ~154bp). Think of it as the market's stress meter, and it's flashing. The French budget still has to survive the Senate (votes 20–23 Nov), and S&P reviews France's rating on 27 Nov. Meanwhile the ECB is already expected to hike 2–3 times, so the good news is mostly baked in. Little room for a happy surprise, plenty of room for scary headlines.",
   up='The spread falling back below ~130bp, or the Senate defusing the budget fight',
   down='The spread breaking above its 3 Nov peak (161.8bp)',
   update=None),
 'GBP': dict(short=SHORT['GBP'], flag='💷', oldflag='🇬🇧', title='The hike with a warning label',
   hook='The pound got the rate hike it wanted, and then it read the fine print.',
   story="The Bank of England raised rates to 4.00%. Sounds bullish, right? Not so fast. In the same breath, the BoE warned it doesn't want a long run of hikes. The problem: markets still price about 3 more. When the central bank says \"easy\" and the market says \"more\", the market usually has to back down. And the nervous risk mood isn't doing sterling any favours either.",
   up='A strong UK Q3 GDP (12 Nov) or BoE members backing more hikes',
   down='Weak Q3 GDP or BoE members talking about a pause',
   update=None),
 'JPY': dict(short=SHORT['JPY'], flag='💴', oldflag='🇯🇵', title='The safe harbour with a secret',
   hook="The yen is the quiet one in the corner, but everyone keeps glancing at it.",
   story="When markets get nervous, money runs to the yen, and right now markets are nervous. Tokyo has also warned it could step in to stop the yen falling, which keeps sellers on their toes. The secret everyone is arguing about: will the Bank of Japan hike in December? One market measure says ~80%, another only 56%. Same question, two very different answers.",
   up='A clear Bank of Japan signal for December',
   down='A calmer market where carry trades come back',
   update="Fresh twist (11 Nov): the BoJ Summary of Opinions (10 Nov) leaned hawkish. Depending on how markets reprice December, the yen could be stronger than its score shows."),
 'CHF': dict(short=SHORT['CHF'], flag='🏔️', oldflag='🇨🇭', title='Zero interest, full safety',
   hook='The Swiss franc is stuck in a tug-of-war with itself.',
   story="On one side, the franc pays zero interest. Not exactly exciting. On the other side, when fear rises, the franc is where investors hide. This week both forces pull equally hard, so the franc sits right in the middle of the pack. No drama, but don't mistake calm for weakness.",
   up='Deeper risk-off, or markets starting to price an SNB hike',
   down='A fast return of optimism',
   update=None),
 'CAD': dict(short=SHORT['CAD'], flag='🛢️', oldflag='🇨🇦', title='Everything hitting at once',
   hook='The Canadian dollar is having the worst week in our whole line-up.',
   story="Ever had one of those weeks where everything goes wrong? That's the loonie. Oil, Canada's lifeline, is down about 6% in four weeks. Canada lost 4.7k jobs when economists expected +13.6k. The US tariff threat is still hanging over it. And a nervous market is bad news for commodity currencies. Put it all together and CAD carries the weakest score in our model (−6).",
   up='Oil climbing back above its 9 Oct level, or a US–Canada tariff deal',
   down='More oil weakness or tariff escalation',
   update="Side note (11 Nov): the Bank of Canada's meeting notes (10 Nov) said rates may need to go higher, but carefully, one meeting at a time. Not enough to change the plot."),
 'AUD': dict(short=SHORT['AUD'], flag='🦘', oldflag='🇦🇺', title='Top carry, lost its edge',
   hook='The Aussie still has the best interest rate in the room, but it just lost its swagger.',
   story="Australia still pays the highest interest rate of the eight. The catch? The RBA just dropped its bias to hike (a split 6–3 vote), and markets now even price small cuts over the next year. When the \"next move is up\" story disappears, a high-yielder loses its magnet. Add a risk-off mood, which usually hits the Aussie, and only a small lift from iron ore (+3%). Net result: dead even.",
   up='Strong China data and a calmer market',
   down='Weak China data or deeper risk-off',
   update=None),
 'NZD': dict(short=SHORT['NZD'], flag='🥝', oldflag='🇳🇿', title='Jobs wobble, dairy cushion',
   hook='The kiwi is trying to fly with a few feathers missing.',
   story="New Zealand's unemployment rose to 5.7% (5.5% expected). Not the headline you want. The nervous market mood weighs on it too. The cushion? Dairy, the country's big export, is up 5.6%. Politics is the side plot: the election gave the right-leaning bloc 68 of 131 seats, with the official result due 27 Nov.",
   up='A better risk mood, or dairy prices rising again at the 17 Nov auction',
   down='Stalled coalition talks, or weaker dairy prices',
   update=None),
 'XAU': dict(short=SHORT['XAU'], flag='🥇', oldflag='🥇', title="The safe haven's moment",
   hook='Gold is having the kind of week every safe haven dreams about.',
   story="Fear is in the air, and gold loves fear. Investors want protection, and central banks and gold ETFs keep buying. Gold's own score is +7, one of the strongest reads in our whole model. Its one real enemy is a hawkish Fed: when US real yields climb, holding a metal that pays no interest gets more expensive.",
   up='Real yields falling, or haven demand growing',
   down='Hot US inflation lifting real yields, or ETF outflows',
   update="Fresh twist (11 Nov): the hot US CPI is exactly gold's enemy, because it pushes real yields up. The model still leans bullish (gold-only score between +4 and +7), but this is the risk to watch."),
}

def lc(s): return s if s[:3].isupper() and s[:2]!="Ho" and s[:2]!="Th" else s[0].lower()+s[1:]
def sgn(n): return f"+{n}" if n > 0 else ("0" if n == 0 else f"−{abs(n)}")
news = [n for n in D['news'] if datetime.date.fromisoformat(n['date']) >= TODAY and n['importance'] in ('HIGH','CRITICAL','MEDIUM')]
def dates_for(a, b):
    seen, out = set(), []
    for n in news:
        if n['currency'] in (a, b) and n['event'] not in seen:
            seen.add(n['event']); out.append(n)
    out.sort(key=lambda n: n['date'])
    return out[:5]
def fmt_date(s): return datetime.date.fromisoformat(s).strftime('%a %d %b').replace(' 0', ' ')

LEAN = {'high': "This is one of the clearest stories on our board this week.",
        'medium': "The story leans one way, but not without a fight.",
        'low': "There's a lean here, but a gentle one. Don't expect fireworks from the fundamentals alone."}

SEP = "━━━━━━━━━━━━━━━━━━"
BIASE = {'bullish':'🟢','bearish':'🔴','two-sided':'🟡'}
CONVE = {'high':'🔥🔥🔥 High conviction','medium':'🔥🔥 Medium conviction','low':'🔥 Low conviction'}
def chapter(n, code, score):
    c = C[code]
    t = f"[b]{c['flag']} CHAPTER {n} · {code} · {c['title']}[/b]\n[i]Score {sgn(score)}[/i]\n{c['story']}"
    pass  # weekly post = Monday snapshot; mid-week news goes only in daily notes
    return t

posts = []
for p in D['pairs']:
    pair, b, q = p['pair'], p['pair'][:3], p['pair'][3:]
    bs, qs = p['base_score'], p['quote_score']; gap = bs - qs
    bias, conv = p['bias'], p['conviction']
    if bias == 'two-sided':
        title = f"{pair}: {C[b]['short']} vs {C[q]['short']} | W{W}"
        opening = f"Sometimes the honest answer is: nobody has the upper hand. {C[b]['hook']} {C[q]['hook']} Put them on the same chart and you get {pair} this week: a stand-off. 🤝"
        head = f"{BIASE[bias]} Week {W} bias: TWO-SIDED  |  no clear edge"
        verdict = "Two-sided: no clear fundamental edge"
    else:
        fav, weak = (b, q) if gap > 0 else (q, b)
        title = f"{pair}: {C[fav]['short']} vs {C[weak]['short']} | W{W}"
        opening = f"{C[fav]['hook']} {C[weak]['hook']} Put those two on the same chart and you get {pair}. {LEAN[conv]}"
        head = f"{BIASE[bias]} Week {W} bias: {bias.upper()} ({fav} favoured)  |  {CONVE[conv]}"
        verdict = f"{bias.capitalize()} ({fav} favoured), {conv} conviction"
    dl = dates_for(b, q)
    parts = [
        f"$FOREXCOM:{pair}",
        f"[b]🎬 {C[b]['short']} vs {C[q]['short']}[/b]",
        opening,
        f"[quote][b]{head}[/b]\n{C[b]['flag']} {b} {sgn(bs)}  vs  {C[q]['flag']} {q} {sgn(qs)}   (scale −18 to +18, gap {sgn(gap)})\n🗓️ {WEEK_DATES}[/quote]",
        "📸 >>> PASTE CHART HERE <<<",
        SEP,
        chapter(1, b, bs),
        SEP,
        chapter(2, q, qs),
        SEP,
        "[b]⚡ PLOT TWIST: what could flip the story[/b]\n[list]\n"
          + f"[*]🟢 {b} stronger if: {lc(C[b]['up'])}\n[*]🔴 {b} weaker if: {lc(C[b]['down'])}\n"
          + f"[*]🟢 {q} stronger if: {lc(C[q]['up'])}\n[*]🔴 {q} weaker if: {lc(C[q]['down'])}\n[/list]",
        "[b]📅 DATES TO CIRCLE[/b]\n" + ("[list=1]\n" + "".join(f"[*]{fmt_date(n['date'])}: {n['event']} ({n['currency']})\n" for n in dl) + "[/list]" if dl else "No big scheduled events for this pair for the rest of the week."),
        SEP,
        "[b]🗳️ Your turn:[/b] which side of the story are you on? Tell me in the comments 👇",
        "[i]⚠️ This is my fundamental bias, not a trade signal. The story tells me which side to favour; the chart tells me when.[/i]",
    ]
    strat = 'Neutral' if (bias == 'two-sided' or conv == 'low') else ('Long' if bias == 'bullish' else 'Short')
    TH = dict(USD='fed', EUR='ecb', GBP='boe', JPY='boj', CHF='snb', CAD='oil', AUD='rba', NZD='rbnz', XAU='gold')
    tags = ['fundamentalanalysis'] + (['gold','usd','fed','safehaven'] if pair=='XAUUSD' else ['forex', b.lower(), q.lower(), TH[b], TH[q]])
    posts.append(dict(strat=strat, tags=', '.join(tags), pair=pair, title=title, text="\n\n".join(parts), cls={'bullish':'bull','bearish':'bear'}.get(bias,'neu'), verdict=verdict))

from daily import daily_posts, DAYLBL
DAILY = daily_posts(D, SEP)
def bb2html(t):
    h = html.escape(t)
    h = re.sub(r'\[list=1\]\n?(.*?)\[/list\]', lambda m: '<ol>' + ''.join(f'<li>{x.strip()}</li>' for x in m[1].split('[*]') if x.strip()) + '</ol>', h, flags=re.S)
    h = re.sub(r'\[list\]\n?(.*?)\[/list\]', lambda m: '<ul>' + ''.join(f'<li>{x.strip()}</li>' for x in m[1].split('[*]') if x.strip()) + '</ul>', h, flags=re.S)
    for a, b_ in (('b','b'),('i','i'),('s','s')): h = h.replace(f'[{a}]', f'<{b_}>').replace(f'[/{a}]', f'</{b_}>')
    h = h.replace('[quote]', '<blockquote>').replace('[/quote]', '</blockquote>')
    h = re.sub(r'\n(?=\s*<(ol|ul|/ol|/ul|li))', '', h)
    return h.replace('\n', '<br>')

e = html.escape
for x in posts:
    assert len(x['title']) <= 58, (x['pair'], len(x['title']))
dd_js = json.dumps([x['text'] for x in DAILY], ensure_ascii=False).replace('</', '<\\/')
data_js = json.dumps([{k: x[k] for k in ('title','text','tags')} for x in posts], ensure_ascii=False).replace('</', '<\\/')
dcards = "\n".join(f'''<section class="card" data-pair="{x['pair']}">
 <div class="ch"><h2>{x['pair']}</h2><span class="tag {x['cls']}">{e(x['status'])}</span></div>
 <div class="btns"><button class="pri" onclick="cpd({i},this)">Copy note</button></div>
 <details><summary>Preview (how it will look)</summary><div class="post">{bb2html(x['text'])}</div></details>
</section>''' for i, x in enumerate(DAILY))
cards = "\n".join(f'''<section class="card" data-pair="{x['pair']}" id="{x['pair']}">
 <div class="ch"><h2>{x['pair']}</h2><span class="tag {x['cls']}">{e(x['verdict'])}</span></div>
 <div class="lbl">Title</div><div class="title">{e(x['title'])}</div>
 <div class="btns"><button onclick="cp({i},'title',this)">Copy title</button><button class="pri" onclick="cp({i},'text',this)">Copy post</button></div>
 <div class="ft"><div><span class="lbl">Final touches</span></div>
 <div>Type: <b>Analysis</b> · Strategy: <b class="s-{x['strat'].lower()}">{x['strat']}</b> · Category: <b>Fundamental analysis</b></div>
 <div>Tags: <code>{x['tags']}</code> <button class="sm" onclick="cp({i},'tags',this)">Copy tags</button></div>
 <div class="hint">Related idea: last week's {x['pair']} idea (from next week on)</div></div>
 <details><summary>Preview (how it will look)</summary><div class="post">{bb2html(x['text'])}</div></details>
</section>''' for i, x in enumerate(posts))

page = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>TradingView Ideas — Week {W}</title>
<style>
:root{{--bg:#0f1115;--card:#171a21;--line:#2a2f3a;--ink:#e8eaed;--sub:#9aa3ad;--bull:#2fbf71;--bear:#ef5350;--neu:#d4a72c;--acc:#2962ff}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 -apple-system,Segoe UI,Roboto,sans-serif}}
.wrap{{max-width:760px;margin:0 auto;padding:18px 14px 60px}}h1{{font-size:20px;margin:0 0 4px}}.meta{{color:var(--sub);font-size:13px}}
.note{{background:#1d2230;border-left:3px solid var(--acc);padding:10px 12px;border-radius:6px;font-size:13.5px;margin:14px 0}}
input{{width:100%;padding:10px 12px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--ink);font-size:15px;margin:6px 0 14px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px;margin:12px 0}}
.ch{{display:flex;justify-content:space-between;align-items:center;gap:8px}}.ch h2{{margin:0;font-size:18px}}
.tag{{font-size:12px;font-weight:700;padding:3px 9px;border-radius:12px;text-align:right}}
.tag.bull{{background:#123323;color:var(--bull)}}.tag.bear{{background:#3a1717;color:var(--bear)}}.tag.neu{{background:#352c10;color:var(--neu)}}
.lbl{{color:var(--sub);font-size:11px;text-transform:uppercase;margin-top:10px}}.title{{font-weight:600}}

.tabs{{display:flex;gap:8px;margin:12px 0 4px}}.tabs button{{flex:1}}
.ft{{background:#11141a;border:1px dashed var(--line);border-radius:8px;padding:8px 10px;margin:6px 0 10px;font-size:13.5px}}.ft code{{color:#cfd3d8;font-size:12.5px}}.ft .hint{{color:var(--sub);font-size:12px}}button.sm{{padding:4px 9px;font-size:12px;margin-left:4px}}.s-long{{color:var(--bull)}}.s-short{{color:var(--bear)}}.s-neutral{{color:var(--neu)}}
.btns{{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0}}
button{{background:#232836;color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:9px 14px;font-size:14px;cursor:pointer}}
button.pri{{background:var(--acc);border-color:var(--acc);color:#fff;font-weight:600}}button.ok{{background:var(--bull);border-color:var(--bull);color:#04130a}}
summary{{cursor:pointer;color:var(--sub);font-size:13.5px}}
.post{{background:#000;border:1px solid var(--line);border-radius:8px;padding:12px;margin-top:8px;font-size:14px}}
.post blockquote{{border-left:3px solid #666;margin:4px 0;padding:4px 10px;color:#cfd3d8}}.post ul,.post ol{{margin:4px 0;padding-left:20px}}
</style></head><body><div class="wrap">
<h1>TradingView Ideas — Week {W}</h1>
<div class="meta">Story versions of the Forex Fundamental Bias Engine, Week {W} FINAL (8 Nov 2026). Weekly ideas = start-of-week snapshot; mid-week news appears only in the daily notes. 29 pairs.</div>
<div class="note"><b>How to use:</b> <b>Copy title</b> → paste in the title field. <b>Copy post</b> → paste in the text box. The post uses TradingView's own tags ([b], [i], [list], [quote]), so TradingView formats it when you publish. The first line is the ticker ($FOREXCOM:PAIR); change the broker prefix if you use another feed. Each card also shows what to pick on the <b>Final touches</b> screen: Strategy follows the bias (Neutral for two-sided and low-conviction pairs). Replace the line <b>📸 &gt;&gt;&gt; PASTE CHART HERE &lt;&lt;&lt;</b> with your chart (TradingView snapshot link or image); copy that line wherever you want more charts.</div>
<div class="tabs"><button id="t1" class="pri" onclick="tab(1)">📰 Weekly ideas</button><button id="t2" onclick="tab(2)">📍 Daily notes · {DAYLBL}</button></div>
<input id="f" placeholder="Filter, e.g. EUR, JPY, XAU…" oninput="flt()">
<div id="wk">{cards}</div>
<div id="dy" style="display:none"><div class="note">Short daily update for each pair, to add as a <b>note</b> under the week's idea (Add note → paste). Based on the latest daily check (end of Tue 10 Nov). Same tags and the same chart placeholder.</div>{dcards}</div>
</div>
<script>
const D={data_js};const DD={dd_js};
function cpd(i,b){{const t=DD[i];if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(t).then(()=>done(b,'Copied ✓'),()=>fallback(t,b));else fallback(t,b)}}
function tab(n){{document.getElementById('wk').style.display=n==1?'':'none';document.getElementById('dy').style.display=n==2?'':'none';document.getElementById('t1').className=n==1?'pri':'';document.getElementById('t2').className=n==2?'pri':''}}
function done(b,t){{const o=b.textContent;b.textContent=t;b.classList.add('ok');setTimeout(()=>{{b.textContent=o;b.classList.remove('ok')}},1600)}}
function fallback(t,b){{const ta=document.createElement('textarea');ta.value=t;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();try{{document.execCommand('copy');done(b,'Copied ✓')}}catch(e){{done(b,'Copy failed')}}document.body.removeChild(ta)}}
function cp(i,k,b){{const t=D[i][k];if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(t).then(()=>done(b,'Copied ✓'),()=>fallback(t,b));else fallback(t,b)}}
function flt(){{const q=document.getElementById('f').value.trim().toUpperCase();document.querySelectorAll('.card').forEach(c=>c.style.display=!q||c.dataset.pair.includes(q)?'':'none')}}
</script></body></html>'''
open('/home/claude/w46/tv/TradingView_Ideas_Week46.html', 'w').write(page)
print(posts[0]['title']); print(posts[0]['text']); print(max(len(x['title']) for x in posts))
