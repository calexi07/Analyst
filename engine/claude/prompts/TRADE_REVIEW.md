# PHASE T — TRADE REVIEW (user decision, 13 Nov 2026)

A weekly review of the trader's own executed (live) trades, run at 00:00 Bucharest on the night from Friday to Saturday, after the market close (he has logged the week's trades by then; user decision, 13 Nov 2026) or manually when he asks ("Pornește Trade review" or the task's Run now). It checks every trade against the trader's strategy and against the fundamental context of that week, finds recurring mistakes and patterns, and asks questions where the log is unclear.

Reply to the user in Romanian; archive files stay in English.

## 1. Separation from the fundamental analysis (hard rule)

- PHASE 1, PHASE 2, PHASE 3 and the daily checks never read the trade review or its archive. The review never changes a score, vintage, report, Daily Observer JSON, TradingView page or Discord file.
- The review reads the fundamental archive (read-only) only to describe the context each trade was taken in.
- It reviews closed trades. It gives no trade signals, entries, stops, targets or sizing for future trades. Recommendations are about process and habits (see §6).

## 2. Inputs

1. Trades of the week: `https://raw.githubusercontent.com/calexi07/Analyst/main/exports/trades-latest.json` (format `daily-observer-trades` v1, written by the GitHub Action "Weekly live-trade export" every 30 minutes on Friday 21:00–23:30, at 23:50, and on Saturday 07:15 Bucharest). Review week = the ISO week that contains today when run Friday to Sunday, otherwise the previous week. Check that `week` is the review week and state `generated_at` in the report (trades logged after that time are not included). If it is for another week, download `exports/trades-YYYY-Www.json`; if that is missing too, say so and stop.
2. All live trades for pattern detection: `exports/trades-history.json` (same repo).
3. Fundamental context of that week (read-only, Projects tool): `archive/vintage-YYYY-Www-final.json` (else the PHASE 1 vintage; say which), `archive/dobs-YYYY-Www-final.json` (catalysts with dates), `archive/do-checks/check-YYYY-MM-DD-<slot>.json` (status of the pair at each check), `archive/checks-log.md` (event times when needed).
4. Earlier reviews: `archive/trades/review-*.md` (open questions, answers already given, patterns already flagged).

Trade fields (each a row of the app's trade log, `run` = "Live"): `pair`, `day`, `entry_time` (Bucharest), `session` (computed by the app from the entry time), `sweep_day` and `sweep_time` (when the liquidity was taken, Bucharest; may be empty), `direction` (Long/Short), `break_type` (wick/body), `result` (W/L/BE, or O = still open), `r` (result in R), `entry`, `sl`, `mfe_r` (max favourable in R), `mae_r` (max adverse in R, how close it came to the stop), `chart_url`, `rules_ok` (the trader's own "I followed my rules" tick), `conf_pro` and `conf_con` (optional lists of confluences for and against that he ticked when logging; empty = not logged, never read as "none"), `notes`, and the context the app attached at logging time: `bias`, `conviction`, `base_score`, `quote_score`, `alignment`, `news`, `news_day`, `ctx_manual` (true if he set the context by hand).

## 3. The trader's strategy (as he stated it, 13 Nov 2026)

- S1 Fundamental bias: trades are taken in the direction of the weekly fundamental bias of the pair.
- S2 Liquidity: wait for a previous high/low to be swept (liquidity taken).
- S3 Structure change: a fractal structure break after the sweep, in the opposite direction to the sweep.
- S4 Entry: limit order on the break line (treated as supply/demand).
- S5 Stop loss: beyond the swept liquidity (above it for shorts, below it for longs).
- S6 Take profit: 2R.
- Context he has stated before: risk 1% per trade; he often takes the same setup on several prop accounts at once; he is a swing trader.

Do not add rules he did not state. If a rule seems missing (e.g. no rule for news), ask instead of judging.

## 4. Per-trade review (in code where it is a calculation)

Open trades (`result` = O) are not reviewed or counted in any statistic; list them once under "Still open" with pair, day and direction. A live trade without a `chart_url` is a rule-7 miss (the app now requires the TradingView snapshot): note it.

Treat duplicates first: trades with the same pair, day, direction and entry time within 15 minutes are one setup taken on several accounts. Review the setup once, show how many accounts, and count it once in every statistic (state this in the report).

For every setup, a short card with:
1. Facts: pair, day, time and session, direction, result, R, MFE.
2. Strategy check, one line per rule, each marked ✓ followed / ✗ broken / ? cannot tell from the log:
   - S1: direction vs the bias of that week (from the vintage, not only the app's tag). Two-sided pair → "no fundamental bias" (✗ unless his notes explain).
   - S2: the sweep time (`sweep_day`/`sweep_time`) must be before the entry; report the session of the sweep and the time from sweep to entry. Missing → "?" and, the first time, a question.
   - S3–S4: from `notes`, `break_type` and the chart link description; if not stated → "?" and a question.
   - S5: `sl` present and on the correct side of `entry`; position beyond liquidity can only be judged from notes or chart → "?" if unknown.
   - Management (MFE/MAE): a loss whose MFE reached 1R or more → it was in profit first (consider how it was managed); a win whose MAE was 0.8R or more → it nearly hit the stop (entry or stop placement). Report these as facts with the numbers.
   - S6: a win should be about +2R. A win clearly below 2R → early/manual close; a loss beyond −1.1R → slippage, moved stop or oversizing. Flag either.
   - `rules_ok` = false → ask which rule and why.
   - Confluences (if logged): list the ones for and against. A setup taken with more against than for, or with "Against weekly bias" / "News soon" ticked, is noted as a fact; ask why only if his notes do not explain.
3. Fundamental context at entry: weekly bias and conviction, the status of the pair in the latest daily check before the entry (✅ / 🟡 / 👀 / ⚠️ / ❌ / ⚪), and any HIGH/CRITICAL catalyst for either currency on that day or within ±2 hours of the entry (times from the archive; "time not verified" if unknown).
4. Verdict in one sentence: what was done well, what was wrong, what to change. Factual, direct, no flattery.

## 5. Statistics and patterns (computed in code)

Week: number of setups, wins/losses/BE, total R, average R, win rate, average MFE of losses (how far losers went in favour first), share taken with/against the bias.

Patterns use the full history (trades-history.json, setups de-duplicated). Group by: pair, session, weekday, sweep session, MFE of losses (did losers reach +1R first?), MAE of wins, time from sweep to entry (under 1 h / 1–4 h / over 4 h), with/against bias, weekly conviction, daily-check status at entry, news day, break type, direction, pair × session, each logged confluence (for and against, separately), and confluence balance (for − against: +3 or more / +1 to +2 / 0 / negative). Only setups where confluences were logged count in the confluence groups.

- Clear pattern (report as a recommendation): a group with at least 5 setups and an average of −0.3R or worse per setup. Example: "USDJPY in the Asia session: 6 setups, −4.2R, 5 losses".
- Clear edge (report as a strength): at least 5 setups and an average of +0.5R or better.
- Watch list: 3–4 setups with all losses or an average of −0.5R or worse. Report as "to watch", never as a conclusion.
- Always show n, total R and win rate. Below 5 setups nothing is a conclusion. Say that 5–20 trades are a small sample.
- Do not repeat a recommendation every week in full: if it was already flagged, say whether this week confirmed or weakened it.

## 6. Recommendations

- Only from (a) clear patterns of §5, (b) a rule broken in two or more setups, or (c) a single serious breach (no stop loss, loss beyond −1.5R, trade against a high-conviction bias without a note).
- Phrase them as process changes the trader can choose to adopt ("consider skipping USDJPY in Asia until the pattern changes", "write the sweep level in the notes"), never as instructions for a specific future trade.

## 7. Questions

Ask where the log is unclear or a choice needs explaining (missing stop, against bias without a note, `rules_ok` false, R that does not match the result, entry far from the stated rules). Number them (Q1, Q2…), reference the setup, and keep them short. The run is unattended: put them at the end of the report and in the Romanian summary. The user answers in a chat in this Project ("Răspuns trade review W46: Q1 …"); then append the answers to the review file and update the affected verdicts. Never invent an answer.

## 8. Outputs

1. `archive/trades/review-YYYY-Www.md` (Projects tool): the per-setup cards, statistics, patterns, recommendations, questions. Append-only for later answers.
2. HTML report `Trade_Review_YYYY-MM-DD_WeekNN.html`: self-contained, readable on a phone, in English, plain language; sections: summary, setups (cards), statistics, patterns (with n), recommendations, questions. Send it with SendUserFile.
3. A short Romanian summary with SendUserMessage: setups and total R, the main mistake, the main strength, any clear pattern, the questions.
4. Daily Observer "Analyst" page (user decision, 13 Nov 2026): build in code a JSON with exactly this structure and deliver it to the app:
   `{"format":"daily-observer-trade-review","version":1,"week":{"year":YYYY,"week":NN},"generated_at":"<UTC ISO>","export_generated_at":"<the export's generated_at>","headline":"<one sentence: setups, total R, main point>","summary":{"setups":n,"wins":n,"losses":n,"be":n,"total_r":x,"avg_r":x,"win_rate":0..1,"with_bias":n,"against_bias":n},"setups":[{"pair":"EURUSD","day":"YYYY-MM-DD","time":"HH:MM","session":"London","direction":"Long|Short","result":"W|L|BE","r":x,"accounts":n,"rules":[{"rule":"S1 bias","status":"ok|broken|unknown","note":"..."}, … S1–S6 …],"context":"<fundamental context at entry, one line>","verdict":"<one or two sentences>"}],"patterns":[{"type":"clear|edge|watch","group":"USDJPY · Asia","n":n,"total_r":x,"win_rate":0..1,"text":"<short>"}],"recommendations":["…"],"questions":[{"id":"Q1","setup":"<pair + day>","text":"…"}],"strengths":"<what went well>"}`
   All numbers computed in code from the export. Validate it in code (strict JSON, counts match the setups list). Deliver per claude/prompts/DO_IMPORT.md §3: write imports/trade-review-YYYY-Www.json in the checkout at /home/claude/analyst, append `{"id":"trade-review-YYYY-Www","file":"imports/trade-review-YYYY-Www.json","kind":"trade-review"}` to imports/index.json (a re-run uses the id suffix -r2, -r3 …), commit only those two files and push to main. The app imports it into the Analyst page automatically. If the push fails, say so in the summary.
5. No trades that week: one Romanian line ("Nicio tranzacție live notată în săptămâna NN") and no files.

## 9. Rules

- Never invent a trade, price, time, event or reason. If something is not in the log or the archive, write "not logged" or ask.
- Price after the exit is not judged; only what was knowable at entry and how the trade was managed.
- Tone: honest and specific. Name the mistake plainly, and name what was done well.

## 10. Backfill run, W40 to the current week (user decision, 13 Nov 2026)

The trader is logging his live trades from ISO week 2026-W40 onward after the fact, each with the fundamental context the app showed for that week (the app attaches the weekly bias, conviction and scores of the trade's own week automatically). These trades count like any other live trade: they are in `trades-history.json` and enter every pattern of §5 from the next review on.

The scheduled run of Saturday 14 Nov 2026 (W46) is skipped; the first automatic review is the night of Friday 20 → Saturday 21 Nov 2026 (W47). W40–W46 are reviewed once, by hand, when he writes "Pornește Trade review W40–W46" (or names another range) after he has finished logging:

1. Fresh data first: download `exports/trades-history.json` and check its `generated_at`. If it is older than his message, ask him to run the GitHub Action "Weekly live-trade export" (Actions → Run workflow, week empty) and wait, or try `gh workflow run trades-export.yml --repo calexi07/Analyst` if that works in the session; never review from a stale file without saying so.
2. Scope: all live trades dated in the named weeks. Per-setup cards (§4) for every setup, grouped by week; statistics per week and for the whole range; patterns (§5) over the full history.
3. Context: use the context stored with each trade (bias, conviction, scores, alignment, news), which is what was on the site that week. For weeks before W46 there may be no v2.1 vintage in the archive; say "context: v1 weekly report as shown in the app" instead of reading a vintage. Daily checks only exist from 11 Nov 2026: for earlier trades write "no daily check yet (checks started 11 Nov)" and do not treat it as missing data or a rule miss.
4. Logged after the fact: if the export has `created_at` and it is more than 3 days after the trade day, mark the setup "logged later" (a fact, not a judgement). Ask about the sweep time, MAE or confluences only where they are missing, and keep the questions to the 15 most useful for the whole range.
5. Outputs: one `archive/trades/review-YYYY-Www.md` and one `imports/trade-review-YYYY-Www.json` (+ index entry) per week that has trades, so the Analyst page shows every week, all pushed in one commit; one HTML report for the whole range (`Trade_Review_YYYY-MM-DD_W40-W46.html`); one Romanian summary.
6. Weeks with no logged trades get no file. Never invent a trade or fill a missing field.
