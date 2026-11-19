# Unique daily notes for Wed 11 Nov 2026 (evening, Check 13) and unique weekly section headers.
# Facts from archive/checks-log.md Check 13; statuses, reads and next-up lists are taken from the check's own notes.
D = {
'EURUSD': dict(
 hook="Same direction as Monday, only with more fuel in the dollar's tank.",
 story="Nothing in Wednesday's news gave the euro a reason to fight back, while the US side kept adding weight to its case. The gap between the two stays at −10, the widest bearish read on the euro side of our board, and the plot has not changed: French worries on one side, a Fed that keeps talking tougher on the other.",
 cb="Markets trimmed their ECB bets as oil cooled, with a December hike now priced near 78%. Paris stayed quiet on the budget front. (The euro also touched an 18-month low against the dollar, which we note as price context only.)",
 cq="Dallas Fed President Logan said two more hikes may be needed and the Fed could move faster this winter. December hike odds climbed to about 88–91%, and January is now above 60%. One fix from yesterday: our shadow dollar score is +7, not +8."),
'GBPUSD': dict(
 hook="The pound is holding its breath for Thursday; the dollar isn't waiting for anyone.",
 story="Sterling spent the day on the sidelines ahead of the first estimate of UK Q3 GDP, the release that can either rescue or deepen the BoE's 'not too many hikes' message. Meanwhile, Fed speakers kept raising the bar. The read stays at −10, so nothing has softened the lean.",
 cb="No fresh UK news today. Everything now points to Thursday morning's GDP number as the next real test for the pound.",
 cq="Another Fed voice turned hawkish: Lorie Logan backed two further increases and a quicker pace this winter, and futures now put a December move at roughly 88–91% (January above 60%). Small correction: the shadow USD score stays at +7 rather than the +8 we showed yesterday."),
'USDJPY': dict(
 hook="Both characters spoke up today, but one of them clearly spoke louder.",
 story="This pair depends on two questions: how hawkish the Fed gets, and how sure markets are about a December BoJ hike. Today the first answer grew stronger and the second became clearer. That makes the 'much stronger yen' scenario less likely, so the central read stays at +5 in favour of the dollar.",
 cb="Fed hike odds for December rose to about 88–91% after Logan argued for two more moves; January sits above 60%. Our shadow USD score remains +7 (not the +8 shown yesterday).",
 cq="The yen weakened to around 159 per dollar on those Fed bets. Swap markets price a December BoJ hike at about 70–75%, near the higher of the two readings we had, so the yen's central score stays +2."),
'USDCHF': dict(
 hook="A busy day for the dollar, a silent one for the franc. Advantage unchanged.",
 story="The franc had nothing new to react to: no SNB comment, no fresh data. The dollar, by contrast, picked up another hawkish voice at the Fed. The published gap of +7 holds, with the US side doing all the talking.",
 cb="Logan, from the Dallas Fed, favoured two more hikes and a faster pace; markets now see December at roughly 88–91%. The score stays at +7 — yesterday's +8 shadow was a mistake, since our stability rule only moves a score on a full point.",
 cq="No SNB signal and no new Swiss data. The franc's tug-of-war between zero interest and safe-haven demand carries on, still balanced at 0."),
'USDCAD': dict(
 hook="The widest gap on our board got a little more supporting evidence on both sides.",
 story="Oil news did the loonie no favours, and the Fed did the dollar plenty. When a currency's lifeline is crude and supply keeps rising, while the other side keeps pricing more rate hikes, the story writes itself. The read stays at +13.",
 cb="Hawkish Fed talk continued: Logan wants two more hikes and possibly faster, and December pricing rose to 88–91%. Our shadow score for USD stays +7 (correcting yesterday's +8).",
 cq="OPEC's own monthly numbers: the group and its allies pumped roughly 2 million extra barrels a day in October (total 41.23 million; Saudi 10.56 million). Extra crude means cheaper crude, and that is the loonie's weak spot."),
'AUDUSD': dict(
 hook="A quiet day down under, a loud one in the US. The lean only gets clearer.",
 story="The Aussie had no new reason to move: no RBA headline, no China surprise. On the other side of the Pacific, the Fed kept talking about more hikes. The read stays at −7, with the dollar's case quietly strengthening while the Aussie waits for a catalyst.",
 cb="Nothing from the RBA or China today that would shift the picture. The risk mood remains the Aussie's main driver.",
 cq="Fed rhetoric hardened again after Dallas Fed's Logan called for two more hikes; December odds are now about 88–91%, January over 60%. The USD shadow score is +7 (yesterday's +8 was an error)."),
'NZDUSD': dict(
 hook="The kiwi is waiting for news. The dollar is making it.",
 story="New Zealand had a calm day while coalition talks continue in the background. In the US, another Fed official argued for a tougher path, and markets agreed. With nothing to lift the kiwi and more support for the dollar, the −10 read holds firm.",
 cb="Coalition talks are still going on; the next real test for the kiwi is the Global Dairy Trade auction on 17 Nov.",
 cq="Logan's call for two more hikes pushed December Fed odds to roughly 88–91% and January above 60%. We keep the shadow USD score at +7 (we showed +8 yesterday by mistake)."),
'EURGBP': dict(
 hook="Two stuck currencies, still stuck. Thursday may finally move one of them.",
 story="Neither side gave the other an opening today. The euro's ECB pricing eased a little and Paris stayed quiet; the pound simply waited. With both at −3, this pair still has no fundamental edge, but UK GDP on Thursday is the first real chance to break the tie.",
 cb="With oil cooling, markets pulled back slightly on ECB hikes: a December move is now priced near 78%. No new French budget news.",
 cq="Sterling had no fresh drivers. UK Q3 GDP at 09:00 Bucharest on Thursday is the release that could finally tip this pair."),
'EURJPY': dict(
 hook="The euro's lean lower holds; the 'much stronger yen' twist got less likely.",
 story="On paper, a hawkish BoJ could have made this story much bigger. Today's pricing suggests markets already expect a lot from Tokyo, so the extra-strong yen scenario fades a little. The central read stays at −5, still favouring the yen.",
 cb="ECB pricing eased as oil cooled, with December now near 78%, and there was no new budget headline from France.",
 cq="Traders now see roughly a 70–75% chance the BoJ hikes next month, matching our higher estimate. Score: +2 for the yen, while dollar strength dragged it toward 159."),
'EURCHF': dict(
 hook="Thin margin, quiet day. The euro's small disadvantage is still there.",
 story="The franc had no news, and the euro had only a small pricing change. That leaves this pair exactly where it started the week: a gentle lean toward the franc, with a gap of just 3 points. One clear headline from either side could still tip it.",
 cb="A December ECB hike is now priced around 78%, a little less than before, as oil prices cooled. France stayed quiet.",
 cq="No new SNB signal. The franc stays balanced at 0 between its zero rate and safe-haven appeal."),
'EURAUD': dict(
 hook="No new chapters today, so the thin lead stays with the Aussie.",
 story="Both currencies had a calm Wednesday. The euro's rate pricing softened slightly while the Aussie had no RBA or China news. The fragile −3 read holds, but it is the kind of gap one strong data point could erase.",
 cb="Markets trimmed ECB hike bets as oil cooled; December is now near 78%. No fresh French fiscal headlines.",
 cq="No RBA comment and no China surprise. The Aussie's fate still depends mostly on the global risk mood."),
'EURNZD': dict(
 hook="Stand-off continues. Both sides stayed in their corners.",
 story="Neither the euro nor the kiwi produced news that could break the tie at −3 each. The euro saw ECB pricing ease a bit, and New Zealand's coalition talks rolled on. The next real catalyst may be the dairy auction on 17 Nov.",
 cb="ECB pricing eased slightly as oil cooled (December hike near 78%); France had no new budget twist.",
 cq="Coalition negotiations continue without a result. The kiwi waits for the 17 Nov dairy auction."),
'EURCAD': dict(
 hook="The euro's small lead got a little help from the oil market.",
 story="This pair is about who is having the worse week. The euro had a calm day, while Canada's crude story got worse on the supply side. The read stays at +3, fragile but intact.",
 cb="Oil cooling trimmed ECB hike bets, with December now near 78%. No French budget news.",
 cq="October brought a supply wave: OPEC+ production rose by around two million barrels daily, OPEC says. That is a headwind for Canada's oil-driven dollar."),
'GBPJPY': dict(
 hook="Sterling waits for Thursday; the yen's 'extra-strong' scenario fades a little.",
 story="The pound had no news, and the yen's case became clearer rather than bigger. With BoJ expectations already high, the biggest yen upside looks less likely, and the pair holds at −5.",
 cb="Quiet for sterling until UK Q3 GDP on Thursday morning, the next big test of the BoE's cautious message.",
 cq="Japan's December hike now looks like the base case for markets (about 70–75%). Our yen score holds at +2; the currency itself slipped near 159 versus the greenback."),
'GBPCHF': dict(
 hook="Nothing moved today. The franc keeps its thin edge.",
 story="Both currencies spent Wednesday without fresh catalysts. The franc stays neutral, the pound stays weighed down by the BoE's mixed message. The −3 gap is still the definition of fragile, and Thursday's UK GDP is its first real test.",
 cb="The pound waits for Thursday's GDP release at 09:00 Bucharest; there was nothing new today.",
 cq="The SNB was silent, and there was no Swiss data to move the franc."),
'GBPAUD': dict(
 hook="Two currencies waiting for news. The Aussie's slim lead holds.",
 story="Without new data on either side, this pair stays where Monday's analysis left it: a small edge for the Aussie, with a gap of −3. UK GDP on Thursday is the most likely trigger for a change.",
 cb="No UK news today; Q3 GDP on Thursday is the next big moment for sterling.",
 cq="No RBA or China headlines. The Aussie's mood still follows global risk appetite."),
'GBPNZD': dict(
 hook="Still level at −3 each. Tomorrow could change that.",
 story="This stand-off continues. The pound waits for its GDP number, and the kiwi waits for coalition news and the dairy auction. Neither side gave the other an inch today.",
 cb="Sterling's next test is UK Q3 GDP on Thursday at 09:00 Bucharest.",
 cq="New Zealand's coalition talks rolled on; dairy prices on 17 Nov are the kiwi's next checkpoint."),
'GBPCAD': dict(
 hook="The pound did nothing today, and still kept its lead. Thank the oil market.",
 story="Sterling was quiet, but the loonie got more bad news from oil supply. That keeps the small +3 edge for the pound intact, though it remains fragile until UK GDP on Thursday gives the pound its own reason to move.",
 cb="No fresh UK data; the market is waiting for Thursday's Q3 GDP estimate.",
 cq="Producers opened the taps: OPEC data put October output at 41.23 million barrels a day, up about two million. Canada's biggest export now faces a heavier market."),
'AUDJPY': dict(
 hook="Still no edge here, and the twist that could create one got less likely.",
 story="The Aussie had no news, and the yen's outlook became clearer. Tokyo's December move is already largely expected, so a sudden yen surge looks less probable. We stay at −2, meaning no clear winner.",
 cb="No RBA or China headline today. The Aussie keeps following the global risk mood.",
 cq="December BoJ hike pricing in swaps is about 70–75%, keeping the yen at a central +2. The yen eased toward 159 per dollar as Fed bets rose."),
'AUDCHF': dict(
 hook="Zero against zero, and nobody moved.",
 story="Both currencies had a silent day. No RBA or China news for the Aussie, no SNB signal for the franc. This remains a pure stand-off, and the risk mood is the main thing to watch.",
 cb="No new RBA or China drivers today.",
 cq="No SNB comment and no Swiss data; the franc's balance holds at 0."),
'AUDNZD': dict(
 hook="Two quiet neighbours. The Aussie keeps its slim lead.",
 story="Neither Australia nor New Zealand produced news today. Coalition talks continue in Wellington, and the dairy auction on 17 Nov is the next real test for the kiwi. The +3 lead for the Aussie stays fragile but intact.",
 cb="Nothing new from the RBA or China; the Aussie stays at 0.",
 cq="Wellington's coalition talks drag on; the dairy auction on the 17th is the kiwi's next checkpoint."),
'AUDCAD': dict(
 hook="Nothing changed for the Aussie; more pressure arrived for the loonie.",
 story="The Aussie had a calm day, while OPEC's numbers added another weight on Canada's oil-dependent currency. That keeps the +6 read firm, with CAD still the weakest score on our board.",
 cb="Australia had a news-free day, and China stayed calm.",
 cq="Oil supply jumped last month (OPEC+ near 41.2 million barrels a day, per OPEC), keeping the pressure on a currency that lives off crude."),
'NZDJPY': dict(
 hook="The kiwi waits; the yen's story becomes clearer, not bigger.",
 story="Much of Tokyo's December hike is already in the price, which shrinks the room for a yen shock. That keeps the central read at −5, still favouring the yen against a kiwi with no fresh news.",
 cb="Coalition talks continue; the kiwi's next checkpoint is the 17 Nov dairy auction.",
 cq="Tokyo's rate outlook firmed up: roughly seven-in-ten odds (70–75%) of a BoJ move in December. That anchors the yen at +2, even as it lost ground near 159 against the dollar."),
'NZDCHF': dict(
 hook="Quiet in Wellington, quiet in Zurich. The franc's thin edge holds.",
 story="Neither side gave traders anything new today. The gap stays at −3, which keeps it fragile: a good dairy auction or a burst of optimism could quickly erase it.",
 cb="Still no new government deal; next week's dairy auction is the one to watch.",
 cq="No SNB signal today, and no Swiss data."),
'NZDCAD': dict(
 hook="Both are having a tough week, but the oil market just made the loonie's tougher.",
 story="New Zealand had no news, while Canada faced a fresh glut of barrels. The kiwi's small +3 lead holds for now.",
 cb="No result yet from coalition negotiations. Dairy prices next Tuesday matter most.",
 cq="OPEC's report showed Saudi Arabia alone at 10.56 million barrels a day in October, part of a roughly 2 million jump for OPEC+. Bad timing for the loonie."),
'CADJPY': dict(
 hook="The weakest currency on our board got weaker news; the yen got clearer news.",
 story="Oil supply data added pressure on the loonie, and the yen's December BoJ picture became clearer. The central read stays at −8 in favour of the yen, with the more dramatic yen scenario now less likely.",
 cb="The oil cartel and partners added around two million barrels a day in October, OPEC reports. More barrels, softer crude, softer CAD.",
 cq="BoJ odds for December hover at 70–75%, the upper end of our range, which pins the yen's score at +2. Against the dollar it eased to around 159."),
'CADCHF': dict(
 hook="The franc did nothing today. The loonie's problems did the work.",
 story="With no SNB news, the franc stayed neutral, while the loonie absorbed another blow from oil supply data. The −6 read is unchanged and remains driven mostly by the Canadian side.",
 cb="OPEC figures show a big October output increase (about +2 million barrels a day). For Canada, that means its main export earns less.",
 cq="No SNB signal, no Swiss data; the franc holds at 0."),
'CHFJPY': dict(
 hook="Two safe havens, still no winner. One possible twist faded today.",
 story="The franc was silent, and the yen's outlook became clearer. Because a BoJ hike is now mostly priced, the yen has less room for a surprise sprint. That leaves this havens' duel at −2, still two-sided.",
 cb="No SNB comment or Swiss data today.",
 cq="With a December BoJ hike now 70–75% priced, the yen sits at its central +2. US rate bets nudged it weaker, to about 159 a dollar."),
'XAUUSD': dict(
 hook="Gold caught its breath, but its biggest enemy is still in the room.",
 story="After Tuesday's sharp drop, gold steadied. The problem is that the reason for the drop has not gone away: US yields are higher and Fed officials keep talking about more, even faster, hikes. Its own model score may ease from +7 toward +4. That is still positive, but the lead is shrinking.",
 cb="Gold steadied near $4,050 after a 2.7% fall on Tuesday. No new ETF or central-bank buying data today.",
 cq="The Dallas Fed chief's call for extra tightening lifted December Fed odds to 88–91%. The USD shadow score stays +7 (correcting yesterday's +8)."),
}
# Unique weekly section headers per pair: (base header, quote header)
H = {
'EURUSD': ("Trouble in Paris", "The dollar finds its swagger"),
'GBPUSD': ("A hike with a warning label", "The greenback reloads"),
'USDJPY': ("Jobs beat, Fed still leaning", "The yen won't be pushed around"),
'USDCHF': ("Momentum on its side", "Paid nothing, still hard to beat"),
'USDCAD': ("All momentum", "Everything going wrong at once"),
'AUDUSD': ("Top carry, lost magnet", "A dollar with fresh legs"),
'NZDUSD': ("Feathers missing", "Dollar in full stride"),
'EURGBP': ("The French burden", "The BoE's mixed message"),
'EURJPY': ("Politics as a weight", "The scared-money magnet"),
'EURCHF': ("France, the problem child", "Quiet safety"),
'EURAUD': ("The heavier backpack", "Lighter, but not light"),
'EURNZD': ("Stress from Paris", "Jobs wobble, dairy cushion"),
'EURCAD': ("Not shining, but steadier", "Deeper in trouble"),
'GBPJPY': ("Read the fine print", "Thriving on nerves"),
'GBPCHF': ("Mixed signals from London", "Calm resilience"),
'GBPAUD': ("Slipping a little faster", "Losing shine more slowly"),
'GBPNZD': ("Held back by the BoE", "Held back by jobs"),
'GBPCAD': ("Not great, but better", "The worst hand on the table"),
'AUDJPY': ("Risk-on without the push", "Risk-off with a backstop"),
'AUDCHF': ("High rate, no hiking story", "Zero rate, full safety"),
'AUDNZD': ("The slightly better hand", "One real cushion"),
'AUDCAD': ("Iron ore holds up", "Watching its export fall"),
'NZDJPY': ("A shaky high-yielder", "The safe harbour"),
'NZDCHF': ("Fragile in a nervous market", "Where fear goes to hide"),
'NZDCAD': ("Slightly less rough", "Rougher still"),
'CADJPY': ("Pressure from every side", "Bought when scared"),
'CADCHF': ("A perfect storm", "Calm in the middle"),
'CHFJPY': ("Safety at zero yield", "Safety with a hawkish hint"),
'XAUUSD': ("The safe haven's moment", "Strong, but a threat to gold"),
}
