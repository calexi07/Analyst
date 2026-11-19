# FX Before Coffee — YEN SPECIAL, Week 47, Mon 16 Nov 2026 (built ~07:40 Bucharest)
# Sources: archive/vintage-2026-W47-final.json (FINAL, JPY factors R1 -1, R2 0, R3 0, N1 0, N2 +1, G1 0; S 0, prev +2)
# archive/dobs-2026-W47-final.json (JPY invalidation texts) · archive/checks-log.md W47 Check 2 (C7-C12, shadow raw -0.90)
# Overnight news: C7 Reuters/AOL, C8 Reuters/Business Recorder, C9 Trading Economics (GDP detail), C10 China data,
# C11 HDFC Sky (oil), KuCoin flash 16 Nov 03:26 (Katayama line, Q2 annualised 1.4%). Gaps computed in build.py (calc.json).
import json
C = json.load(open('/tmp/claude-0/-home-claude-analyst/e7b839a7-8443-5f03-8443-b53f9a4d089f/scratchpad/calc.json'))
JA = C['JALT']; LB = C['labels']; GP = {r['pair']: r['pg'] for r in C['rows']}
WEEK = 47
FN = ['Rate level', 'Rate expectations', 'Data surprises', 'Commodities', 'Politics & policy', 'Global risk mood']
JPYF = [-1, 0, 0, 0, 1, 0]            # FINAL vintage factors
JPYF_SH = [-1, 0, -1, 0, 1, 0]        # shadow after the GDP miss (R3 0 -> -1)
RAW_SH = C['RAW']['JPY']              # -0.9
PAIRS = [  # (pair, published gap, label, gap if yen -1)
    (p[:3] + '/' + p[3:], GP[p], LB[p], JA[p]) for p in ['USDJPY', 'EURJPY', 'CHFJPY', 'CADJPY', 'AUDJPY', 'GBPJPY', 'NZDJPY']]
