# Calibration log — Forex Fundamental Bias Engine (method v2.1)

Cumulative and append-only. Weights, bands and thresholds are frozen until 26 live 1-week vintages exist (§8.5).

## 2026-W44 — PHASE 1 (generated 2026-10-23, cutoff 2026-10-23 01:35 Europe/Bucharest)
- First live v2.1 vintage; scored fresh (no earlier v2.1 vintage in the archive). Track record starts here; no backfill.
- Run timing: generated before the Fri 23 Oct close, so the §3 baseline is the Fri 16 Oct close and the vintage is flagged weekend_information = true. Scored evidence runs to 22 Oct; a 1-week Track A test from the 16 Oct baseline overlaps the research window — note this in Phase 2.
- Interpretation decisions taken (no rule change):
  - `state` on a first run: Strong/Weak by level, otherwise Neutral (no previous v2.1 score).
  - Regime: e and c from the latest closes, v from the Friday 16 Oct VIX close; 16 Oct endpoints give the same values.
  - Oil sources agreed on direction only (+8.5% to +10.9%): N1 capped at ±1, grade C; EUR/JPY importer rule left at 0.
  - §6.1 priced-in has no label for O = 0 and R2 = 0 (CHF, CAD): shown as "Not applicable".
  - R1 used current policy rates (fallback, grade B); cited pricing does not reorder the bands.
- Open items: Daily Observer import code not reviewed (§10); XAU/USD closes not yet in the export; σ source for Phase 2 = Fed H.10 if retrievable, else v1 fixed thresholds ("uncalibrated").

