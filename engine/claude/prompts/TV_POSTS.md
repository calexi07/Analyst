# TRADINGVIEW POSTS (automatic — user decision, 11 Nov 2026)

The user publishes the engine's story on TradingView under his EaglePips brand. Produce these posts automatically, without being asked:

| When | What | Built from |
|---|---|---|
| After every PHASE 2 (delta check, FINAL vintage) | **Weekly ideas**: one idea per pair, 29 posts, each with a **chart kit** (§3a) | The week's FINAL vintage and FINAL Daily Observer JSON |
| After every daily check (scheduled morning and evening checks, and any "Verifică" run covering all pairs) | **Daily notes**: one short note per pair, 29 notes, added under the week's idea, each with its **chart flag** (§4) | That check's checks-log entry (statuses, shadow gaps, what changed) |
| After every PHASE 3 (closing review of the completed week) | **Week wrap-up notes**: one closing note per pair, 29 notes, added under that week's idea | The PHASE 3 review (realised moves, hit/miss/flat, attribution codes) |

All posts are in English (very simple, friendly), all replies to the user in Romanian. Same numbers as the analysis; build them in code from the archive files; never hand-type a score, gap, bias or status. No entries, stops, targets or sizing. A fundamental bias is never called a signal.

Reference implementation (Week 46): claude/tools/tv_posts_reference_W46.py (page, helpers, daily notes), claude/tools/tv_pair_stories_W46.py (example of 29 pair-specific stories with unique section headers `tb`/`tq`, closing-question and disclaimer pools), claude/tools/tv_daily_unique_W46.py (example of 29 unique daily notes: hook, descriptive paragraph, per-leg wording, plus the weekly header dict H) and claude/tools/tv_chart_kit_W46.py (chart kit + daily flags added to the page; volatility input claude/tradingview/vol-2026-W46.json). Reuse the structure, styling and helpers; write new pair texts every time.

## 1. TradingView formatting (mandatory)

TradingView does NOT keep rich-text paste. Use only its BBCode tags:
`[b]…[/b]`, `[i]…[/i]`, `[s]…[/s]`, `[list]\n[*]…\n[/list]`, `[list=1]\n[*]…\n[/list]`, `[quote]…[/quote]`, `[url=LINK]text[/url]`.

- First line of each weekly idea: the ticker `$FOREXCOM:PAIR` (the user changes the prefix if needed).
- Emojis are welcome. Do not use flag emojis (they render as letters on Windows). Currency emojis: 💵 USD, 💶 EUR, 💷 GBP, 💴 JPY, 🏔️ CHF, 🛢️ CAD, 🦘 AUD, 🥝 NZD, 🥇 XAU. Bias: 🟢 bullish, 🔴 bearish, 🟡 two-sided. Conviction: 🔥🔥🔥 high, 🔥🔥 medium, 🔥 low.
- Section separator line: `━━━━━━━━━━━━━━━━━━`.
- Every post and note contains at least one chart placeholder line: `📸 >>> PASTE CHART HERE <<<` (the user replaces it with a chart and copies it where he wants more).
- Titles (weekly ideas only) must be 58 characters or fewer (TradingView cuts longer ones). Check in code. Pattern: `PAIR: <favoured character> vs <other character> | Wnn`.
- Copy buttons always copy plain text (no rich formatting).

## 2. Tone and originality

Friendly storytelling, not a report. A hook in the first lines, a little suspense, flowing sentences that make people want to read on. Keep some technical content (scores, priced probabilities, key data, spreads) but explain each term in a few words. Each currency is a "character" with a short name (≤ 20 characters, used in titles and the 🎬 line) and a one-line hook.

**Every post must be original (user decision, 11 Nov 2026).** The user posts many pairs that share a currency (EURUSD, GBPUSD, EURGBP…), so the same text must never appear in two posts. Write the hook, both section headers, both currency paragraphs and the plot-twist bullets fresh for each pair: same facts and numbers, different words, told from the angle of that matchup (e.g. "the euro's trouble against a dollar with fresh legs" vs "the euro's trouble against a franc that pays nothing"). Rotate the closing question (include the pair name) and the disclaimer from a pool of variants.

