# YouTube weekly outlook — Week 47, built 14 Nov 2026 from archive/vintage-2026-W47-phase1.json + dobs-2026-W47-phase1.json
# VINTAGE: PHASE 1 (the FINAL delta check runs Sunday evening; no FINAL existed at build time). Previous scores = W46 FINAL.
# Every figure comes from the W47 computed.json / texts.py / data.py (evidence IDs in comments).
WEEK=47; DATES="16–20 Nov 2026"; VINTAGE="PHASE1"
BIG_COL='#D9A35B'
FN={'R1':'Rate level','R2':'Rate expectations','R3':'Data surprises','N1':'Commodities','N2':'Politics & fiscal','G1':'Global risk mood'}
GN={'X1':'Real yields','X2':'Haven demand','X3':'Central banks & ETFs','X4':'Inflation hedge','X5':'Positioning'}
CCY=[
 dict(id='usd',code='USD',name='US Dollar',sym='$',col='#3DDC97',ch=1,score=5,prev=7,f=[1,1,1,0,0,0],
  vo=["Chapter one: the US dollar.",
      "The dollar scores plus five, down from plus seven last week. But it's still the strongest of the eight.",
      "Why? October inflation ran hot. Prices rose zero point four percent in the month, against zero point three expected. Core prices rose zero point three, against zero point two.",  # S4
      "Markets now price a December Fed hike at about ninety-one percent, and a fifty basis point move at nine to twelve percent. Fed speakers Waller and Logan talk about bigger, or more, hikes. So we think pricing could still move higher. That's a judgement call.",  # S1 S2 S6
      "What the dollar lost is the fear. With calm markets, it no longer gets a safe-haven bonus.",  # G1 1->0
      "Stronger if Fed Chair Warsh on Monday, or the FOMC minutes on Wednesday, back a fifty basis point or a January hike. Weaker if Warsh sounds patient, or US retail sales disappoint on Tuesday.",
      "Pairs to watch: USD/CAD at plus nine, USD/CHF at plus eight, and EUR/USD at minus eight."],
  cards={2:('+0.4%','US CPI, October · vs +0.3% expected · core +0.3% vs +0.2%'),3:('~91%','December Fed hike priced · 50bp at 9–12%'),4:('+1 → 0','Global risk mood · no more haven bonus')},
  up="Warsh or FOMC minutes backing 50bp or a January hike",down="A patient Warsh or weak US retail sales",pairs=[('USD/CAD',9),('USD/CHF',8),('EUR/USD',-8)],flip=5),
 dict(id='eur',code='EUR',name='Euro',sym='€',col='#5B8DEF',ch=2,score=-3,prev=-3,f=[0,0,0,0,-2,0],
  vo=["Chapter two: the euro.",
      "The euro holds at minus three, the same as last week.",
      "The problem is Paris. French ten-year bonds pay one hundred fifty-one point eight basis points more than German ones, up from one hundred thirty-seven point four four weeks ago. That's a stress signal.",  # S20
      "The French Senate votes on the social security budget on Wednesday, and opens the main budget debate on Friday. A December ECB hike is already priced at seventy-two to ninety-one percent, so there's no extra boost.",  # S21 S16 S17
      "Stronger if the spread falls back under about one hundred thirty-seven after smooth Senate votes. Weaker if it widens above its early November peak, or a vote fails.",
      "Pairs to watch: EUR/USD at minus eight, EUR/AUD at minus six, and EUR/GBP at minus four."],
  cards={2:('151.8bp','France vs Germany 10-year gap · 137.4bp four weeks ago'),3:('18 · 20 Nov','Senate: social-security vote · budget debate opens')},
  up="Spread back under ~137bp after smooth Senate votes",down="Spread above its 3 Nov peak or a failed Senate vote",pairs=[('EUR/USD',-8),('EUR/AUD',-6),('EUR/GBP',-4)],flip=4),
 dict(id='gbp',code='GBP',name='British Pound',sym='£',col='#B57BFF',ch=3,score=1,prev=-3,f=[1,0,0,0,0,0],
  vo=["Chapter three: the British pound.",
      "The pound jumps to plus one, up from minus three. One of the biggest moves on the board.",
      "First, last week's fear is gone, so the pound no longer gets dragged down by it.",
      "Second, Bank of England deputy governor Lombardelli said there's likely a case for another hike soon. Markets price December at about seventy-three percent, which now matches what the Bank is saying.",  # S24 S23
      "Growth was in line, at plus zero point seven percent in the third quarter. Now comes a big week: UK jobs on Tuesday, and inflation on Wednesday.",  # S23 S27
      "Stronger if hot wages or inflation lock in a December hike. Weaker if UK inflation comes in below the Bank's three point seven three percent projection.",
      "Pairs to watch: GBP/CAD at plus five, GBP/CHF at plus four, and GBP/USD at minus four."],
  cards={2:('−1 → 0','Global risk mood · the fear drag is gone'),3:('~73%','December BoE hike priced · matches Lombardelli'),4:('+0.7%','UK Q3 GDP, in line · jobs Tue, CPI Wed')},
  up="Hot UK wages or CPI locking in a December hike",down="UK CPI below the BoE's 3.73% projection",pairs=[('GBP/CAD',5),('GBP/CHF',4),('GBP/USD',-4)],flip=5),
 dict(id='jpy',code='JPY',name='Japanese Yen',sym='¥',col='#F0616D',ch=4,score=0,prev=2,f=[-1,0,0,0,1,0],
  vo=["Chapter four: the Japanese yen.",
      "The yen slips to zero, down from plus two.",
      "Calm markets took away its safe-haven support, which was worth plus two on that driver last week.",
      "What still holds it up: Japan's finance minister warned again against rapid moves, with the dollar near one hundred sixty yen. That's an intervention threat.",  # S31
      "But Japanese rates are low, and a December Bank of Japan hike is priced anywhere from fifty-four to seventy-five percent, depending on the source.",  # S28
      "Stronger if Tokyo actually intervenes, or hot growth and inflation data make a December hike certain. Weaker if growth is weak and December pricing fades.",
      "Pairs to watch: USD/JPY at plus five, AUD/JPY at plus three, and CAD/JPY at minus four."],
  cards={2:('+2 → 0','Global risk mood · haven support gone'),3:('~160','Intervention warnings near 160 per dollar'),4:('54–75%','December BoJ hike priced · depends on the source')},
  up="Actual intervention, or hot GDP and CPI making December certain",down="Weak Q3 GDP and fading December pricing",pairs=[('USD/JPY',5),('AUD/JPY',3),('CAD/JPY',-4)],flip=5),
 dict(id='chf',code='CHF',name='Swiss Franc',sym='₣',col='#E8E2D6',ch=5,score=-3,prev=0,f=[-2,0,0,0,0,0],
  vo=["Chapter five: the Swiss franc.",
      "The franc drops to minus three, down from zero. A safe haven with nothing left to hide behind.",
      "It pays zero percent interest, the lowest of the eight. Last week, fear made up for that. This week the fear is gone, so nothing offsets the low rate.",  # S33
      "Markets price only about a ten to twelve percent chance of a December SNB hike, and SNB chief Schlegel sees no clear broadening of price pressure.",  # S33 S32
      "Stronger if a new risk shock hits, with the VIX above twenty-five, or the SNB hints at a December hike. Weaker if markets stay calm.",
      "Pairs to watch: USD/CHF at plus eight, AUD/CHF at plus six, and GBP/CHF at plus four."],
  cards={2:('0%','SNB rate · lowest of the eight · no haven bid'),3:('10–12%','December SNB hike priced · Schlegel relaxed')},
  up="A new risk shock (VIX above 25) or an SNB December hint",down="Continued calm and a relaxed SNB",pairs=[('USD/CHF',8),('AUD/CHF',6),('GBP/CHF',4)],flip=4),
 dict(id='cad',code='CAD',name='Canadian Dollar',sym='C$',col='#FF8A3D',ch=6,score=-4,prev=-6,f=[-1,0,0,-1,-1,0],
  vo=["Chapter six: the Canadian dollar.",
      "The loonie scores minus four. That's up from minus six, but still last on our board.",
      "Oil, Canada's key export, fell about thirteen percent in four weeks. Brent went from one hundred nine dollars eighty-six to ninety-five forty-one. And a fifty percent US tariff on about twenty billion dollars of Canadian goods is still in place.",  # S11 S12 S38
      "The Bank of Canada says rates could need to rise further, and markets price a December hike at forty-five to sixty-six percent. The only relief is the end of risk-off. Our confidence here is low.",  # S34 S35 S36
      "Stronger if Canada's inflation runs hot on Monday, oil rebounds, or a tariff deal comes at APEC. Weaker if inflation is soft, oil drops further, or new tariffs arrive.",
      "Pairs to watch: USD/CAD at plus nine, AUD/CAD at plus seven, and CAD/JPY at minus four."],
  cards={2:('−13%','Brent oil · 4 weeks · plus a live 50% US tariff'),3:('45–66%','December BoC hike priced · "could need to raise"')},
  up="Hot Canada CPI (16 Nov), an oil rebound or a tariff deal",down="Soft CPI, a further oil drop or new tariffs",pairs=[('USD/CAD',9),('AUD/CAD',7),('CAD/JPY',-4)],flip=4),
 dict(id='aud',code='AUD',name='Australian Dollar',sym='A$',col='#FFD25A',ch=7,score=3,prev=0,f=[2,0,0,0,0,0],
  vo=["Chapter seven: the Australian dollar.",
      "The Aussie climbs to plus three, up from zero. That's now a bullish lean.",
      "Australia pays the highest interest rate of the eight, four point eight five percent. In nervous markets that didn't help. In calm markets, it does.",  # S39
      "The RBA is expected to hold in December, at about ninety-seven percent, and consumer sentiment is weak at seventy-eight point two. So this is a carry story, nothing more.",  # S39 S41
      "Stronger if October jobs beat plus twenty-seven point five thousand on Thursday, with strong wages on Wednesday. Weaker if jobs or wages disappoint, the RBA minutes sound dovish, or a new risk scare hits.",  # CAL consensus
      "Pairs to watch: AUD/CAD at plus seven, AUD/CHF at plus six, and EUR/AUD at minus six."],
  cards={2:('4.85%','RBA cash rate · highest of the eight'),3:('~97%','December RBA hold priced · sentiment 78.2')},
  up="Jobs above +27.5k (19 Nov) and strong wages (18 Nov)",down="Weak jobs or wages, dovish RBA minutes, a risk scare",pairs=[('AUD/CAD',7),('AUD/CHF',6),('EUR/AUD',-6)],flip=4),
 dict(id='nzd',code='NZD',name='New Zealand Dollar',sym='NZ$',col='#4FD1C5',ch=8,score=1,prev=-3,f=[0,0,0,1,0,0],
  vo=["Chapter eight: the New Zealand dollar.",
      "The kiwi rises to plus one, up from minus three.",
      "Dairy prices, New Zealand's big export, rose in the last two auctions, by two point five and three percent. And with calm markets, the kiwi no longer pays a fear tax.",  # S15
      "But the interest rate is only two point seven five percent, card spending fell zero point seven percent in October, and the election result only becomes final on November twenty-seventh. Our confidence here is low.",  # S44 S46 S47
      "Stronger if Tuesday's dairy auction is strong again and markets stay calm. Weaker if dairy prices fall, or special votes threaten the government's majority.",
      "Pairs to watch: NZD/CAD at plus five, NZD/CHF at plus four, and NZD/USD at minus four."],
  cards={2:('+5.6%','Dairy prices · last two auctions'),3:('2.75%','RBNZ rate · card spending −0.7% in October')},
  up="A strong dairy auction (17 Nov) and calm markets",down="Weaker dairy or special votes threatening the majority",pairs=[('NZD/CAD',5),('NZD/CHF',4),('NZD/USD',-4)],flip=4),
 dict(id='xau',code='XAU',name='Gold',sym='Au',col='#D9A35B',ch=9,score=-3,prev=7,f=[-1,0,1,-1,0],gold=True,
  vo=["And a bonus chapter: gold.",
      "Gold's own factor swings from plus seven to minus three. One of the biggest changes in our model this week.",
      "Gold pays no interest. The US ten-year real yield rose from two point seven four to two point eight six percent in four weeks, and that makes holding gold more expensive.",  # S48
      "Inflation expectations fell eleven basis points, and calm markets mean no safe-haven demand.",  # S49 regime
      "The support that's left is central banks. China added about twenty-six tonnes in October. Add the dollar's plus five, and gold's overall score is plus two.",  # S51
      "Stronger if real yields fall back below two point seven four percent, or a new risk scare hits. Weaker if real yields keep rising, or central bank and ETF demand fades.",
      "Against the dollar, that's a gap of minus three: a mild bearish lean, with low conviction."],
  cards={2:('2.74→2.86%','US 10-year real yield · 4 weeks'),3:('−11bp','Breakeven inflation · no haven bid'),4:('+26t','China central bank gold buying · October')},
  up="Real yields back below 2.74% or a new risk scare",down="Real yields rising further, or CB and ETF demand fading",pairs=[('XAU/USD',-3)],flip=5),
]
INTRO={
 'cold':["The fear just left the market.","Safe havens like the franc, the yen and gold lost their support.","But the dollar is still on top, thanks to hot inflation.","Here's what that means for every major currency this week."],
 'title':["Welcome to the weekly outlook. Week forty-seven."],
 'big':["Let's start with the big picture.",
        "Last week, markets were scared. This week, the fear has faded. The S and P five hundred is down only one point two eight percent over four weeks, the VIX fear index sits at nineteen point three, and credit spreads narrowed by eleven basis points.",  # S7-S10
        "In our model, that moves the global risk mood from minus two to zero: neutral. Safe havens lose their bonus, and higher-yield currencies stop paying a fear tax.",
        "Three stories drive this week: hot US inflation and a hawkish Fed, French budget stress, and Brent oil down about thirteen percent in four weeks."],
 'guide':["Quick guide to our scores.","Every currency gets a score from minus eighteen to plus eighteen, built from six fundamental drivers.","For a pair, we subtract the two scores. A gap of three or more gives a bullish or bearish lean. Smaller than that, we call it two-sided.","This is a fundamental bias, not a trade signal."],
}
OUTRO={
 'rank':["Now, let's put it all together.",
         "Here's the ranking: the dollar on top at plus five, then the Aussie at plus three, the pound and the kiwi at plus one, and the yen at zero. The euro and the franc sit at minus three, and the Canadian dollar is last at minus four.",
         "The widest gaps: USD/CAD at plus nine, USD/CHF at plus eight and EUR/USD at minus eight, AUD/CAD at plus seven, then AUD/CHF at plus six and EUR/AUD at minus six. The two C A D pairs carry low conviction, because our confidence in the loonie is low.",
         "And some pairs are a stand-off, with no real edge: AUD/USD, EUR/CHF, GBP/NZD and GBP/JPY."],
 'week':["Finally, the week ahead. No major central bank decides rates this week, so the data does the talking.",
         "Monday: Canada's inflation at thirteen thirty GMT, and Fed Chair Warsh speaks at seventeen hundred.",
         "Tuesday: UK jobs at seven, the dairy auction at twelve, and US retail sales at thirteen thirty.",
         "Wednesday: Australian wages, UK inflation at seven, and the FOMC minutes at nineteen hundred GMT.",
         "Thursday: Australian jobs just after midnight GMT, and late in the evening Japan's inflation, time not verified. On Friday, the French Senate opens its budget debate.",
         "Our scenarios: a hawkish Warsh or hawkish minutes would make the dollar story louder. Soft US data would be the biggest risk to it."],
 'outro':["That's the weekly outlook.","If this helped, subscribe and turn on notifications. A new episode every Monday.","Fundamental bias only, not a trade signal. See you next week."],
}
ORDER=['cold','title','big','guide']+[c['id'] for c in CCY]+['rank','week','outro']
def phrases():
    d={**INTRO,**OUTRO}
    for c in CCY: d[c['id']]=c['vo']
    return [(k,d[k]) for k in ORDER]
