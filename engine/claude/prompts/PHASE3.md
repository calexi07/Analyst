# PHASE 3 — WEEKLY REVIEW (template, triggered by "Pornește Phase 3" with the Daily Observer export attached)

Follow all standing Project Instructions (method v2.1), especially §8. This step evaluates frozen forecasts against realised outcomes. It never changes a score, a vintage or an archived JSON.

## 1. Parameters (determine them yourself; do not ask the user)

- Completed week: the most recent ISO week whose Friday close is before today (Europe/Bucharest). Check that the export covers that week; if it covers a different week, say so and ask before continuing.
- Review cutoff: now (Europe/Bucharest and UTC).
- Forecasts under review: archive/vintage-YYYY-Wnn-phase1.json and archive/vintage-YYYY-Wnn-final.json for the completed week (verify the FINAL file's SHA-256 against the calibration log before use). If one is missing, evaluate the one that exists and say so.
- Next target week: the ISO week starting the following Monday.

If no export is attached, ask for it and stop.

Workflow note: the user keeps one conversation per target week (PHASE 1 → PHASE 2 → PHASE 3). Phase 3 normally runs in the same conversation as that week's PHASE 1, after the week has closed; use the archive files, not the conversation history, as the source of record.

## 2. Steps

1. **Export validation (§8.1 step 0):** format and version, ISO week, 29 instruments (28 FX + XAUUSD) × 5 sessions, names, duplicates, week totals, presence of closes, triangular check (cross vs USD legs, 0.05% tolerance; report the max deviation and its likely cause). Archive the normalized export as archive/prices-YYYY-Wnn.json (new file) with its SHA-256.
2. **Track A (§8.2):** realised currency strength (seven sign-adjusted crosses, chained log returns); Spearman ρ for PHASE 1 and FINAL; permutation test across all live vintages so far; top-3 minus bottom-3; directional hit/miss/flat and signed edge by conviction (flat band ±0.25σ); XAUUSD direction. Add 2-week and 4-week horizons as soon as enough weeks exist. Label every result "insufficient sample" per §8.2.
3. **Benchmarks:** carry (R1), equal-weight (c_eq), momentum and persistence (from archived exports only; say "unavailable" if not enough history), PHASE 1 vs FINAL.
4. **Attribution (§8.1 step B):** every currency with a rank gap ≥ 3 and every pair moving ≥ 1σ against its bias gets one code (N1, M, N2, I, P, F, X, D), with sources for post-cutoff explanations. Post-cutoff news explains outcomes only; it never rescores the reviewed week. Mark anything unexplained "UNRESOLVED CONTRADICTION".
5. **Reviews (§8.4):** check whether any currency has run ≥ 1σ against its bias for three consecutive weeks, and count recurring code/factor pairs over the last 12 weeks. Flag any that reach the thresholds; propose nothing automatically.
6. **Calibration log:** append one entry with inputs and SHA-256s, export validation result, Track A numbers, benchmarks, attribution and updated hypotheses. Weights and thresholds stay frozen until 26 live vintages.
7. **Handoff for the next PHASE 1:** the frozen starting factor table (latest FINAL), the list of evidence that must be re-checked, one disproof question per currency and for gold, and a catalyst checklist for the next week.

## 3. Deliverables

1. Self-contained HTML report, readable on a phone: Forex_Fundamental_Bias_Engine_YYYY-MM-DD_WeekNN_PHASE3_WEEKLY_REVIEW.html (NN = completed week), saved in claude/. Sections: metadata and cutoff; executive summary; forecast evaluated (frozen); data quality; currency outcome review; pair outcome review (all 29); Track A; benchmarks; contradictions and attribution codes; verified evidence vs hypotheses; calibration observations; unresolved contradictions; what worked; what failed; lessons (no rule change); next-cycle handoff; catalyst checklist; archive and version status; limitations.
2. archive/prices-YYYY-Wnn.json (new) and the appended archive/calibration-log.md entry.
3. Easy-read companion: Forex_Fundamental_Bias_Engine_YYYY-MM-DD_WeekNN_PHASE3_WEEKLY_REVIEW_EASY.html in claude/, built per claude/prompts/EASY_READ.md (PHASE 3 section).
4. TradingView week wrap-up notes for all 29 pairs, built automatically per claude/prompts/TV_POSTS.md §5 (added to the completed week's TradingView page).

## 4. Reply

Send both HTML files (technical and easy-read) and the TradingView page. Reply to the user in Romanian, briefly: ρ for the week, hit/miss/flat, the biggest misses with their codes, any review trigger, and a reminder that the next step is "Pornește Phase 1" in a new conversation for the next week, after this review is saved (Phase 1 reads this review's handoff).