Section headers are unique too (user decision, 11 Nov 2026): never reuse a currency's character title across pairs; each pair gets its own header for each leg (e.g. EURUSD "The dollar finds its swagger", GBPUSD "The greenback reloads").

Check in code that no run of 8 consecutive words appears in two posts of the same batch, across hook, headers, paragraphs and twists (the bias box, the dates list, NEXT UP items, the chart-guide legend pool, the plot-twist closing-line pool and the disclaimer pool are exempt). The same rule applies to daily notes and week wrap-up notes: each pair's hook, descriptive paragraph and "what changed" / "what happened" text is written for that pair; the same fact for a shared currency (e.g. a Fed speech in EURUSD, GBPUSD and USDJPY) is told with different words and from that matchup's angle.

## 3. Weekly idea (after PHASE 2)

Only the start-of-week analysis. Never include news from after the FINAL cutoff (those go only in daily notes, when they happen).

Order:
1. `$FOREXCOM:PAIR`
2. `[b]🎬 <base character> vs <quote character>[/b]`
3. Hook paragraph written for this pair (one or two sentences; for two-sided pairs, a stand-off).
4. `[quote]` box: `[b]🟢/🔴/🟡 Week nn bias: BULLISH/BEARISH (CCY favoured) | 🔥… conviction[/b]`, the two scores with emojis, scale −18 to +18 and the gap, the week's dates.
5. Chart placeholder.
6. Separator, then `[b]<emoji> BASE · <pair-specific header>[/b] [i](score ±n)[/i]` with the base currency's paragraph written against this quote currency, then the same for the quote currency. Headers are unique per pair (§2).
7. `[b]⚡ PLOT TWIST: what could flip the story[/b]` as a `[list]` of 2–3 pair-specific bullets (from the thesis-card invalidation conditions of both legs). Include at least one bullet per leg (the chart note in §3a takes one bullet for each currency).
8. `[b]📅 DATES TO CIRCLE[/b]` as `[list=1]`: up to 5 upcoming catalysts for the two legs (weekday, date, event, currency).
9. Separator, a closing question that names the pair (rotate variants).
10. A disclaimer line in italics (rotate variants), always saying it is a fundamental bias, not a trade signal.

"Final touches" box on each card (not inside the post): Type Analysis; Investment Strategy = Long for bullish, Short for bearish, Neutral for two-sided or low conviction; Category Fundamental analysis; tags (fundamentalanalysis, forex, the two codes, the two central banks or themes; XAUUSD: fundamentalanalysis, gold, usd, fed, safehaven) with a Copy tags button; Related idea = last week's idea for the same pair.

## 3a. Chart kit (each weekly card, between Final touches and Preview — user decision, 11 Nov 2026)

Purpose: the user draws the week on his daily chart so the published idea is not an empty chart, and viewers can press TradingView's play button to watch the week unfold. It is a volatility envelope, never a target or a signal. The model's bias does NOT move the box; it only marks which half the bias favours.

Inputs (compute in code):
- Volatility: standard deviation σ of the pair's weekly log returns over the 26 weeks before the baseline Friday close. Source, in order: (1) archived Daily Observer exports once 26 weeks of closes exist; (2) the GitHub Action file `exports/fx-vol-latest.json` in calexi07/Analyst (user decision 12 Nov 2026: no Chrome needed): `curl -sS https://raw.githubusercontent.com/calexi07/Analyst/main/exports/fx-vol-latest.json` — use it only if its `baseline_friday` is the Friday before the target week; it holds `close` (reference Friday close) and `sigma_pct` per pair, computed every Saturday 05:00 UTC and Sunday 10:00 UTC from Yahoo Finance (FX = PAIR=X, gold = GC=F futures); (3) only if that file is missing or stale: Yahoo Finance through Claude in Chrome (same method, reference script scripts/fx-vol.mjs in the repo); (4) if none is available, show the kit without prices and say "volatility data unavailable"; never use figures from memory. Save the inputs used as claude/tradingview/vol-YYYY-Www.json.
- Reference Friday close: from the same source, labelled "reference; type your chart's Friday close". The page has an input per pair; the levels recompute in the browser from the typed close.

