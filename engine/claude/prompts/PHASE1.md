# PHASE 1 — WEEKLY FUNDAMENTAL RESEARCH (template, triggered by "Pornește Phase 1")

Follow all standing Project Instructions (method v2.1). Do not change the methodology, weights, thresholds or the Daily Observer JSON schema.

## 1. Parameters (determine them yourself; do not ask the user)

- Target week: the ISO week that starts on the next Monday after today's date (Europe/Bucharest). If today is Monday–Friday, ask once whether the user means the current week or the next one.
- Research date and cutoff: now; state the exact date, time and time zone (Europe/Bucharest and UTC).
- Evaluation baseline: the Daily Observer Friday close before the cutoff. If any scored evidence is dated after that close, flag the vintage "weekend information".
- Previous vintage: archive/vintage-YYYY-W(nn−1)-final.json. If no FINAL exists for the previous week, use the latest PHASE 1 vintage for that week, say so, and never reconstruct a missing file.
- Existing files: if a PHASE 1 vintage for the target week already exists in the archive, never overwrite it. Save the new run with an -r2 (then -r3…) suffix on every file (report, vintage, dobs), and ask the user which run is the forecast of record before the delta check; the other is marked SUPERSEDED in the calibration log.
- Check daylight-saving changes in the target week (US, UK, EU, Australia, New Zealand) and state the offsets used.

## 2. Mandatory starting point (read before any research)

1. The previous FINAL vintage: start from its factor scores (§5.5). A factor changes only with a new evidence ID and a one-line reason. Apply carry-forward and decay to evidence older than two reports.
2. archive/calibration-log.md: active hypotheses and unresolved contradictions.
3. The latest PHASE 3 weekly review report (claude/…_PHASE3_WEEKLY_REVIEW.html), handoff section: the re-check list and the disproof question for every currency. Answer each disproof question explicitly in the report. If no Phase 3 review exists for the previous week, say so and write one disproof question per currency yourself.
4. Hysteresis: S_t = S_(t−1) if |raw − S_(t−1)| < 1, using the previous FINAL published scores. The JSON `state` uses the change versus the previous published score.

Do not carry an old figure forward because it appeared in the previous report. Re-verify every priced path, regime input and commodity change against the new cutoff.

## 3. Research requirements

Cover every factor in §5 for USD, EUR, GBP, JPY, CHF, CAD, AUD, NZD and XAU:
- Central-bank decisions and communication since the previous cutoff, verified from the central bank's own release where possible.
- Current market-implied paths for all eight banks (R1 on a ~6-month implied basis where available; R2 priced path with its observation date). Refresh any probability older than ~3 trading days at cutoff.
- R3: every HIGH/CRITICAL release and central-bank event since the previous cutoff, each against its own consensus. Keep importance labels consistent with earlier weeks. R3 = sum + trunc(previous R3 ÷ 2).
- N1: Brent 4-week change from settlement data (note contract rolls), iron ore, the last two GDT auctions.
- N2: live fiscal, political, trade and FX-intervention risks for each currency, with dated binary events and market confirmation (spreads).
- G1 regime: S&P 500 4-week change, VIX Friday close, US HY OAS 4-week change.
- Gold: US 10Y real-yield direction, 10Y breakeven 4-week change, central-bank purchases, ETF flows (4-week if available), CFTC positioning.
- For every currency, log at least one search aimed at disproving the current thesis.

Source priority and grading per §4. Open the page for every number used. Never use figures from memory. Separate observed conditions, new information and surprises, market expectations and assessment.

## 4. Scoring and pairs

- Score R1, R2, R3, N1, N2, G1 and gold X1–X5 per §5, then compute §5.4 and §6 in code: composite, raw, hysteresis, published S, blocks, c_eq, confidence, conviction, priced-in, horizon, state, all 29 pairs with evidence/agreement/robustness caps. Never hand-type derived values.
- For every CRITICAL central-bank decision inside the target week, record the priced probability, the dispersion of analyst calls and what a surprise in either direction would do.
- State any single judgement that moves a published score, with the score it would have without that judgement.

## 5. Target week

Catalyst calendar with ISO dates, Bucharest time and UTC: every central-bank decision, CPI, jobs, GDP, PMI/ISM, China data, elections, budget votes and other HIGH/CRITICAL events in the target week, plus key later events in the horizon. Do not fabricate consensus figures.

## 6. Deliverables

1. Self-contained HTML report with the 19 PHASE 1 sections in §9. Filename: Forex_Fundamental_Bias_Engine_YYYY-MM-DD_WeekNN_PHASE1.html, saved in claude/.
2. Daily Observer JSON (daily-observer-fundamentals v1, schema unchanged), all 14 checks run in code on the decoded copy-button text.
3. Archive (new files only, never overwrite): archive/vintage-YYYY-Wnn-phase1.json and archive/dobs-YYYY-Wnn-phase1.json; one appended entry in archive/calibration-log.md with the JSON SHA-256 and the interpretation decisions taken.
4. Section 15: every factor change versus the previous FINAL with old value, new value, evidence ID and reason.
5. Easy-read companion (same scores, plain English, no JSON block; full rules in claude/prompts/EASY_READ.md): Forex_Fundamental_Bias_Engine_YYYY-MM-DD_WeekNN_PHASE1_EASY.html in claude/ (same suffix as the technical report if it is an -r2/-r3 run). Short sentences, simple words, every term explained the first time. Sections: how to read a score; the week in short; ranking with bars; each currency (why, what would make it stronger, what would make it weaker, events); the six ingredients in plain words plus the factor grid; risk mood; gold; central banks and what the market expects; all 29 pairs in plain words with both legs; calendar in Bucharest time with "what it is"; themes and what would change them; changes vs last week; last week's result in plain words; weak spots; where the numbers come from; glossary. Generate it from the same computed data as the technical report; never hand-type a score. The technical report stays the analysis of record.
6. Discord data file: claude/discord/discord-bias.json (replace), built per the "Discord data file" section of claude/prompts/EASY_READ.md, sent to the user with the upload reminder.

## 7. Final quality check and reply

Before finishing, confirm: all nine assets assessed; scale −18…+18; base/quote directions correct; every number traced to a source; dates and time zones explicit; facts, expectations and hypotheses separated; no future information; JSON valid and schema-compatible; no trade signals.

Reply to the user in Romanian, briefly: the published scores table (previous → new, bias), the widest pairs, the critical events of the week, and in one line the target week, research cutoff, weekend-information flag and material limitations. Remind them that the next steps, in this same conversation, are "Pornește Phase 2" (Sunday evening or Monday before 09:00) and, after the week closes, "Pornește Phase 3" with the Daily Observer export.