# ---- screen data for yt_make_spec.py (v1.1 reads these when present)
REGIME=[('S&P 500 · 4 weeks',-1.28,'a small dip, not a sell-off',0,2,'%','var(--crema)'),   # S7 S8
        ('VIX fear index',19.3,'15–25 = normal',15,1,'','var(--crema)'),                     # S9
        ('Credit spreads · 4 weeks',-11,'basis points narrower',0,0,'bp','var(--bull)')]      # S10
STAMP=dict(text='NEUTRAL',col='var(--crema)',left=1500,size=58)
THEMES=[('🔥','Hot US CPI · hawkish Fed'),('🇫🇷','French budget stress'),('🛢️','Brent −13% in 4 weeks')]
COLD_ICONS=['😌','🏔️','💵','☕']
GUIDE_EX=['EUR',-3,'USD',5]
RANK=[('USD',5),('AUD',3),('GBP',1),('NZD',1),('JPY',0),('EUR',-3),('CHF',-3),('CAD',-4)]
TOP=[('USD/CAD',9,'low'),('USD/CHF',8,'medium'),('EUR/USD',-8,'medium'),('AUD/CAD',7,'low'),('AUD/CHF',6,'medium'),('EUR/AUD',-6,'medium')]
TOP_POP=[0.3,2.6,4.6,6.8,9.0,10.8]
TWO=['AUD/USD','EUR/CHF','GBP/NZD','GBP/JPY']
# days: (label, [(event, time, importance, pop '@phrase+sec')]) — times GMT (= UTC) from data.CAL
DAYS=[('Mon 16 Nov',[('Japan Q3 GDP','Sun 23:50 GMT','HIGH','1+0.3'),('Canada CPI','13:30 GMT','HIGH','1+0.8'),('Fed Chair Warsh','17:00 GMT','HIGH','1+3.5')]),
      ('Tue 17 Nov',[('RBA minutes','00:30 GMT','MEDIUM','2+0.3'),('UK jobs','07:00 GMT','HIGH','2+0.8'),('Dairy auction','12:00 GMT','MEDIUM','2+2.2'),('US retail sales','13:30 GMT','HIGH','2+3.8')]),
      ('Wed 18 Nov',[('Australia wages','00:30 GMT','HIGH','3+0.8'),('UK CPI','07:00 GMT','HIGH','3+2.2'),('French Senate vote','time not verified','MEDIUM','3+3.0'),('FOMC minutes','19:00 GMT','HIGH','3+3.8')]),
      ('Thu 19 Nov',[('Australia jobs','00:30 GMT','HIGH','4+0.8'),('APEC: Trump–Putin–Xi','time not verified','MEDIUM','4+2.5'),('Japan CPI','Thu 23:30 GMT · not verified','HIGH','4+4.2')]),
      ('Fri 20 Nov',[('UK retail sales','07:00 GMT','MEDIUM','4+7.0'),('Lagarde speech','08:30 GMT','MEDIUM','4+7.3'),('Senate budget debate','time not verified','HIGH','4+7.6'),('Canada retail','13:30 GMT · not verified','MEDIUM','4+7.9')])]
SCEN='🔥 Hawkish Warsh or minutes → dollar story louder &nbsp;·&nbsp; 🧊 Soft US data → biggest risk to it'
SUBS=[('guide','@3+2.5'),('jpy','@3'),('rank','@1+3')]