Kit layout (user's own chart style, decided 11 Nov 2026): one table per pair with columns **Drawing | #1 (bottom) | #2 (top) | Style**, matching TradingView's Rectangle → Coordinates dialog (#1 = bottom price, #2 = top price), plus a line "Bars: Mon <date> → Fri <date> (5 daily candles)". Labels in plain English, no σ symbols on the chart. Rows and styles:
- Week starts here: Friday's close (one value across both columns); "Blue line, extend right".
- Week marker: vertical line at Monday's open with the text "Week nn · Bearish/Bullish/Two-sided"; red for bearish, green for bullish, grey for two-sided.
- Typical week: close × e^(−σ) / close × e^(+σ) (about 2 of 3 weeks stay inside); "Dark blue border, light blue fill, blue label".
- Big-news week: close × e^(−2σ) / close × e^(+2σ); "Black dashed lines, no fill, black label".
- Bias side: bearish → from the big-news-week bottom to Friday's close, "Red-pink fill, red label"; bullish → from Friday's close to the big-news-week top, "Green fill, green label"; two-sided → the line "Two-sided pair: no bias side to shade."
Below the table:
- 📌 News pins for the 4H chart: that pair's catalysts inside the week with day and Bucharest time from the PHASE 1 catalyst calendar ("time not verified" when n/v); short labels (e.g. "US CPI").
- 💡 Plot-twist note (Copy note text button), for a note on the chart, visually pleasant, exactly one condition per currency, chosen in code by matching each bullet to its leg (keywords: currency name, central bank, country, key commodity), never two bullets about the same currency (user decision, 11 Nov 2026):
  `⚡ PLOT TWIST WATCH ⚡` / blank line / `<base emoji> <base-leg bullet>` / blank line / `<quote emoji> <quote-leg bullet>` / blank line / a closing line from a small pool (directional: e.g. "👀 Until then, the story stays on track."; two-sided: e.g. "🤝 Until one of these happens, it stays a stand-off."). Leg emoji = the currency emoji of the leg the bullet is about. News conditions only, never price levels.
- Two legend buttons, both WITHOUT prices, pins or flags (user decision, 11 Nov 2026): "Copy chart guide (article)" = BBCode `[b]🗺️ …[/b]` + `[list]`; "Copy legend (chart text box)" = the same lines as plain text. Lines use the chart's own label names: 🔵 Week starts here, 🟦 Typical week (with the pair name), ⬛ Big-news week, 🟥/🟩 Bias side (omitted for two-sided pairs). Rotate among several wordings so pairs do not repeat.
- Decimals: 5 for most pairs, 3 for JPY pairs, 2 for XAUUSD.
- A hint line: what "typical week" means, the 26-week window and percentage, and "Not a target and not a signal."

Daily vs 4H: the weekly idea is published on the daily chart with the boxes; daily-note updates use 4H snapshots carrying the news pins (vertical lines, visible on intraday intervals only) and the check flags.

## 4. Daily note (after each daily check)

Shorter, same style, no ticker and no title:
1. `[b]📍 DAILY CHECK · <Ddd D Mon> (morning|evening)[/b]`
2. `[b]<hook sentence>[/b]` matching the status, then on the next line a descriptive paragraph (about 40–80 words) written for this pair: what the day meant for this matchup, why the read holds or moves, what tension is building. Unique per pair (§2).
3. `[quote]` box: `[b]<status>[/b]`, the week's bias with both scores, and "Published gap X → today's read Y" (shadow; show both scenarios if the check has two).
4. Chart placeholder, separator.
5. `[b]🔄 WHAT CHANGED[/b]` as a `[list]`: one or two story sentences per leg (new data, central-bank news, with numbers), worded differently in every pair that shares the currency. If nothing new, say so in this pair's own words (never one shared "Quiet day…" line).
6. `[b]👀 NEXT UP[/b]` as a `[list]`: the next catalysts for the two legs.
7. `[i]⚠️ Fundamental check, not a trade signal.[/i]`

On each daily card (not inside the note), a chart-flag line: "🚩 Chart flag for this check: <flag> on the 4H candle of the check", where ✅ and 🟡 statuses → ✓ green flag; 👀 and ⚠️ → ! amber flag; ❌ → ✗ red flag; ⚪ → – grey flag (two-sided).

Status labels (from the check's pair groups): ✅ CONFIRMED; ✅ CONFIRMED · getting stronger; ✅ CONFIRMED · could get even stronger; 🟡 CONFIRMED · but fragile (|gap| = 3); 👀 UNDER WATCH (scenario-dependent); ⚠️ UNDER PRESSURE (invalidation wording met but model bias unchanged); ❌ INVALIDATED (shadow bias differs); ⚪ STILL TWO-SIDED.

## 5. Week wrap-up note (after PHASE 3)

Closes the story of the completed week, added under that week's idea:
1. `[b]🏁 WEEK nn WRAP-UP · how the story ended[/b]`
2. `[b]<hook sentence>[/b]` ("The story played out", "Plot twist: the market had other ideas", "Not much happened"), then a short descriptive paragraph unique to the pair.
3. `[quote]` box: the week's bias and conviction, the realised weekly move in % and in σ (from the PHASE 3 review), whether the week closed inside the typical-week box, and the result: ✅ HIT, ❌ MISS or ➖ FLAT (flat band ±0.25σ; two-sided pairs: "no call").
4. Chart placeholder, separator.
5. `[b]📖 What happened[/b]`: two or three plain sentences per leg on what drove the week (from the PHASE 3 attribution; for a miss, the reason in plain words, e.g. "news after the forecast", "already priced", "market flows"), worded uniquely per pair.
6. `[b]🧠 Lesson[/b]`: one sentence (no rule changes; one week proves nothing).
7. `[b]🔜 Next week's story drops Monday.[/b]` and the disclaimer line.

## 6. Delivery

- One self-contained, phone-friendly HTML page per week (dark style as in the Week 46 page): tabs for Weekly ideas, Daily notes (one sub-section per check, newest first) and Wrap-up; filter box; per pair a status tag, Copy title / Copy post / Copy note / Copy tags buttons (plain-text clipboard copy of the BBCode), the chart kit on weekly cards, the chart flag on daily cards, and a collapsible preview that renders the BBCode.
- Publish it as an artifact (republish the same artifact for the same week when possible; otherwise create one) if the artifact tool is available; otherwise send the HTML with SendUserFile. Also save the posts' text as claude/tradingview/tv-YYYY-Www.md (replace) so later runs can extend the same week's page. When republishing, keep the existing chart kits and earlier daily sections.
- Tell the user in one Romanian line that the posts are ready and what changed.

## 7. Current week's page

- Week 46: artifact "TradingView Ideas — Week 46", slug 831679cb-f60f-45d7-b3fb-4a5ce09f204e (https://claude.ai/artifact/HBs1ZHK4H19Zc6EuNQBDm7). Daily notes for Week 46 republish this artifact (read its current version first; add a new daily-notes section, keep the weekly ideas unchanged).
- From Week 47 on, the PHASE 2 run creates the week's page and records its slug here (append a line; never delete older lines).
- Week 47: artifact "TradingView Ideas Week 47", https://claude.ai/artifact/A77yqCvS8QtfPpWy14jMhk (created by the W47 PHASE 2 run, 15 Nov 2026). Daily notes for Week 47 republish this artifact (read its current version first; add a daily-notes section, keep the weekly ideas and kits unchanged).
