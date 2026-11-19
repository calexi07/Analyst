# EASY-READ COMPANION REPORTS (all phases)

After every PHASE 1, PHASE 2 (delta check) and PHASE 3, also produce a plain-English companion HTML for the user. The technical report stays the analysis of record; the easy-read file only explains it.

## Rules (all phases)
- English only, short sentences, simple everyday words. Explain every technical term the first time it appears (bias, conviction, confidence, priced, hawkish/dovish, carry, spread, σ, ρ, etc.).
- Same numbers as the technical report. Build it in code from the same computed data (vintage, JSON, prices file); never hand-type a score, gap, bias or result. Check in code that every score, gap and bias matches the technical report before saving.
- No Daily Observer JSON block (the user copies the JSON only from the technical report).
- No trade signals, entries, stops or targets. Keep the line: "fundamental analysis only, not a trade signal".
- Self-contained HTML, readable on a phone (no horizontal scroll at 390px), light and dark mode, same visual style as the W45 easy-read edition (claude/Forex_Fundamental_Bias_Engine_2026-10-31_Week45_PHASE1_r3_EASY.html): coloured score bars, ++/+/0/−/−− chips, collapsible details for currencies and pairs.
- Name the technical report it explains at the top. Glossary at the end (only terms used on the page).
- File name: the technical report's file name with _EASY before .html, saved in claude/. Send it to the user together with the technical report.

## PHASE 1 easy-read
How to read a score; the week in short; ranking with bars; each currency (why, what would make it stronger, what would make it weaker, events); the six ingredients in plain words plus the factor grid; risk mood; gold; central banks and what the market expects; the CRITICAL decisions of the week with hawkish/dovish outcomes; all 29 pairs in plain words with both legs; calendar in Bucharest time with a "what it is" column; main themes and what would change them; changes vs last week; last week's result in plain words; weak spots; where the numbers come from; glossary.

## PHASE 2 (delta check) easy-read — 1:1 copy of the week's PHASE 1 easy-read (user decision, 1 Nov 2026)
The PHASE 2 easy-read is NOT a separate short page. It is the same week's PHASE 1 easy-read file, reproduced 1:1: same title block, warning box, nav, the same 16 numbered sections in the same order, same wording, same layout, collapsible currencies and pairs, glossary and footer. Build it in code by taking the PHASE 1 easy-read HTML as the template and replacing only what the FINAL data changes:
- Subtitle "Easy-read edition · FINAL (after the delta check) · <dates>"; the intro names both technical reports (FINAL_DELTA and PHASE1).
- Insert right after the warning box: one "Final check" box (the result in one line — "No change, the Phase 1 scores are final" or each change with old → new score, the reason and the ±2-point limit if it bound — plus what was checked, in plain words) and one collapsible table "Last week's move vs this week's bias (29 pairs)" with Aligned / Partial conflict / Conflicting / Neutral explained as a consistency read, not a test.
- Regenerate from the FINAL vintage/JSON: section 2 bullets that mention changed scores or the widest pairs, the section 3 ranking bars, the changed currencies' blocks in section 4 (same texts as the Discord file), the section 5 grid, changed rows in section 8, all 29 pairs in section 9 (same markup, plus a one-line "Final check: was … in Phase 1" note on changed pairs), affected lines in sections 11, 12, 14 and 15, a glossary entry for "Final check", and the footer/import note pointing to the FINAL_DELTA report.
- If there is no correction, the page is still the full 1:1 copy, with the box saying no change.
- Check in code that every score, gap, bias and conviction on the page matches the FINAL vintage, and that the section count equals the template's.

## PHASE 3 (weekly review) easy-read
Strictly about the completed week's review: how last week's forecast did and why. No new-week analysis, scores or pair biases (those come in the next PHASE 1 easy-read).
1. The answer first: did last week's forecast work? One short paragraph with the ranking match (ρ explained as a number from −1 to +1) and hits / misses / flats.
2. How to read the results (what ρ, σ, hit, miss and flat mean; why one week proves nothing and 26 weeks are needed).
3. How each currency actually did vs its score: table with predicted rank, actual rank and a plain sentence.
4. Pairs: which directional pairs worked, which failed, which barely moved, each with one sentence.
5. Why the misses happened: each attribution code explained in plain words (new news after the forecast, something missed, something misjudged, already priced, flows, noise, data problem) with the story for each miss.
6. Gold: what happened and why.
7. Compared with simple alternatives (carry only, momentum, equal weights): did the model do better or worse, in plain words.
8. Data quality of the export, in one or two sentences.
9. Lessons and patterns to watch (no rule changes until 26 weeks).
10. What to watch next week (the handoff questions in plain words).
11. Glossary.

## Discord data file (after PHASE 1 and after every PHASE 2)
- Also produce discord-bias.json for the Discord bot (claude/discord/index.ts), in the exact structure of claude/discord/discord-bias.json: format "bias-engine-discord", version 1, year, week, valid_from, valid_to (target Friday), valid_label ("Mon D – Fri D Mon YYYY"), status, generated, summary (3 short lines), key_events (Bucharest time), currencies (9 assets: name, flag, score, prev, bias, short, breakdown, why[], helps, hurts, events[]), pairs (29: gap, bias, conviction, text, prev_bias).
- Texts are the same plain-English texts as the easy-read report; build in code from the same data and check in code that every score, gap and bias matches the technical report. Keep every Discord field ≤ 1024 characters and each reply ≤ 6000 characters.
- Save it as claude/discord/discord-bias.json (replace).
- Publish it automatically (user decision, 13 Nov 2026; no manual Supabase upload any more): in the repo checkout at /home/claude/analyst (DO_IMPORT.md §3), write the same text to exports/discord-bias.json, commit it together with the run's Daily Observer import (or alone) and push to main. The bot reads it from https://raw.githubusercontent.com/calexi07/Analyst/main/exports/discord-bias.json. After PHASE 2 publish it every time, so the bot shows the FINAL status line even when no score changed. In the summary say "Discord updated automatically" (or the push error); do not ask for an upload.

## TradingView posts (automatic — user decision, 11 Nov 2026)
- After every PHASE 2: the week's TradingView ideas for all 29 pairs, per claude/prompts/TV_POSTS.md §3.
- After every PHASE 3: the week wrap-up notes for all 29 pairs, per claude/prompts/TV_POSTS.md §5.
- After every daily check: the daily notes, per claude/prompts/TV_POSTS.md §4 (see claude/prompts/CHECK.md).
- Produce them without being asked, in the same run, and send the page with the other deliverables.