VO = {
 'cold': ["Japan's economy just stalled.",
          "The dollar sits just under one hundred sixty yen, the line Tokyo keeps warning about.",
          "And the Fed is still on course for a December hike.",
          "Here's what it all means for the yen this week, pair by pair."],
 'title': ["Welcome to a special yen update. Week forty-seven."],
 'recap': ["Chapter one: what our weekend analysis said.",
           "In this week's Weekly Outlook, the yen scored zero, down from plus two the week before.",
           "The biggest reason: fear left the market. Last week, the yen earned plus two from the global risk mood, as a safe haven. With calm markets, that support dropped to zero.",
           "Two drivers still pull in opposite directions. Japanese interest rates are low, so the yen scores minus one on rate level.",
           "But Japan's finance ministry keeps warning against rapid moves, with the dollar near one hundred sixty yen. That intervention threat scores plus one on politics and policy.",
           "And the Bank of Japan? A December hike is priced anywhere from fifty-four to seventy-five percent, depending on the source. Because the sources conflict, rate expectations score zero.",
           "So the yen starts the week at zero: neutral. Not weak, not strong. A currency waiting for news."],
 'news': ["Chapter two: what happened overnight.",
          "The big one: Japan's third quarter growth. The economy didn't grow at all. Zero point zero percent on the quarter, against plus zero point one expected. Annualised, that's minus zero point one percent, against plus zero point three.",
          "Inside the numbers: households spent zero point three percent less, exports slipped zero point two percent, and imports jumped two point five percent. Business investment was the bright spot, up one point six percent.",
          "So does this stop the Bank of Japan? Not necessarily. Capital Economics says the stagnation probably won't prevent a December hike. State Street expects the Bank to look through this soft patch, unless the weakness spreads to wages and domestic demand.",
          "On the other side of the pair, the dollar. Fed futures price a December hike at about ninety-two to ninety-four percent. The chance of a bigger, fifty basis point move fell to six to eight percent, from eleven and a half on Friday.",
          "And Tokyo? No new warning was confirmed overnight. The latest official words are still Finance Minister Katayama's: recent moves are one-sided and rapid. The dollar trades just under one hundred sixty yen, but that's price context, not part of our score.",
          "One more thing: oil slipped about one percent, to ninety-four dollars eighty-six, as the energy agency now sees a supply surplus. Japan is a big oil importer, so cheaper oil helps it over time. For now, that's information only, until we re-measure on Saturday."],
 'meaning': ["Chapter three: what it means for the yen.",
             "In our model, a big release that comes in weaker than expected is a dovish surprise. So the yen's data surprises driver drops from zero to minus one.",
             "That moves the yen's raw score to minus zero point nine.",
             "But our model only changes a score when the raw number moves by at least one full point. Minus zero point nine is just short. So the yen's shadow score stays at zero.",
             "The status: weakened, and on watch. Half of the yen's weaker-if condition is met: a weak growth report. The other half, December Bank of Japan pricing fading, hasn't happened.",
             "Think of it as a tug of war. Pulling the yen down: a stalled economy, low rates, and a hawkish Fed. Holding it up: the threat of intervention near one hundred sixty, and a Bank of Japan that still looks set to hike.",
             "Remember, this is a shadow check. The weekly scores stay as published until next weekend."],
 'pairs': ["Chapter four: all seven yen pairs.",
           "USD/JPY: plus five, a bullish lean for the dollar. If the yen slips to minus one, the gap widens to plus six. The stalled economy supports this lean, but near one hundred sixty, Tokyo is the referee.",
           "EUR/JPY: minus three, a mild lean toward the yen, and now on watch. One more point down for the yen, and it turns two-sided.",
           "CHF/JPY: also minus three, also on watch, for the same reason. Two former safe havens, and the yen's small edge just got smaller.",
           "CAD/JPY: minus four, leaning to the yen, and on watch. Cheaper oil hurts the loonie too, and today's Canadian inflation report is the other test here.",
           "AUD/JPY: plus three, a fragile bullish lean. A weaker yen would lift it to plus four. Weak Chinese data overnight is a small headwind for the Aussie, but it doesn't change a score.",
           "GBP/JPY and NZD/JPY: both plus one, both two-sided. Even with a weaker yen, they would only reach plus two. Still a stand-off."],
 'watch': ["Chapter five: what to watch this week. Times are in GMT.",
           "Today: Canada's inflation at thirteen thirty, for CAD/JPY. Then Fed Chair Warsh at seventeen hundred. A hawkish Warsh would push the dollar side of USD/JPY. A patient Warsh would be the first real test of that lean.",
           "Tuesday: US retail sales at thirteen thirty. Wednesday: the FOMC minutes at nineteen hundred.",
           "Late on Thursday, around twenty-three thirty GMT, Japan's national inflation for October. A hot number would revive December hike bets for the Bank of Japan.",
           "And all week: any word from Tokyo. Sharper language from the finance ministry would be the first sign that the intervention threat is getting real.",
           "Further out: the Fed decides on December ninth, and the Bank of Japan on December eighteenth."],
 'scen': ["Chapter six: what could happen next.",
          "Scenario one, a weaker yen: Warsh sounds hawkish, US data stays strong, and Bank of Japan pricing fades. The yen's score could slip to minus one. EUR/JPY and CHF/JPY would turn two-sided, and the USD/JPY lean would grow. But the closer we get to one hundred sixty, the bigger the intervention risk.",
          "Scenario two, a stronger yen: Tokyo actually steps in, or Japan's inflation runs hot and a December hike looks certain. Then the yen side gains, and the USD/JPY lean shrinks.",
          "Scenario three, the stand-off: only verbal warnings and mixed data. The yen stays at zero, and every pair keeps its current read.",
          "Right now, the evidence leans slightly toward scenario one, with Tokyo standing guard. None of this is a trade signal."],
 'outro': ["That's the yen update.",
           "For the full picture of all eight currencies, watch this week's Weekly Outlook: Fear Is Gone, Dollar Still on Top.",
           "Subscribe and turn on notifications. Fundamental bias only, not a trade signal. See you soon."],
}
ORDER = ['cold', 'title', 'recap', 'news', 'meaning', 'pairs', 'watch', 'scen', 'outro']
def phrases(): return [(k, VO[k]) for k in ORDER]
SCREEN = dict(
 week=WEEK, order=ORDER, cold=VO['cold'], fn=FN, f=JPYF, fsh=JPYF_SH, raw=RAW_SH,
 coldIcons=['📉', '🗾', '🏦', '☕'],
 recapCards={2: ('+2 → 0', 'Global risk mood · haven support gone'), 3: ('−1', 'Rate level · low Japanese rates'),
             4: ('+1', 'Politics & policy · intervention warnings near 160'), 5: ('54–75%', 'December BoJ hike priced · sources conflict')},
 newsCards={1: ('0.0%', 'Japan Q3 GDP, q/q', 'vs +0.1% expected · −0.1% annualised vs +0.3%', 'bear'),
            2: ('−0.3%', 'Household spending', 'exports −0.2% · imports +2.5% · business investment +1.6%', 'bear'),
            3: ('Still on', 'December BoJ hike?', 'Capital Economics: GDP “probably won’t prevent” it · State Street: look-through', 'crema'),
            4: ('92–94%', 'December Fed hike priced', '50bp tail 6–8% (11.5% on Friday)', 'bull'),
            5: ('~160', 'USD/JPY · no new warning', 'Katayama: moves “one-sided and rapid” · price is context only', 'crema'),
            6: ('$94.86', 'Brent oil · −1%', 'IEA sees a Q4 surplus · information only', 'crema')},
 pairs=PAIRS,
 days=[('TODAY · MON', [('Canada CPI', '13:30 GMT', 'CAD/JPY'), ('Fed Chair Warsh', '17:00 GMT', 'USD/JPY')], 1),
       ('TUE · WED', [('US retail sales', 'Tue 13:30 GMT', 'USD/JPY'), ('FOMC minutes', 'Wed 19:00 GMT', 'USD/JPY')], 2),
       ('THU NIGHT', [('Japan national CPI (Oct)', '~23:30 GMT · not verified', 'all yen pairs')], 3),
       ('ALL WEEK', [('Finance ministry words', 'near 160', 'all yen pairs')], 4),
       ('DECEMBER', [('FOMC decision', '9 Dec', 'USD/JPY'), ('BoJ decision', '18 Dec', 'all yen pairs')], 5)],
 scen=[('📉', 'Weaker yen', 'Hawkish Warsh · strong US data · BoJ pricing fades', 'JPY 0 → −1 · EUR/JPY & CHF/JPY two-sided · USD/JPY +6', 'bear'),
       ('📈', 'Stronger yen', 'Tokyo intervenes · or hot Japan CPI makes December certain', 'Yen leg gains · USD/JPY lean shrinks', 'bull'),
       ('🤝', 'Stand-off', 'Only verbal warnings · mixed data', 'JPY stays 0 · all reads unchanged', 'crema')],
 subs=[('news', '@1+2'), ('pairs', '@6+1'), ('outro', '@2')],
 colors=dict(cold='#D9A35B', title='#F0616D', recap='#F0616D', news='#5B8DEF', meaning='#F0616D', pairs='#D9A35B', watch='#5B8DEF', scen='#B57BFF', outro='#E5322D'),
 chips=dict(recap='CH 1 · THE WEEKEND VIEW', news='CH 2 · OVERNIGHT', meaning='CH 3 · WHAT IT MEANS', pairs='CH 4 · YEN PAIRS', watch='CH 5 · WHAT TO WATCH', scen='CH 6 · SCENARIOS'),
)
if __name__ == '__main__':
    json.dump(SCREEN, open('spec.json', 'w'), ensure_ascii=False)
    print(PAIRS, RAW_SH, sum(len(' '.join(v).split()) for v in VO.values()), 'words')
