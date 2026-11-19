# INTERMEDIARY CHECK (on demand) — triggered by "Verifică <X>"

<X> = one currency (AUD, USD, …), gold (XAU) or one pair (AUDUSD, EURNZD, XAUUSD, …). For a pair, check both legs.

This is NOT a new analysis and NOT a new vintage. It is a short, on-demand check of whether the current week's thesis for <X> still holds after news that came out since the last scored cutoff. It never edits the weekly report, vintage, Daily Observer JSON or Discord file. Method v2.1 rules apply unchanged.

## 1. Inputs (read first; never reconstruct)
- The current week's FINAL vintage (archive/vintage-YYYY-Www-final.json); if FINAL does not exist yet, the PHASE 1 vintage. Say which one.
- That week's Daily Observer JSON (archive/dobs-YYYY-Www-final.json or -phase1): for each leg, `note`; for the pair, `bias`, `conviction`, `priced`, `invalidation`, `catalysts`.
- The PHASE 1 report's thesis card for each leg (bullish and bearish invalidation, catalysts) and its evidence log for the priced path.
- archive/checks-log.md (earlier checks this week for the same asset).
- Reference time T0 = the FINAL check time (or the PHASE 1 cutoff). Check time T1 = now (Europe/Bucharest and UTC).

## 2. What to check (only news dated after T0 and before T1; open every source)
For each leg:
1. Central bank: decisions, vote splits, statements, minutes, speeches.
2. Priced path now vs the path cited in the vintage (probability or implied rate, with date and source).
3. HIGH/CRITICAL data released since T0 vs consensus (surprise direction).
4. Political, fiscal, trade, intervention news (N2 inputs).
5. The leg's terms-of-trade benchmark (oil, iron ore, GDT) and the risk regime inputs, only if they moved materially. These are information only: they are re-measured from closes in the next PHASE 1.
6. One search aimed at disproving the current bias.

Price moves are context only. They are never evidence and never change the verdict on their own.

## 3. Verdict (computed per leg and for the pair)
1. Invalidation test: for each leg, is any bullish or bearish invalidation condition written in the PHASE 1 report now met? Quote the condition and the evidence.
2. Factor impact: map each new item to the single factor it would affect (§5.2) and the direction (+ / −), with a one-line reason.
3. Shadow score (code): apply those factor changes to the vintage's factor scores (±1 step per factor per check, same §5.4 formula and hysteresis against the vintage's published S), recompute the leg's shadow S and the pair's shadow gap and bias. Label it "shadow — not published". Do not apply the ±2 delta-check cap, so the shadow shows the full effect.
4. Status, one per leg and one for the pair:
   - CONFIRMED: no invalidation met, shadow S within 1 point of the published S, and the shadow bias is the same as the published bias.
   - WEAKENED: shadow S moves 2 or more points against the bias, or a "watch" condition is close (event pending, partial evidence), but the shadow bias is unchanged.
   - INVALIDATED: an invalidation condition is met with evidence graded B or better, or the shadow pair bias flips or turns two-sided.
5. What to watch next: the next catalyst for each leg (Bucharest time) and what result would change the status.

No trade signals, entries, stops, targets or sizing. "Status" describes the fundamental thesis only.

## 4. Output
- Reply in Romanian, short and plain (easy-read style, technical terms explained in a few words): the status line first (e.g. "AUD: INVALIDATED"), then the frozen view vs what changed, the invalidation test, the shadow score vs published, and what to watch. Sources as links at the end.
- No HTML report and no Discord file by default. Make an HTML page only if the user asks.
- Append one entry to archive/checks-log.md (create it if missing): check time (Bucharest and UTC), asset, vintage used, T0, published S/bias, shadow S/bias, status, invalidations met, evidence list with URLs and grades, and the price change of the pair/legs from the vintage baseline to T1 if the user supplies it (context only).
- Daily checks covering all currencies and 29 pairs (the scheduled morning and evening checks, or a full manual run): also produce the TradingView daily notes for all 29 pairs automatically, per claude/prompts/TV_POSTS.md §4, and send them to the user with the summary (user decision, 11 Nov 2026). Single-asset "Verifică <X>" checks do not need them unless the user asks.

## 5. Use in PHASE 2 and PHASE 3
- PHASE 2 (delta check) reads archive/checks-log.md: any check item dated before the PHASE 1 cutoff that PHASE 1 missed is an M candidate; anything after it is N1. Checks never change a score directly.
- PHASE 3 adds a short section "Intermediary checks": for each check that week, compare its status with the outcome from the check time to Friday close (did INVALIDATED / WEAKENED calls point the right way?). This is a separate, descriptive track: label it "insufficient sample" until 20 checks exist. It never rescores the week.

## 6. Rules
- Never edit or overwrite any archived file except appending to archive/checks-log.md.
- Never use information dated after T1, never use a source not opened, never estimate a missing figure.
- If nothing new exists since T0, say so in one line: "CONFIRMED — no new evidence since <T0>".
