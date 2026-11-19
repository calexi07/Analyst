# YOUTUBE WEEKLY OUTLOOK (FX Before Coffee) — format v1 (user request, 13 Nov 2026)

One long-form episode per week, published Monday, built after PHASE 2 from the week's FINAL vintage and FINAL Daily Observer JSON (start-of-week snapshot; no news after the FINAL cutoff). Same numbers as the analysis; built in code; never hand-typed. Fundamental bias only — never a trade signal, entry, stop or target.

## 1. Format
- 16:9, 1920×1080, 30 fps. Target 8–12 min (8+ keeps mid-roll ads possible once monetised). Section length follows the news: big stories get more time, quiet currencies less.
- Voice: Kokoro af_heart, speed 0.95, 0.55 s pauses; pair codes spoken as words (euro-dollar, dollar-yen, dollar-C A D…; map in yt_tts.py). English; captions burned in (word-highlighted).
- Music: lo-fi electric-piano bed (yt_audio.py), ducked under voice; SFX for pops, wipes, stamps, subscribe click + bell.
- Style: coffee-dark palette, cartoon coin mascots per currency (eyes, bob, blink), bouncy (back-out) motion, colour wipe between chapters, chapter slam titles, gauges, animated driver bars, stamps.
- Branded intro (every episode, user decision 13 Nov 2026): claude/video/yt_intro.html + yt_intro_sting.py (7.2 s: chart line → candles → cup logo draws → "FX BEFORE COFFEE" + tagline "Weekly forex outlook · fundamentals, made clear", light sweep, own audio sting). Placed at the very start of every video (user decision 13 Nov 2026: intro first, then the cold open); it replaces the old title sting. Render once per change and reuse the MP4.
- Subscribe: lower-third (bottom right) with cursor click + bell, 3× per episode (after the guide, mid-episode, during the ranking) + big SUBSCRIBE in the outro (outro ≥ 10 s for YouTube end-screen elements).

## 2. Running order (chapters)
1. Branded intro (7 s) · 2. Cold open (3 hooks + promise) · 3. The big picture (risk regime S&P/VIX/credit + RISK-ON/OFF stamp + 3 themes) · 4. How to read our scores (short; can be dropped once the audience knows it) · 5. One chapter per currency in the order USD, EUR, GBP, JPY, CHF, CAD, AUD, NZD + bonus Gold: chapter slam → coin + gauge + score (last week → this week) → the 6 drivers (friendly names) → 2–3 evidence cards (big number + one line) → "Stronger if / Weaker if" (PHASE 1 thesis-card invalidation) → pairs to watch with gaps · 6. Ranking (8 bars) + widest gaps + two-sided stand-offs · 7. The week ahead (5-day calendar from the FINAL catalyst list, GMT times, "time not verified" when n/v) + scenario line · 8. Outro (subscribe, "new episode every Monday", "Fundamental bias only · not a trade signal").
Driver names: R1 Rate level · R2 Rate expectations · R3 Data surprises · N1 Commodities · N2 Politics & fiscal · G1 Global risk mood. Gold: Real yields · Haven demand · Central banks & ETFs · Inflation hedge · Positioning.

## 3. Deliverables (every episode, without being asked)
- MP4 (SendUserFile).
- Thumbnails 1280×720 PNG, two variants A and B for YouTube "Test & compare" (user decision 13 Nov 2026: professional but click-worthy, no cartoon mascots): near-black background with a glowing green trend line and faint candles; a huge 2–4-word headline (statement or question, key word in green/red, e.g. "THE DOLLAR IS BACK", "WHO LOSES TO THE DOLLAR?"); one red/white pill hook ("7 PAIRS. ONE WINNER."); a right-hand card with the week's single strongest number (widest gap, big glowing) or the 8-currency score board. Every claim must be true to the week's FINAL scores (no fake urgency, no price targets). Keep the bottom-right corner clear. Template: claude/video/yt_thumbnail.html (#A / #B).
- English SRT captions file built from the voice timings (upload as subtitles; helps search).
- Title (≤ 70 characters, keyword first, e.g. "Forex Weekly Outlook: Dollar on Top, Loonie Last | Week 46").
- Description: 2-line hook, chapter list with timestamps computed from the render (first at 00:00), the 8 scores, key pairs, the week's calendar, disclaimer, 3–5 hashtags; plus tags and a pinned-comment question.
- Optional: 2–3 Shorts cut from chapters (9:16 versions use the TikTok format).

## 4. Tools (claude/video/)
yt_spec.py (episode content: scores, drivers, VO, cards, flip conditions, pairs) → yt_make_spec.py (spec.json: regime, themes, ranking, top gaps, calendar, colours, chips, subscribe times) → yt_tts.py (vo.json + wav) → yt_render.js (`node yt_render.js cues`, `test '[[scene,t],…]'`, `full 0,2,4…` in two parallel workers) → yt_audio.py (mix.wav) → ffmpeg concat + mux. Engine page: yt_engine.html. Pilot: Week 46 (built 13 Nov 2026 from the W46 FINAL vintage).

## 5. Channel
Setup guide, channel texts and brand assets: claude/prompts/YT_CHANNEL.md (banner 2560×1440, profile 800×800, watermark 150×150 made 13 Nov 2026). Publish Mondays ~07:30 Europe/Bucharest (before the London open).