## 2026-W44 — PHASE 1 r2, LIVE (generated 2026-10-24, cutoff 2026-10-24 10:45 Europe/Bucharest)
- The user designated the 23 Oct run above a test run and asked for a fresh start. The 23 Oct file (archive/vintage-2026-W44-phase1.json) stays frozen but is SUPERSEDED and is not a forecast of record; evaluations should read archive/vintage-2026-W44-phase1-r2.json. The v2.1 track record starts with r2.
- Baseline: Fri 23 Oct close. weekend_information = true (Moody's France decision after the US close on 23 Oct; research to Sat 24 Oct).
- Published S: USD +2, EUR −5, GBP +1, JPY +2, CHF −1, CAD −2, AUD +5, NZD 0; gold G +1, XAU +3. Regime −1 (credit only: HY OAS +67bp; SPX −1.07%; VIX ~20).
- Interpretation decisions (no rule change):
  - JPY R3 = +1: core CPI in line, core-core (BoJ preferred) beat; "core governs headline" read as the narrowest core measure.
  - EUR N2 = −1, not −2: −2 conditions arguably met at the Friday close, but Moody's affirmation removed the rating-review binary. Sensitivity: −2 would publish −6.
  - Gold X4 = −2 from FRED T10YIE 2.73% → 2.32% (−41bp); X3 = +1 at grade C (ETF flows only monthly to 30 Sep).
  - CAD N1 +1 capped (oil +9.5% to ~+14% by source); EUR/JPY N1 = 0.
  - Rounding at the boundary: EUR and AUD raw = ∓4.50 exactly, rounded away from zero.
- Hypotheses to watch (no change): v2.1 USD (+2) is far below v1 (+5) because a fully priced December hike gives R2 = 0 — check in Phase 2 whether USD realised strength tracks carry/regime or the v1 inflation read.
- Daily Observer JSON SHA-256: 494d510564e51466120761ef421271f2c0e8d0e52f50672e7aed0d305731e583

## 2026-W44 — FINAL (Phase 2 market review; approved by the user 2026-10-24 11:46 Europe/Bucharest)
- Archive: archive/vintage-2026-W44-final.json · method_version v2.1 · published_at_utc 2026-10-24T09:00:00Z · Phase 2 research cutoff 2026-10-24 12:30 Europe/Bucharest (09:30 UTC) · archived 2026-10-24 ~11:55 Europe/Bucharest.
- Vintage file SHA-256: 522e96040cb013358649761c9f6feb61711e878e867e0e99303bab7f9a17acdb
- Daily Observer JSON: archive/dobs-2026-W44-final.json · SHA-256 634eb4693038d427d7ee64318f6625de756fae3a914b931d0006a074826bbe98 (equals the `daily_observer_json_sha256` field in the vintage; check 14 PASS, run in code on the decoded copy-button text).
- Outcome: no score changes. All published S, factor scores, gold G/XAU, pair biases and convictions identical to PHASE 1 r2. JSON differs from PHASE 1 only in `alignment`, `alignment_note`, `changed`.
- Price data: Dukascopy BID H1, 2026-08-24 00:00 to 2026-10-23 20:00, 29 instruments; validation PASS WITH WARNINGS (CHFJPY missing Sun 2026-10-04 21:00, not filled; XAUUSD instrument schedule; timestamps assumed UTC; volume relative only). All H1 data end at the Phase 1 baseline → in-sample consistency read only. Track A not run (no Daily Observer export).
- §8.3 alignment used the v1 fixed thresholds as 1σ ("uncalibrated"): 14 Aligned, 13 Neutral, 2 Partial conflict (USDCAD −0.83σu, GBPCAD −0.50σu), 0 Conflicting.
- Spearman, scores vs realised strength (in-sample, descriptive): 1w +0.46, 2w −0.14, 4w −0.12, 2-month +0.54.
- Attribution:
  - CAD (S −2; realised rank 2/1/2 over 1w/2w/4w): code P (BoC repricing to ~80% on 17–20 Oct, oil) with F possible. UNRESOLVED CONTRADICTION: CAD strength in late Sep/early Oct, before the Macklem repricing.
  - USD (S +2; realised rank 6/8/7): code P (December odds slipped to ~76–80% on 22–23 Oct; 10Y to ~5%). Priced-path citation corrected (M, documentation only); R2 stays 0 under §5.1 anchors (neutral communication, mixed data).
  - XAU (G +1; gold −4.1% 1w, −6.7% 4w, bottom of two-month range): F hypothesis. UNRESOLVED CONTRADICTION: gold fell on the risk-off Thursday while real yields eased; no October ETF-flow data to test X3.
  - AUD 4-week weakness (S +5; 4w rank 6): code P (12–16 Oct jobs shock, then RBA communication).
- Candidates considered and rejected (no change): USD R2 0 → +1; CAD N1 +1 → +2 with EUR/JPY N1 −1 (Brent $102.75 at 09:00 ET on 25 Sep is intraday, not a settle; threshold still straddled); gold X3 +1 → 0 (commentary only).
- Calibration hypotheses (no methodology change; §8.5 freeze applies):
  - H1: R2 = 0 "already priced" may miss continuation after a large repricing in the 5 days before cutoff (CAD, USD).
  - H2: USD (−0.5) and CHF (−1) did not act as havens in an AI/tech-led credit widening; JPY did. Review betas at 26 weeks.
  - H3: gold model in an oil-led "higher for longer" regime — X2/X3 pushed G up while price fell; check whether X4 alone carried the signal.
  - H4: refresh priced-path probabilities older than ~3 trading days at cutoff (USD citation was 4 days old and had moved ~15 points).
  - Data: BID-only triangular deviation up to 0.12% (GBP crosses) on the completed week; revisit the 0.05% tolerance if Daily Observer exports show the same.
- Report versions: Phase 1 original preserved (claude/Forex_Fundamental_Bias_Engine_2026-10-24_Week44_PHASE1.html); corrected text version claude/Forex_Fundamental_Bias_Engine_2026-10-24_Week44_PHASE1_r2.html (USD December odds ~76–80%, CME FedWatch via Trading Economics, observed 22–23 Oct; SNB hike anticipated in early 2027, Trading Economics, observed 19 Oct, single source). The r2 JSON block is byte-identical to the archived Phase 1 JSON (SHA 494d51…), so its `main_driver`/`priced` text still reads "~94%". Phase 2 report r1 (check 14 PENDING) preserved; r2 = check 14 PASS and status line only.

## 2026-W44 — PHASE 3 weekly review (review cutoff 2026-10-31 09:30 Europe/Bucharest, UTC+2)
- Inputs: frozen archive/vintage-2026-W44-phase1-r2.json and archive/vintage-2026-W44-final.json (FINAL SHA-256 522e9604… re-verified before use); Daily Observer export v2 generated 2026-10-31 07:02 UTC (file SHA-256 0af9880ccc229e0e554207a2d3d362402032eab4bb9ee52239bc3697ec94ae03). No H1 data supplied for 26–30 Oct. No vintage, score or JSON was changed.
- Export validation: 29 instruments × 5/5 sessions, ISO week 44, no duplicates — PASS. Triangular check FAIL vs 0.05% tolerance (max weekly 0.082% EURCAD, max daily 0.070%); attributed to 2-decimal rounding (~0.075% envelope) plus close timing — code D, minor. No close levels in the export. Archived as archive/prices-2026-W44.json (SHA-256 e19e98cc46bdfee8dfde78bb6a9082557db972c4439171421afcf0915836dab8).
- Track A, 1-week, first live observation (insufficient sample throughout; 2w/4w not available):
  - Realised strength (§8.2, 7 crosses): CAD +0.51%, GBP +0.40%, USD +0.25%, CHF +0.23%, AUD +0.20%, EUR −0.18%, JPY −0.26%, NZD −1.13%.
  - Spearman ρ = −0.12 (PHASE 1 = FINAL); single-week permutation p = 0.62. Top-3 (AUD, USD, JPY) minus bottom-3 (EUR, CHF, CAD) = −0.12% (−0.10σu).
  - Directional pairs (uncalibrated σ, flat ±0.25σu): 7 hit / 3 miss / 8 flat. High: 1/0/0 (EURAUD, marginal 0.25σu). Medium: 3/1/3. Low: 3/2/5. Misses: EURNZD, CADJPY, CHFJPY. XAUUSD −2.96% (two-sided, not scored).
  - Benchmarks ρ: carry (R1) +0.06; equal-weight −0.18; momentum +0.38 and persistence +0.02 (both inputs from H1, provisional).
- Attribution (post-cutoff explanations, sources B–C):
  - NZD (0 → rank 8): N1 — RBNZ held 2.75% (4-3) vs ~90% priced hike on 28 Oct.
  - CAD (−2 → rank 1): N1 — BoC hiked to 2.50%, "more increases may be needed". Recurring: rank 2 (W43 H1, in-sample) then rank 1 (W44). UNRESOLVED for the pre-repricing strength. §8.4 not triggered (CAD bias neutral).
  - JPY (+2 → rank 7): P/F — hawkish BoJ hold (8-1, forecasts up) faded; early-week risk-on.
  - AUD (+5 → rank 5): P — Q3 trimmed mean 1.0% q/q in line with consensus (above RBA 0.8%); November hike already ~56% priced.
  - GBP (+1 → rank 2): N1 — Budget benign; gilts eased (N2 risk did not materialise).
  - XAU: F + N1 hypothesis — Friday sell-off with a tech-led equity rout and hot PCE; UNRESOLVED (second week gold fell on a risk-off day).
  - No M (missed pre-cutoff evidence) identified.
- Calibration hypotheses (no change; 1 of 26 live vintages):
  - H1 (repeat): R2 = 0 for "largely priced" CRITICAL meetings inside the target week hides binary event risk (RBNZ, BoC this week).
  - H2 (repeat): haven betas — JPY +0.10% and CHF −0.09% on Friday's risk-off session; gold down on risk-off days two weeks running.
  - H5 (new): CAD ranked 1st/2nd in consecutive weeks while scoring −2; count recurrences per §8.4 (same code, same factor, 4 in 12 weeks).
  - Data: request 3–4 decimals or close levels in the Daily Observer export so the 0.05% triangular tolerance is testable.
- Report: claude/Forex_Fundamental_Bias_Engine_2026-10-31_Week44_PHASE3_WEEKLY_REVIEW.html (includes the W45 handoff: frozen factors, re-check list, disproof questions, catalyst checklist).

## 2026-W45 — PHASE 1 (generated 2026-10-31, cutoff 2026-10-31 15:30 Europe/Bucharest = 13:30 UTC)
- Archive: archive/vintage-2026-W45-phase1.json (new; previous vintages untouched) · baseline Fri 30 Oct close · weekend_information = true (ASX RBA tracker and China PMI dated 31 Oct).
- Daily Observer JSON: archive/dobs-2026-W45-phase1.json · SHA-256 5408e1a9f0ad3a18a9876633542ce8a7be00ca06bb34fd0b26503534aa63ef22 (equals the vintage field; checks 1–14 PASS, run in code on the decoded copy-button text). Vintage file SHA-256 dfa43445ce4f31575336529d4501bdc290458ba93e1612bef8c2773bf3c987ec.
- Published S (W44 FINAL → W45): USD +2 → +5, EUR −5 → −2, GBP +1 → +4, JPY +2 → −1, CHF −1 → −3, CAD −2 → −2 (hysteresis, raw −2.70), AUD +5 → +5 (raw 5.85), NZD 0 → 0; gold G +1 → 0, XAU +3 → +5. Regime −1 → 0 (S&P −1.85%, VIX 19.42, HY OAS +4bp).
- Factor changes (evidence IDs in the report): USD R2 0→+1 (judgement: GDP beat, two hike dissents vs December odds sliding 83%→~73%), USD R3 0→+1; EUR R2 −1→0 (Lagarde validated December), EUR N1 0→−1 and JPY N1 0→−1 (Brent +10.9% front-to-front, capped, grade C); GBP N2 −1→+1 (Budget risk eased), GBP R3 2→1 (decay); JPY R3 1→0; CAD R3 0→−1 (flat August GDP); AUD N1 −1→0 (iron ore −0.7%), AUD R3 1→0; NZD R3 0→−1 (RBNZ hold surprise); all G1 → 0; gold X2 1→0, X3 1→0 (first weekly ETF outflow in 14 weeks), X4 −2→0.
- Interpretation decisions (no rule change):
  - Tokyo CPI and euro-area GDP flash treated as MEDIUM (consistent with the W44 calendar), so excluded from R3.
  - Oil: same straddle handling as W44 but now applied to importers too (most measures ≥ +10%; one at 9.79%) → CAD +1, EUR/JPY −1, all grade C.
  - EUR N2 kept at −1: spread far wider than four weeks ago but retracing from the 23 Oct peak; −2 not met. Sensitivity: −2 would give raw −3.6 → −4.
  - X1 capped at 0 by the USD R2 > 0 rule despite real yields −25bp.
  - Sensitivity: USD R2 = 0 would give raw 2.25 → published +2 (hysteresis).
- Calibration hypotheses (no change; 1 of 26 live vintages evaluated):
  - H1: CRITICAL decisions inside W45 recorded with priced probability and dispersion — RBA 3 Nov (~80%, four major banks expect a hike), BoE 5 Nov (fully priced; economists below market beyond November).
  - H2: moot this week (regime 0); note that one credit-spread input moved JPY/CHF/AUD/NZD scores.
  - H5: CAD count continues (score held at −2).
  - H6 (new): regime inputs sit near cliff-edges (S&P −1.85% vs −2%); track week-to-week regime flips caused by a single input.
- Report: claude/Forex_Fundamental_Bias_Engine_2026-10-31_Week45_PHASE1.html

## 2026-W45 — workflow note (2026-10-31 10:51 Europe/Bucharest)
- The user will re-run PHASE 1 for W45 in a new conversation and has decided in advance that the NEW run (saved with the -r2 suffix) becomes the forecast of record. The 31 Oct PHASE 1 files above (archive/vintage-2026-W45-phase1.json, archive/dobs-2026-W45-phase1.json, both W45 PHASE1 reports) stay frozen but are SUPERSEDED once the r2 run is archived; the delta check and Phase 3 must read the r2 vintage.
- Workflow from now on: one conversation per target week (Phase 1 → Phase 2 delta check → Phase 3); commands per §12 of the Project instructions.

## 2026-W45 — PHASE 1 r3, FORECAST OF RECORD (generated 2026-10-31, cutoff 2026-10-31 11:05 Europe/Bucharest = 09:05 UTC)
- This is the new W45 PHASE 1 run referred to in the workflow note above. It is saved with the -r3 suffix (not -r2) because the name "_PHASE1_r2" was already used by the 31 Oct report claude/Forex_Fundamental_Bias_Engine_2026-10-31_Week45_PHASE1_r2.html. Per the user's decision in that note, r3 is the forecast of record; archive/vintage-2026-W45-phase1.json and archive/dobs-2026-W45-phase1.json (r1) and both earlier W45 PHASE1 reports are SUPERSEDED. The delta check and Phase 3 must read archive/vintage-2026-W45-phase1-r3.json.
- Observation on r1 (no change made): its vintage records a cutoff of 15:30 Europe/Bucharest, but the file was saved at 09:32 Europe/Bucharest the same day.
- Archive: archive/vintage-2026-W45-phase1-r3.json (SHA-256 580c1d9f8cc4dcc24ce316e9c8ec6015004a6f25d457543fe8b1009141e03497) · archive/dobs-2026-W45-phase1-r3.json (SHA-256 6be4b46798e22d48e2461561d2885142fa7ce4be4583fbedc412f201b1854cfe, equals the vintage field; checks 1–14 PASS in code on the decoded copy-button text) · report claude/Forex_Fundamental_Bias_Engine_2026-10-31_Week45_PHASE1_r3.html. Baseline Fri 30 Oct close; weekend_information = true (ASX pricing observed 31 Oct scored in AUD R1/R2).
- Published S (W44 FINAL → W45 r3): USD +2 → +2, EUR -5 → -4, GBP +1 → +4, JPY +2 → +2, CHF -1 → -3, CAD -2 → -2, AUD +5 → +5, NZD 0 → +3; gold G +1 → 0, XAU +3 → +2. Regime −1 → 0 (S&P −1.85%, VIX 19.42, HY OAS +2bp from 1 Oct / +16bp from 2 Oct). Hysteresis held USD (raw +2.25), JPY (+2.25), CAD (−1.80), AUD (+5.85).
- Factor changes vs W44 FINAL (25, each with evidence ID in report section 15): EUR R2 −1→0, N1 0→−1, N2 −1→−2; GBP R3 2→1 (decay), N2 −1→+1; JPY R2 0→+1 (C), R3 1→0, N1 0→−1; CAD R3 0→−1, N1 +1→+2; AUD R3 1→0, N1 −1→0; NZD R2 0→+1, R3 0→−1; USD R3 0→+1; all G1 → 0; gold X2 1→0, X3 1→0, X4 −2→0.
- Interpretation decisions (no rule change):
  - Brent: both front-to-front (+10.9%) and same-contract (+15.0%) settle measures ≥ +10% → CAD N1 +2, EUR/JPY N1 −1 at grade B (r1 had capped CAD at +1 with one measure at 9.79%).
  - EUR N2 −2 by the strict anchor (dated 3 Nov vote + OAT-Bund 159bp vs 130-147bp four weeks earlier), despite the retracement from the 174.6bp peak. Sensitivity: −1 → published −2.
  - NZD R2 +1: statement (all members see tighter policy likely) and four banks calling December vs ~40.8% priced; data neutral. Largest single judgement — R2 0 keeps NZD at 0.
  - JPY R2 +1 at grade C (single aggregator: December 57% after vs 75% before the meeting). Sensitivity: 0 → published −1.
  - USD R2 0: Warsh non-committal vs dissents/Musalem and a GDP beat — lines conflict. Sensitivity: +1 → published +5 (r1 had +1).
  - R1 ranking from 6-month implied levels (AUD 4.91, USD ~4.33, GBP ~4.25, EUR ~3.00, NZD unquantified, CAD ~2.75, JPY ~1.7, CHF 0); NZD/CAD order inferred from ~four RBNZ hikes priced by Sep 2027 → grade C for those two.
  - Gold X1 0 (real yields −25 to −33bp vs a hike-leaning Fed); X3 0 (first weekly ETF outflow in 14 weeks; central-bank data only to August).
  - Tokyo CPI, euro-area GDP flash and national CPIs kept MEDIUM (consistent with W44) → excluded from R3.
- Calibration hypotheses (no change; 1 of 26 live vintages evaluated):
  - H1: CRITICAL decisions in W45 recorded with pricing, dispersion and surprise paths — RBA 3 Nov (~81% ASX, big four unanimous, split after) and BoE 5 Nov (~95%, economists below market after November).
  - H5: CAD held at −2 by hysteresis (raw −1.80) with N1 now +2; count continues.
  - H6: regime cliff-edges — S&P 0.15pp from the −2% threshold; HY change depends on the start day.
- Research access: FRED, CME, BLS, ECB, SNB, RBNZ, ASX tracker, EIA and CFTC (20/27 Oct) were not reachable; their figures come from secondary sources listed in the evidence log (S1–S68).

## 2026-W45 — FINAL (Phase 2 delta check, 2026-11-01 10:00 Europe/Bucharest = 08:00 UTC)
- Checked: archive/vintage-2026-W45-phase1-r3.json (forecast of record; SHA-256 580c1d9f… re-verified) against its cutoff 2026-10-31 11:05 Bucharest (09:05 UTC). Alignment from archive/prices-2026-W44.json (v1 thresholds as 1σ, uncalibrated).
- Archive: archive/vintage-2026-W45-final.json (SHA-256 5d48673fb0d6136deffb900dac6b0bd94a6624ab4574e0cf47aa120a07ac443e) · archive/dobs-2026-W45-final.json (SHA-256 c2a5584d44f48b15abc1526905f634eda53e95fa9f9b02f78db7ae4a473abb47, equals the vintage field; checks 1–14 PASS in code on the decoded copy-button text) · addendum claude/Forex_Fundamental_Bias_Engine_2026-11-01_Week45_FINAL_DELTA.html (+ _EASY companion; discord-bias.json replaced).
- N1 (after cutoff): nothing that changes a scored input. Information only: OPEC+ in-principle December hold (Reuters, 31 Oct 17:01 UTC); unconfirmed Iran–Qatar two-day Hormuz reopening plan; no new RBA/BoE pricing (futures closed).
- Correction (code M, one): NZD R2 +1 → 0, evidence S70 (Trading Economics: December RBNZ hike 77% priced on 29 Oct, 76% on 30 Oct, OCR peak ≥3.75%), grade B. Phase 1 scored the gap from the decision-day 40.8% (S54), which was stale at the cutoff. Recomputed raw 0.00 → S 0 (hysteresis vs W44 FINAL 0); the ±2 legacy-point limit bound, so NZD is published at +1 (PHASE 1 +3). Pairs changed: NZDUSD −1 two-sided; EURNZD −5 bearish medium; GBPNZD +3 bullish low (was two-sided); AUDNZD +4 bullish low (was two-sided); NZDJPY −1 two-sided; NZDCHF +4 bullish low (was medium); NZDCAD +3 bullish low (was medium).
- Interpretation decision (no rule change): "±2 legacy points per currency" applied as a cap on the published S relative to PHASE 1, with derived labels computed from the capped S. Consequence: the FINAL NZD score (+1) is not the rounded raw (0); next week's hysteresis compares against +1.
- M re-checks that confirmed Phase 1 (no change): Fitch France outlook to negative, 30 Oct 22:04 UTC (S69; missed in Phase 1, EUR N2 already −2); OAT-Bund 164.86bp second source (S71; range 159–165bp); BoC later 30 Oct "hold Dec, hike Jan"/~50% (S72); Fed December 68.4% at 08:55 ET 30 Oct and FOMC 8–9 Dec 2026 verified (S73; range ~68–83%); ECB >80% (S74); no revisions to US Q3 GDP, Canada August GDP, Australia Q3 trimmed mean. Unresolved: BoJ post-meeting pricing (JPY R2 +1 stays grade C, unverified — pre-meeting sources show 75–80%, above the 57% used); SNB pricing unquantified; WGC Q3 and October ETF data not found.
- Alignment (in-sample consistency read, not a test): 6 Aligned, 4 Partial conflict (EURNZD, NZDCHF, CADJPY, CHFJPY), 1 Conflicting (NZDCAD −1.19σu), 18 Neutral.
- Calibration notes (no change in the current week): H7 (new) — decision-day pricing after a surprise is a poor R2 input; require the latest close-of-day pricing at the cutoff for any bank that met in the completed week (extends H4). Two Phase 1 judgements flagged as largest (NZD R2, JPY R2) both rested on single post-meeting pricing figures.


## 2026-W45 — PHASE 3 weekly review (review cutoff 2026-11-07 ~15:00 Europe/Bucharest = 13:00 UTC)
- Inputs: frozen archive/vintage-2026-W45-phase1-r3.json (SHA 580c1d9f…) and archive/vintage-2026-W45-final.json (SHA 5d48673f… re-verified before use); Daily Observer export v2 generated 2026-11-07 12:16 UTC (file SHA-256 8999c1e9a7390ca041cd6a120eb215bb9626c3478c0c9fb24b88393ab53afe79). No vintage, score or JSON was changed.
- Export validation: 29 instruments × 5/5 sessions, ISO week 45, no duplicates, week totals = sums — PASS. Triangular check FAIL vs 0.05% (max weekly 0.070% EURNZD; max daily 0.068% Thu) — 2-decimal rounding, code D, minor. No close levels. The export's own strength table includes XAUUSD in USD (+0.06%); §8.2 recomputation gives USD +0.78%. Archived as archive/prices-2026-W45.json (SHA-256 ffa886087118c46fbadfa3f043b0f610902b2582ab1d7ee9c6be4fc0b4c88330).
- Track A, 1-week (insufficient sample throughout):
  - Realised strength (7 crosses): CHF +1.41%, USD +0.78%, EUR +0.61%, GBP +0.47%, JPY +0.12%, CAD -0.47%, NZD -0.96%, AUD -1.96%.
  - Spearman ρ: FINAL -0.47, PHASE 1 r3 -0.63; single-week permutation p (FINAL) = 0.89. Mean ρ across live vintages (W44, W45 FINAL) = -0.29, permutation p = 0.86 (n = 2).
  - Top-3 minus bottom-3: FINAL -0.75% (-0.63σu); PHASE 1 -1.33%.
  - Directional pairs (uncalibrated σ, flat ±0.25σu): FINAL 4 hit / 13 miss / 2 flat (by conviction medium 1/8/2; low 3/5/0); PHASE 1 3/12/2. Hits: USDCAD, GBPNZD, GBPCAD, CADJPY. ≥1σ misses: AUDUSD, EURAUD, AUDJPY, AUDCHF, AUDCAD, EURNZD, NZDCHF. XAUUSD +5.06% (two-sided, not scored).
  - 2-week horizon, W44 FINAL (26 Oct – 6 Nov, overlapping, n = 1): ρ -0.24; pairs 5/10/3 (σu·√2).
  - Benchmarks ρ: carry (R1) -0.35; equal-weight -0.41; persistence (W44 realised) +0.26; momentum unavailable (needs 4 archived exports). FINAL beat PHASE 1 (NZD delta-check correction).
- Attribution (post-cutoff explanations; sources P3-S1–S20 in the report):
  - AUD (+5 → rank 8, gap 7): N1 — RBA hiked to 4.85% as priced but split 6–3 and dropped "including increasing the cash rate if necessary" (official); December odds ~6% afterwards; then Thursday risk-off. Phase 1 R2 +1 rested on Bullock's hawkish words vs a flat post-November curve.
  - CHF (−3 → rank 1, gap 6): N1 (+F) — Swiss CPI 1.5% vs 1.3%, earlier SNB hike pricing; haven flows after the US midterms (Democratic sweep) and the 5 Nov AI sell-off (S&P −4.4%).
  - EUR (−4 → rank 3, gap 5): N1 / P — Brent ~−13% on the week (importer relief), weaker USD after the midterms; French revenue-part rejection (458–0, 4 Nov) widely expected (P); HICP 4.0% in line.
  - Pairs ≥1σ against bias: AUD pairs → N1 (RBA); EURNZD, NZDCHF → N1 (NZ unemployment 5.7% vs 5.5%; December RBNZ odds ~75% → ~60%).
  - No M. UNRESOLVED: AUDCHF −1.25% on Mon 2 Nov (before the RBA); USDCAD +0.78% Fri (LFS reaction unsourced).
- §8.4 reviews: no currency has 3 consecutive weeks ≥1σ against its bias (2 live weeks only; AUD −1.63σu and CHF +1.17σu against bias this week — watch). Recurrence count, code N1 on factor R2 at a CRITICAL meeting inside the target week: RBNZ (W44), BoC (W44), RBA (W45) = 3 in 12 weeks; a 4th reaches the threshold for a methodology proposal. Nothing proposed now.
- Calibration hypotheses (no change; 2 of 26 live vintages):
  - H1 (3rd occurrence): see recurrence count; Phase 1 should record vote-split and guidance risk, not only the priced probability, for CRITICAL meetings inside the week.
  - H2 (mixed): CHF, gold and (Thu) JPY acted as havens this week, unlike W43–W44.
  - H5: CAD weak as scored this week (rank 6); no recurrence.
  - H6 (confirmed): regime near the cliff at cutoff (S&P −1.85% vs −2%) flipped to risk-off within the week (S&P −2.7% on the week, −4.4% on 5 Nov).
  - H7 (support): delta-check correction from stale decision-day pricing improved ρ (−0.63 → −0.47).
  - H8 (new): N1 oil instability — Brent 4-week +10.9% at cutoff, ~−13% in the target week; CAD +2 and EUR/JPY −1 reversed in practice.
- Intra-week note (not a vintage): on 6 Nov a non-archived gold update read the gold factor at about G +10 (X1 +1, X2 +2, X3 +2, X4 0 data missing, X5 0); gold rose +5.06% on the week.
- Report: claude/Forex_Fundamental_Bias_Engine_2026-11-07_Week45_PHASE3_WEEKLY_REVIEW.html (+ _EASY), including the W46 handoff (frozen W45 FINAL factors, re-check list, disproof questions, catalyst checklist).

## 2026-W46 — PHASE 1 (generated 2026-11-07, cutoff 2026-11-07 15:00 Europe/Bucharest = 13:00 UTC)
- Archive: archive/vintage-2026-W46-phase1.json (SHA-256 ab68d01d54608168c9235e8657199896fddd2d634caefe8e78d7e8bd5cbab5c2) · archive/dobs-2026-W46-phase1.json (SHA-256 6ca9bc83e9b40ec78af990732e3201077cf3601b0afb860475f2a1d84ef7d303, equals the vintage field; checks 1–14 PASS in code on the decoded copy-button text) · easy-read claude/Forex_Fundamental_Bias_Engine_2026-11-07_Week46_PHASE1_EASY.html · claude/discord/discord-bias.json replaced. Hysteresis base: archive/vintage-2026-W45-final.json. Baseline Fri 6 Nov close; weekend_information = true (NZ election preliminary count 7 Nov; PBOC October reserves 7 Nov).
- Published S (W45 FINAL → W46 PHASE 1): USD +2 → +7, EUR −4 → −3, GBP +4 → −3, JPY +2 → +2 (hysteresis, raw +2.70), CHF −3 → 0, CAD −2 → −6, AUD +5 → 0, NZD +1 → −4; gold G 0 → +7, XAU +2 → +14. Regime 0 → −2 (S&P 500 −5.56% 9 Oct → 6 Nov; VIX 25.64, one source 23.72; HY OAS +37bp).
- Factor changes vs W45 FINAL (19, each with evidence ID in report section 15): USD R2 0→+1, G1 0→+1; EUR N1 −1→0; GBP R2 0→−1, R3 +1→0, N2 +1→0, G1 0→−1; JPY R2 +1→0, N1 −1→0, G1 0→+2; CHF G1 0→+2; CAD N1 +2→−1, G1 0→−1; AUD R2 +1→0, R3 0→−1, N1 0→+1, G1 0→−2; NZD N2 0→−1, G1 0→−2; gold X2 0→+2, X3 0→+2.
- Interpretation decisions (no rule change):
  - USD R2 +1 (judgement): payrolls/ISM/GDP trend hawkish vs ~75–78% December pricing and about one hike after; communication mixed. Sensitivity: 0 → published +4.
  - GBP R2 −1 (judgement): BoE "not the first in an inevitable long sequence" and Bailey's one-more-then-conditional vs ~3 more hikes priced. Sensitivity: 0 → published 0.
  - AUD R3 −1 judged on the dropped tightening guidance and 6–3 split, the hike itself being priced. Sensitivity: 0 → published +1.
  - JPY R2 0 at grade C: OIS ~80% vs TONA futures 56% for December conflict on the level. Sensitivity: +1 → published +6.
  - NZD N2 −1 (weekend information, no market confirmation yet). Sensitivity: 0 → published −3.
  - Brent 4-week change compares front contracts (January now vs December on 9 Oct): −6.1% → CAD N1 −1, EUR/JPY 0.
  - VIX level conflict (25.64 vs 23.72) is moot: e and c already give regime −2.
  - X1 capped at 0 by USD R2 > 0 despite real yields −31bp from the 5 Oct high.
  - Priced-in "Not applicable" for O = 0 and R2 = 0 (CHF, CAD, NZD), as in W44.
  - R1 rank order unchanged from W45 FINAL; no new 6-month level figures published (CAD and NZD graded C).
- Calibration hypotheses (no change; 2 of 26 live vintages evaluated):
  - H1: no CRITICAL decision inside W46, so no occurrence is possible this week; count stays 3 of 4.
  - H6: regime flipped 0 → −2 between vintages; e and c are now far past their thresholds, v straddles 25.
  - H7: priced paths refreshed to 5–6 Nov.
  - H8: CAD N1 +2 → −1 and EUR/JPY N1 −1 → 0 in one vintage.
  - Cliff-edges logged: iron ore +3.08% (AUD N1 +1 at the +3% band edge); breakeven −10bp (X4 0 at the band edge).
- Process notes: (a) pair-catalyst selection depended on Python set order when importance ties met the 4-item limit; the archived JSON was regenerated byte-identically (same SHA) and the sort will be made deterministic in the next run — no effect on scores. (b) The technical report claude/Forex_Fundamental_Bias_Engine_2026-11-07_Week46_PHASE1.html (~131 KB, SHA-256 f430423ac97213fe…) is too large for the Project save tool; it was sent to the user to add to Project knowledge manually. (c) Secondary-source URLs were not carried into the evidence log (publisher and date recorded; FRED series linked) — re-attach at the delta check.

## 2026-W46 — FINAL (Phase 2 delta check, 2026-11-08 12:30 Europe/Bucharest = 10:30 UTC)
- Checked: archive/vintage-2026-W46-phase1.json (SHA-256 ab68d01d… re-verified) and archive/dobs-2026-W46-phase1.json (SHA-256 6ca9bc83… re-verified) against the PHASE 1 cutoff 2026-11-07 15:00 Bucharest (13:00 UTC). Alignment from archive/prices-2026-W45.json (v1 thresholds as 1σ, uncalibrated). Hysteresis base: W45 FINAL.
- Archive: archive/vintage-2026-W46-final.json (SHA-256 01e8abaf7a912113c5f2e8e2183049795e9aa06141474ef29ed4f9fe504a5288) · archive/dobs-2026-W46-final.json (SHA-256 84df0115a607942c25938518bc72550af911dd98d3e92ad1c7d217e055473d7f, equals the vintage field; checks 1–14 PASS in code on the decoded copy-button text). The dobs-final file was uploaded to the Project as inline text (too large for the file-upload path); byte identity of the Project copy with this SHA was not verified by the tool. Easy-read claude/Forex_Fundamental_Bias_Engine_2026-11-08_Week46_FINAL_DELTA_EASY.html saved; claude/discord/discord-bias.json replaced. The addendum Forex_Fundamental_Bias_Engine_2026-11-08_Week46_FINAL_DELTA.html (~77 KB) is too large for the Project save tool; it was sent to the user to add manually.
- N1 (after cutoff): nothing that changes a scored input (weekend, markets closed; no central-bank, tariff, fiscal or rating news found; search log S63).
- Correction (code M, one): NZD N2 −1 → 0, evidence S54 (elections.nz preliminary results: 131 seats incl. overhang, National–ACT–NZ First 68 of 131) and S55 (majority holds even without the overhang), grade B. PHASE 1 (S20) read 67 of 130 and scored a contested-majority risk premium; the official preliminary count shows a working majority, so the −1 anchor (elevated risk with a dated binary event) is not met. Recomputed raw −2.70; hysteresis vs W45 FINAL (+1) → S −3 (PHASE 1 −4). NZD: bearish, conviction Low, confidence Medium (coverage 85%), state Weakening, horizon short swing.
- Pairs changed (7): NZDUSD −10 bearish medium (evidence cap); EURNZD 0 two-sided; GBPNZD 0 two-sided; AUDNZD +3 bullish low; NZDJPY −5 bearish medium; NZDCHF −3 bearish low; NZDCAD +3 bullish low (was two-sided). All other currencies, gold (G +7, XAU +14) and pairs unchanged.
- M re-checks that confirmed PHASE 1 (no change): Fed December pricing 76.8–80% with one hike beyond (S56); US payrolls 165k (S57); RBA SMP (S58, official); BoE vote 8–1 (S59, official; one outlet said 9–0); OAT–Bund ~135bp on 9 Oct vs 178bp peak 22 Oct (S61). Unresolved but moot: JPY December pricing level (S62, ~80% before the meeting; R2 stays 0 grade C); VIX close conflict (S60; regime −2 either way).
- Alignment (in-sample consistency read, not a test; uncalibrated σ): 13 Aligned, 9 Neutral, 4 Partial conflict (USDCHF, EURJPY, AUDNZD, NZDCAD), 3 Conflicting (EURAUD, GBPAUD, AUDCAD).
- Calibration notes (no change in the current week): (a) M/I observation — a preliminary election count was misread from a secondary source; for scored political events, open the official results source (electoral commission) before scoring N2. (b) Secondary-source URLs from PHASE 1 re-attached where found (S54–S63). (c) No CRITICAL decision inside W46; H1 count stays 3 of 4.

## 2026-W46 — PHASE 3 weekly review (review cutoff 2026-11-14 ~08:35 Europe/Bucharest = 06:35 UTC; automatic scheduled run)
- Inputs: frozen archive/vintage-2026-W46-phase1.json (SHA ab68d01d… re-verified) and archive/vintage-2026-W46-final.json (SHA 01e8abaf… re-verified); W45/W44 FINAL vintages and prices files re-verified. Daily Observer export v2 from the GitHub Action weekly-export (exports/price-action-2026-W46.json, generated 2026-11-14 06:21 UTC, file SHA-256 413a0d5dc55af2088fbab90124bdb7ce1137f403f904727b2d2cddab61975856); export already for W46, no manual workflow dispatch needed. No vintage, score or JSON was changed.
- Export validation: 29 instruments × 5/5 sessions, ISO week 46, pairs_not_logged empty, no duplicates, week totals = sums — PASS. Triangular check FAIL vs 0.05%: max weekly 0.184% NZDCHF (daily +0.031/+0.083/−0.013/+0.011/+0.072 pp, beyond 2-decimal rounding) — code D, the NZDCHF entries for Tue 10 and Fri 13 Nov should be re-checked by the user; next largest EURNZD 0.054%. Export strength table again mixes XAUUSD into USD (+1.56%; §8.2 recomputation +1.13%). Archived as archive/prices-2026-W46.json (SHA-256 a49f4b3fb4089fbcc534d72fa21d4e84ecb2785723b32f80190d41c4ec708f43).
- Track A, 1-week (insufficient sample throughout):
  - Realised strength (7 crosses): USD +1.13%, NZD +0.72%, JPY +0.24%, CAD -0.01%, GBP -0.06%, EUR -0.11%, AUD -0.46%, CHF -1.45%.
  - Spearman ρ: FINAL +0.18, PHASE 1 +0.10; single-week permutation p (FINAL) = 0.33. Mean ρ across live vintages (W44, W45, W46 FINAL) = −0.13, permutation p = 0.73 (n = 3).
  - Top-3 minus bottom-3 (ties shared pro rata): FINAL +0.02%; PHASE 1 −0.07%.
  - Directional FX pairs (uncalibrated σ, flat ±0.25σu): FINAL 9 hit / 8 miss / 5 flat (high 2/0/0; medium 6/3/2; low 1/5/3); PHASE 1 8/8/5. All seven USD pairs hit. ≥1σu misses: EURCHF, GBPCHF, NZDCHF, CADCHF. XAUUSD (bullish medium) -4.71% (log), −3.93σu — miss. Supplementary Yahoo-σ (vol-2026-W46.json, not a §8.2 source): 9/9/4.
  - 2-week horizon, W45 FINAL (2–13 Nov, overlapping, n = 1): ρ −0.18; pairs 6/7/6 (σu·√2). 4-week: available after the W47 close.
  - Benchmarks ρ: carry (R1) +0.13 (top−bottom +0.61%); equal-weight +0.16; persistence (W45 realised) −0.12; momentum unavailable (needs 4 archived exports before the baseline). FINAL beat PHASE 1 (NZD delta-check correction; NZDCAD bullish call hit).
- Attribution (post-cutoff explanations; sources P3-S1–S20 in the report, mostly checks-log C-items):
  - CHF (0 → rank 8, −1.45%, gap +4.5): N1 (+F) — risk mood improved after the cutoff (US–Iran de-escalation headlines; VIX ~18.7–19.5, HY ~330bp by 11–12 Nov) and the hot US CPI widened the Fed–SNB gap (Schlegel: price pressures contained); haven inflows of W45 reversed. G1 +2 rested on the regime −2 measured at the cutoff.
  - NZD (−3 → rank 2, +0.72%): N2 — the election (known, scored N2 0 after the delta check) was read by markets as keeping the RBNZ's inflation-only mandate; NZD led G10 on Monday (+1.57% vs USD); Monday risk-on (N1) added.
  - CAD (−6 → rank 4, −0.01%): N1 — BoC Summary of Deliberations ("could be a need to increase the policy rate further"); Brent +3.3% on 12 Nov after Gulf supply attacks.
  - AUD (0 → rank 7, −0.46%): N1 — Westpac sentiment 78.2 (4-year low), 82% priced that the RBA has peaked, hot US CPI, equity sell-off.
  - XAUUSD: N1 — hot CPI, 50bp talk (Waller), 10-year ~5.10%; gold ~$3,880–3,900 on 13 Nov. Interpretation note (I): USD R2 +1 and X1 0 coexisted (cap allows ≤ 0).
  - AUD, CAD and NZD moves were below 1σu in absolute size. No M identified (the 6 Nov "cut fully priced by year-end" snippet reads "by end-2027" in the 11 Nov source — consistent with the vintage).
- §8.4 reviews: no currency ≥1σu against its bias three weeks running (W44–W46; CHF W45 against, W46 neutral bias). Recurrence counts: N1 on R2 at a CRITICAL meeting inside the target week stays 3 of 4 (no such meeting in W46); N1 on G1 (regime reversal inside the target week) 2 (W45, W46 — CHF both times). Nothing proposed.
- Intermediary checks (CHECK.md §5; 16 checks, insufficient sample): XAUUSD INVALIDATED (from Check 11) pointed right (−3.8% Wed–Fri) while earlier CONFIRMED calls pointed wrong (−6.4% Tue–Fri); JPY INVALIDATED (stronger) right vs the crosses (+0.45% Tue–Fri) but the scenario-B USDJPY call was wrong (+1.15%); EUR WEAKENED (Checks 14–15) pointed wrong (EUR −0.17% Thu–Fri). Windows approximate (close times not recorded).
- Calibration hypotheses (no change; 3 of 26 live vintages):
  - H2: CHF and gold did not act as havens; regime turned risk-on after the cutoff.
  - H6 (second consecutive week): the cutoff regime reversed within the target week (W45 0 → risk-off; W46 −2 → risk-on); G1-driven scores (CHF/JPY +2, AUD/NZD −2) carried the wrong sign in practice.
  - H7 (third support): delta-check correction improved ρ (+0.10 → +0.18).
  - H8: Brent fell early in W46 and rebounded +3.3% on 12 Nov; N1 may flip again at W47.
  - H9 (new): gold structure — a hawkish USD R2 call implies rising real yields, but X1 was set at 0 and G stayed +7 via X2/X3; gold −4.7%.
  - H10 (new, process): XAUUSD invalidation text should reference G inputs only (the gap equals G).
- Handoff for W47 (16–20 Nov): frozen W46 FINAL factors, re-check list (regime likely v 0 / c +1; all priced paths; R3 window incl. US CPI beat and softer PPI; Brent 4-week; OAT–Bund vs four weeks earlier; NZ mandate read), disproof questions per currency and gold, catalyst checklist — in the report.
- Deliverables: claude/Forex_Fundamental_Bias_Engine_2026-11-14_Week46_PHASE3_WEEKLY_REVIEW.html (+ _EASY); TradingView Week 46 page republished with a 🏁 Wrap-up tab (29 notes, 8-word overlap check 0; text in claude/tradingview/tv-2026-W46-wrapup.md).

## 2026-W47 — PHASE 1 (generated 2026-11-14, cutoff 2026-11-14 09:00 Europe/Bucharest = 07:00 UTC; automatic scheduled run)
- Gate: W46 Phase 3 found in the archive (prices-2026-W46.json, calibration-log entry, PHASE3 report); no wait needed. Hysteresis base: archive/vintage-2026-W46-final.json. Baseline Fri 13 Nov close; weekend_information = false (14 Nov weekend items — Rubio on Iran, Trump–Putin–Xi meeting announced for 19 Nov — are context only, S54).
- Archive: archive/vintage-2026-W47-phase1.json (SHA-256 3fe4543f1efbbe34dbe09ce7782c9ee9fc5253535966d47b468e7ec21b904403) · archive/dobs-2026-W47-phase1.json (SHA-256 d89ddb30a49b0ee969795b4f88091597501ba35fd54e2f8c23c2fe20870541c4, equals the vintage field; checks 1–14 PASS in code on the decoded copy-button text read from the rendered page; story checks PASS: 29 stories, $FOREXCOM prefix, titles ≤ 58, 8-word originality, unique headers) · report claude/Forex_Fundamental_Bias_Engine_2026-11-14_Week47_PHASE1.html (+ _EASY) · claude/discord/discord-bias.json replaced · delivered to calexi07/Analyst as imports/2026-W47-phase1.json + exports/discord-bias.json (commit afc1155).
- Published S (W46 FINAL → W47 PHASE 1): USD +7 → +5, EUR −3 → −3 (hysteresis, raw −2.70), GBP −3 → +1, JPY +2 → 0, CHF 0 → −3, CAD −6 → −4, AUD 0 → +3, NZD −3 → +1; gold G +7 → −3, XAU +14 → +2. Regime −2 → 0 (S&P 500 −1.28% 16 Oct → 13 Nov; VIX 19.30; HY OAS −11bp to 12 Nov).
- Factor changes vs W46 FINAL: all G1 → 0 (USD +1, GBP −1, JPY +2, CHF +2, CAD −1, AUD −2, NZD −2 → 0); GBP R2 −1 → 0; CAD R3 −1 → 0, AUD R3 −1 → 0, NZD R3 −1 → 0 (no HIGH release; trunc decay); AUD N1 +1 → 0 (iron ore ~+1–2%); USD R3 stays +1 on a new CPI beat; gold X1 0 → −1, X2 +2 → 0, X3 +2 → +1, X4 0 → −1.
- Interpretation decisions (no rule change):
  - USD R2 +1 (judgement): December ~91% priced, but Waller (50bp) and Logan (two more) exceed the 9–12% priced for 50bp. Sensitivity: 0 → published +2.
  - GBP R2 0: Lombardelli's near-term case matches ~73% December pricing; Bailey's caution read as about the 2027 sequence. Sensitivity: −1 → published −2.
  - JPY R2 0 at grade C (54% futures vs ~70–75% OIS conflict on the level). Sensitivity: +1 → +3.
  - Brent straddle again: front-month −13.2% (109.86 → 95.41, contract roll) vs −9.5% one-month (Trading Economics) → CAD N1 −1, EUR/JPY N1 0, grade C (W44 handling). Sensitivity: CAD −2 → −5; EUR +1 → −2; JPY +1 → +1.
  - NZD N2 0: special votes pending, official result 27 Nov, no market confirmation; the delta-check official count (S54 W46) not overturned. Sensitivity: −1 → 0.
  - EUR N2 −2 held: OAT–Bund 151.8bp vs 137.4bp four weeks earlier, dated Senate votes (18 Nov PLFSS; PLF 20 Nov–9 Dec). The W46 calendar's "23 Nov revenue vote" superseded by the Public Sénat schedule.
  - Gold: X1 −1 with USD R2 +1 and DFII10 +12bp (H9 lesson applied); X3 +1 (PBOC +26t; November ETF flows unavailable). Sensitivity X3 0 → G −5.
  - R1 bands from current policy rates cross-checked with six-month implied proxies (grade C); CAD/NZD graded C. Order: AUD; USD, GBP; EUR, NZD; CAD, JPY; CHF.
  - R3 importance kept as in W46 (US PPI, euro-area GDP, Japan PPI, AU/NZ surveys MEDIUM).
- Calibration hypotheses (no change; 3 of 26 live vintages evaluated):
  - H1: no CRITICAL decision inside W47; count stays 3 of 4. December cluster (RBA 8 Dec; FOMC, BoC, RBNZ 9 Dec; SNB 10 Dec; ECB, BoE 17 Dec; BoJ 18 Dec) falls in W50–W51.
  - H6: third consecutive regime change between vintages (0 → −2 → 0); no input near a threshold at this cutoff.
  - H7: pricing for BoJ, RBA, RBNZ, SNB and BoC only from proxy/aggregator pages (grade C); refresh at the delta check.
  - H8: oil straddle at the −10% band for the second time in three weeks.
- Research access: CME FedWatch, ASX rate tracker (empty table), RBNZ site, Eurostat and several news pages not reachable; figures from secondary sources listed in the evidence log (S1–S58). Research was delegated to four parallel workers that opened the pages; no figure from memory.

## 2026-W47 — FINAL (Phase 2 delta check, 2026-11-15 10:40 Europe/Bucharest = 08:40 UTC; automatic scheduled run)
- Checked: archive/vintage-2026-W47-phase1.json (SHA-256 3fe4543f… re-verified) and archive/dobs-2026-W47-phase1.json (SHA-256 d89ddb30… re-verified; byte-identical to imports/2026-W47-phase1.json in calexi07/Analyst) against the PHASE 1 cutoff 2026-11-14 09:00 Bucharest (07:00 UTC). Alignment from archive/prices-2026-W46.json (v1 thresholds as 1σ, uncalibrated). Hysteresis base: W46 FINAL.
- Result: no correction — PHASE 1 promoted to FINAL. N1 (14 Nov 07:00 UTC → 15 Nov 08:40 UTC): no central-bank, MoF, fiscal, tariff, election or commodity item dated in the window that changes a scored input (weekend; one undated US–Canada "deal at APEC" report not used). M: no PHASE 1 "unavailable" item became verifiably available as of the cutoff; judgement factors unchanged; no revision notices surfaced (scored pages not re-opened one by one). checks-log.md: no check after the cutoff.
- Archive: archive/vintage-2026-W47-final.json (SHA-256 6388402a088149220d0567542c01f07a41fda1a717a55e9c6cb69260fa2e5064) · archive/dobs-2026-W47-final.json (SHA-256 1d720fd6c3ba5ba71264ef20b849bf24407d0ca498399d5ae37758daed2a3862, equals the vintage field; checks 1–14 PASS in code on the decoded copy-button text; story checks PASS incl. 8-word originality 0 overlaps, kit bias = pair bias, kit close/σ = claude/tradingview/vol-2026-W47.json). Delivered to calexi07/Analyst as imports/2026-W47-final.json + exports/discord-bias.json (commit 3342d67).
- Alignment (in-sample consistency read, not a test; uncalibrated σ): 14 Aligned, 13 Neutral, 2 Partial conflict (AUDJPY −0.61%; AUDCAD −0.42%), 0 Conflicting.
- Chart kits: volatility and reference Friday closes from exports/fx-vol-latest.json (GitHub Action, generated 2026-11-14 11:55 UTC, baseline_friday 2026-11-13; no workflow dispatch needed).
- Observations for later review (never applied in the current week): (a) Project knowledge is near its size cap (~1.86 of 2.0 MB before this run); the FINAL dobs/addendum copies may not fit — the GitHub copy imports/2026-W47-final.json carries the SHA above. (b) No CRITICAL decision inside W47; H1 count stays 3 of 4.
