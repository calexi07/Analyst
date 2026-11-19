# DAILY OBSERVER IMPORTS — stories and daily checks (user decision, 12 Nov 2026)

The Daily Observer app (calexi07/Analyst, index.html) has a "Check" page in the "Fundamental Analyse" menu group (formerly History / Fundamental check) with the tabs Daily checks, Stories, Bias history and This week, and shows the week's story and the day's check notes inside the Calendar (day page and week panel). The app reads two JSON blocks, both pasted in Import / export → "Import fundamental analysis or daily check" (the app recognises the format).

## 1. Weekly import (PHASE 1 and PHASE 2): `daily-observer-fundamentals` v1 + `stories`

The user approved one addition to the §10 contract on 12 Nov 2026: an optional top-level key `stories`, placed after `news`. Everything else in §10 is unchanged (same fields, enums and version 1). Validation checks 4 and 6 accept `stories` as the only extra key.

```
"stories": {
  "EURUSD": { "title": "<TV title, ≤58 chars>", "text": "<the full TradingView weekly idea, BBCode>", "tags": "<comma-separated tags>" },
  … all 29 pairs in §2 order …
}
```
- PHASE 1: write the 29 weekly stories per claude/prompts/TV_POSTS.md §2–§3 from the PHASE 1 vintage and put them in `stories` (the chart kit is not part of the JSON).
- PHASE 2: rebuild the stories from the FINAL vintage (they are the weekly ideas published to TradingView) and put them in the FINAL JSON.
- Extra validation in code: 29 stories, keys = the 29 pairs, every `text` starts with `$FOREXCOM:<PAIR>`, every `title` ≤ 58 characters, the 8-word originality check of TV_POSTS.md §2 passes.
- PHASE 2 only (user decision, 12 Nov 2026): each story also carries `kit`, the TradingView chart kit of TV_POSTS.md §3a, so the app shows the boxes inside the story popup:
  `"kit": { "week": NN, "monday": "Mon D Mon", "bars": "Mon D Mon → Fri D Mon (5 daily candles)", "close": <reference Friday close>, "close_date": "Fri D Mon", "sigma_pct": <σ %>, "dec": <decimals>, "bias": "bullish|bearish|two-sided", "pins": [ { "day": "Tue 10 Nov", "time": "15:30" | null, "label": "US CPI" } ], "twist": "<plot-twist note, plain text>", "legend_head": "<legend header>", "legend": ["<legend lines, pair and 🟥/🟩 filled in; no Bias side line when two-sided>"] }`
  Values must equal the kit published on the TV page (same close and σ from vol-YYYY-Www.json). If volatility was unavailable, set `close` and `sigma_pct` to null (the app then shows "no levels"). The app computes the boxes as close·e^(±σ) and close·e^(±2σ) and lets the user type his chart's Friday close.
- The app stores each story in do_weekly.details.story (section "Story (TV article)" in the import dialog).

## 2. Daily check JSON (every morning and evening check covering all pairs): `daily-observer-check` v1

```
{
  "format": "daily-observer-check", "version": 1,
  "date": "YYYY-MM-DD", "slot": "morning" | "evening", "check": <check number>,
  "time": "HH:MM Bucharest", "valid_week": { "year": 2026, "week": NN },
  "title": "Thu 12 Nov · morning check",
  "summary": "<two short BBCode lines: what happened, what is next (Bucharest times)>",
  "currencies": { "USD": { "score": <published S>, "shadow": <central shadow S>, "status": "<status text>", "note": "<one sentence>" }, … the nine codes … },
  "pairs": [ { "pair": "EURUSD", "status": "<status label of TV_POSTS §4>", "bias": "bullish|bearish|two-sided",
               "published_gap": <int>, "today_gap": <central int>, "read": "<today's read text, e.g. −5 (central) or −9 (if the yen is +6)>",
               "flag": "✓ green | ! amber | ✗ red | – grey", "hook": "<hook sentence>", "note": "<the full TV daily note, BBCode>" }, … 29 pairs in §2 order … ]
}
```
- Build it in code from the check's own numbers and the 29 TV daily notes (reference: claude/tools/do_check_json.py, which parses the notes).
- Save it as archive/do-checks/check-YYYY-MM-DD-<slot>.json and send it to the user with SendUserFile, with one Romanian line: "Import în Daily Observer → Import / export → lipește JSON-ul (ziua <date>, <dimineață/seară>)".
- Validation in code: strict JSON, 29 pairs in order, nine currencies, slot/date valid, every note non-empty.
- The app stores it in do_settings under the key `fcheck:<date>:<slot>`; importing the same day and slot again replaces it.

## 3. Automatic delivery to the app (user decision, 12 Nov 2026)

The Claude GitHub App is installed on calexi07/Analyst (the Daily Observer site, GitHub Pages). Every run that produces a Daily Observer JSON also commits it there, so the user never pastes it by hand:
1. Scheduled runs already have a checkout at /home/claude/analyst with push access (verified 13 Nov 2026): `cd /home/claude/analyst && git fetch origin main && git checkout -B main origin/main`. Only if that folder does not exist, call the add_repo tool (owner "calexi07", repo "Analyst", access "push") and follow its clone instructions. Do not use Chrome for this.
2. Write the file to `imports/`: weekly → `imports/YYYY-Www-phase1.json` or `imports/YYYY-Www-final.json` (the full fundamentals JSON with `stories`); check → `imports/check-YYYY-MM-DD-<slot>.json`.
3. Append an entry to `imports/index.json` → `files`: `{ "id": "<file name without .json>", "file": "imports/<file name>", "kind": "fundamentals" | "check" }`. Never remove or reorder existing entries; never reuse an id (a rerun of the same check uses `check-YYYY-MM-DD-<slot>-r2`).
4. Commit only those two files with a short message (e.g. "Bias Engine: W47 FINAL import" or "Bias Engine: check 2026-11-13 morning") and push to `main`. Do not touch any other file in the repo.
5. The app imports each new id once when it opens (and every 10 minutes while open), and shows "Imported automatically: …".
6. If add_repo, the clone or the push fails, say so in the Romanian summary and still send the JSON with SendUserFile so the user can paste it (Import / export).
