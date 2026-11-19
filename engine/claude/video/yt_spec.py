# YouTube weekly outlook — PILOT built from archive/vintage-2026-W46-final.json + dobs-2026-W46-final.json (FINAL, 8 Nov 2026).
WEEK=46; DATES="9–13 Nov 2026"
FN={'R1':'Rate level','R2':'Rate expectations','R3':'Data surprises','N1':'Commodities','N2':'Politics & fiscal','G1':'Global risk mood'}
GN={'X1':'Real yields','X2':'Haven demand','X3':'Central banks & ETFs','X4':'Inflation hedge','X5':'Positioning'}
CCY=[
 dict(id='usd',code='USD',name='US Dollar',sym='$',col='#3DDC97',ch=1,score=7,prev=2,f=[1,1,1,0,0,1],
  vo=["Chapter one: the US dollar.","The dollar scores plus seven, up from plus two last week. That's the strongest of the eight currencies.","The trigger was the jobs report. Payrolls rose by one hundred sixty-five thousand, far above expectations.","Markets price a December Fed hike at around seventy-five to seventy-eight percent. We think that pricing could still move higher.","Risk-off markets add extra support, because investors run to the dollar when they're nervous.","What could change the story? A soft US inflation report, with core under zero point two percent, or Fed speakers cooling the December talk.","Pairs to watch: EUR/USD, GBP/USD and USD/CAD."],
  cards={2:('+165k','US payrolls · far above forecast'),3:('75–78%','December Fed hike priced · room for more'),4:('🛡️','Risk-off: money runs to the dollar')},
  up="Hot inflation + Fed backing December",down="Core CPI under 0.2% m/m or Fed cooling December",pairs=[('EUR/USD',-10),('GBP/USD',-10),('USD/CAD',13)]),
 dict(id='eur',code='EUR',name='Euro',sym='€',col='#5B8DEF',ch=2,score=-3,prev=-4,f=[0,0,0,0,-2,0],
  vo=["Chapter two: the euro.","The euro scores minus three.","The problem isn't Frankfurt, it's Paris. French ten-year bonds pay about one hundred fifty-four basis points more than German ones. That's a stress signal.","The budget faces Senate votes from November twentieth, and S and P reviews France's rating on the twenty-seventh.","Meanwhile, two to three ECB hikes are already priced, so there's little good news left to cash in.","The euro would recover if that spread fell back below about one hundred thirty, or if the Senate removed the budget risk.","Pairs to watch: EUR/USD, EUR/JPY and EUR/CAD."],
  cards={2:('154bp','France vs Germany 10-year gap · stress signal'),3:('20 → 27 Nov','Senate budget votes · S&P rating review'),4:('2–3 hikes','ECB path already priced')},
  up="Spread back below ~130bp or Senate removes budget risk",down="Spread above 161.8bp or a rating action on France",pairs=[('EUR/USD',-10),('EUR/JPY',-5),('EUR/CAD',3)]),
 dict(id='gbp',code='GBP',name='British Pound',sym='£',col='#B57BFF',ch=3,score=-3,prev=4,f=[1,-1,0,0,0,-1],
  vo=["Chapter three: the British pound.","The pound scores minus three, down from plus four.","The Bank of England raised rates to four percent, but warned it doesn't want a long series of hikes.","Markets still price about three more. When the central bank sounds softer than the market, pricing tends to come down, and that weighs on the pound.","Watch UK growth data on Thursday. A strong beat, or Bank of England members backing more hikes, would change the picture.","Pairs to watch: GBP/USD, GBP/JPY and GBP/CAD."],
  cards={2:('4.00%','BoE hiked · but no long series wanted'),3:('~3 more','hikes still priced · gap may close lower')},
  up="UK Q3 GDP well above consensus or MPC backing more hikes",down="Weak Q3 GDP or MPC talking about a pause",pairs=[('GBP/USD',-10),('GBP/JPY',-5),('GBP/CAD',3)],flip=4),
 dict(id='jpy',code='JPY',name='Japanese Yen',sym='¥',col='#F0616D',ch=4,score=2,prev=2,f=[-1,0,0,0,1,2],
  vo=["Chapter four: the Japanese yen.","The yen scores plus two.","Nervous markets send money into the yen, and Tokyo has warned it could step in to support its currency.","The big question is the Bank of Japan. One market gauge prices a December hike at about eighty percent, another at only fifty-six. Same question, two answers.","A clear signal for December would make the yen much stronger. A calmer market, with carry trades coming back, would weaken it.","Pairs to watch: USD/JPY, EUR/JPY and CAD/JPY."],
  cards={2:('🛡️','Safe-haven demand + Tokyo intervention warning'),3:('80% vs 56%','December BoJ hike · two gauges disagree')},
  up="BoJ signalling December clearly",down="Calmer markets, carry trades back, or BoJ delaying",pairs=[('USD/JPY',5),('EUR/JPY',-5),('CAD/JPY',-8)],flip=4),
 dict(id='chf',code='CHF',name='Swiss Franc',sym='₣',col='#E8E2D6',ch=5,score=0,prev=-3,f=[-2,0,0,0,0,2],
  vo=["Chapter five: the Swiss franc.","The franc scores zero, a perfect tug of war.","It pays zero interest, the lowest of the eight, which makes it unattractive in calm times. But fear brings buyers back.","A deeper sell-off, or markets pricing an SNB hike, would lift it. A quick return of optimism would weaken it.","Pairs to watch: USD/CHF and CAD/CHF."],
  cards={2:('0%','Lowest carry of the eight · but a fear magnet')},
  up="Deeper risk-off or SNB hike pricing appearing",down="A quick return of optimism",pairs=[('USD/CHF',7),('CAD/CHF',-6)],flip=3),
 dict(id='cad',code='CAD',name='Canadian Dollar',sym='C$',col='#FF8A3D',ch=6,score=-6,prev=-2,f=[-1,0,-1,-1,-1,-1],
  vo=["Chapter six: the Canadian dollar.","The loonie scores minus six, the weakest on our board.","Oil, Canada's biggest export, fell about six percent in four weeks.","Canada lost four thousand seven hundred jobs when economists expected a gain of thirteen thousand six hundred. A US tariff threat is still live, and risk-off hurts commodity currencies.","The story would change if oil climbed back above its early October level, or if the US and Canada struck a tariff deal.","Pairs to watch: USD/CAD, CAD/JPY and AUD/CAD."],
  cards={2:('−6.1%','Brent oil · 4 weeks'),3:('−4.7k','jobs vs +13.6k expected · tariff threat live')},
  up="Oil back above its 9 Oct level or a US–Canada tariff deal",down="More oil weakness or tariff escalation",pairs=[('USD/CAD',13),('CAD/JPY',-8),('AUD/CAD',6)],flip=4),
 dict(id='aud',code='AUD',name='Australian Dollar',sym='A$',col='#FFD25A',ch=7,score=0,prev=5,f=[2,0,-1,1,0,-2],
  vo=["Chapter seven: the Australian dollar.","The Aussie scores zero, down from plus five.","Australia still has the highest expected interest rate of the eight. But the RBA dropped its bias to hike, in a split six to three vote.","Iron ore rose about three percent, a small help. But risk-off markets usually hit the Aussie hard.","Strong China data and calmer markets would bring it back. Weak China data would push it lower.","Pairs to watch: AUD/USD, AUD/CAD and AUD/NZD."],
  cards={2:('6–3','RBA vote · tightening bias dropped'),3:('+3%','Iron ore · 4 weeks, a small help')},
  up="Strong China data and calmer markets",down="Weak China data or deeper risk-off",pairs=[('AUD/USD',-7),('AUD/CAD',6),('AUD/NZD',3)],flip=4),
 dict(id='nzd',code='NZD',name='New Zealand Dollar',sym='NZ$',col='#4FD1C5',ch=8,score=-3,prev=1,f=[0,0,-1,1,0,-2],
  vo=["Chapter eight: the New Zealand dollar.","The kiwi scores minus three.","Unemployment rose to five point seven percent, above the five point five expected.","Dairy prices, the country's big export, are up about five and a half percent. And the election returned the governing right-leaning bloc with sixty-eight of one hundred thirty-one seats.","Watch the dairy auction on November seventeenth, and the official election result on the twenty-seventh.","Pairs to watch: NZD/USD, NZD/JPY and AUD/NZD."],
  cards={2:('5.7%','Unemployment · vs 5.5% expected'),3:('+5.6%','Dairy prices · election: 68 of 131 seats')},
  up="Better risk mood or rising dairy at the 17 Nov auction",down="Coalition talks stall or weaker dairy",pairs=[('NZD/USD',-10),('NZD/JPY',-5),('AUD/NZD',3)],flip=4),
 dict(id='xau',code='XAU',name='Gold',sym='Au',col='#D9A35B',ch=9,score=7,prev=0,f=[0,2,2,0,0],gold=True,
  vo=["And a bonus chapter: gold.","Gold's own score is plus seven, one of the strongest reads in our model.","Fear is in the air, and central banks and gold ETFs keep buying.","Its main enemy is a hawkish Fed. When US real yields rise, holding a metal that pays no interest gets more expensive.","A hot US inflation report, or ETF outflows, would be the warning signs."],
  cards={2:('🏦','Central banks & ETFs keep buying'),3:('⚠️','Rising real yields = gold’s enemy')},
  up="Falling real yields or growing haven demand",down="Hot US CPI lifting real yields, or ETF outflows",pairs=[('XAU/USD',7)],flip=4),
]
INTRO={
 'cold':["The Fed may not be done hiking.","France's budget is rattling the euro.","And oil just dropped six percent in a month.","Here's what that means for every major currency this week."],
 'title':["Welcome to the weekly outlook. Week forty-six."],
 'big':["Let's start with the big picture.","Global markets turned nervous. The S and P five hundred fell more than five percent in four weeks, and the VIX fear index jumped to around twenty-five.","In our model, that's a risk-off regime. It helps safe havens like the dollar, the yen and the franc, and it hurts commodity currencies.","Three stories drive this week: a Fed that may hike again, France's budget stress, and falling oil."],
 'guide':["Quick guide to our scores.","Every currency gets a score from minus eighteen to plus eighteen, built from six fundamental drivers.","For a pair, we subtract the two scores. A gap of three or more gives a bullish or bearish lean. Smaller than that, we call it two-sided.","This is a fundamental bias, not a trade signal."],
}
OUTRO={
 'rank':["Now, let's put it all together.","Here's the ranking: the dollar on top at plus seven, then the yen, the franc and the Aussie. The euro, the pound and the kiwi at minus three, and the Canadian dollar last at minus six.","The widest gaps are where the strongest stories meet the weakest. USD/CAD leads with plus thirteen. EUR/USD, GBP/USD and NZD/USD follow at minus ten.","And some pairs are a stand-off, with no real edge: EUR/GBP, EUR/NZD, GBP/NZD and AUD/CHF."],
 'week':["Finally, the week ahead.","Tuesday is the big one: US inflation at thirteen thirty GMT, plus the Bank of Japan's meeting summary.","Thursday brings UK growth data at seven GMT. Friday, US producer prices and euro-area growth.","Our scenarios: hot US inflation would make the dollar story even louder. A soft reading would be the biggest risk to it."],
 'outro':["That's the weekly outlook.","If this helped, subscribe and turn on notifications. A new episode every Monday.","Fundamental bias only, not a trade signal. See you next week."],
}
ORDER=['cold','title','big','guide']+[c['id'] for c in CCY]+['rank','week','outro']
def phrases():
    d={**INTRO,**OUTRO}
    for c in CCY: d[c['id']]=c['vo']
    return [(k,d[k]) for k in ORDER]
