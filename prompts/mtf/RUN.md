# Analiza MTF programată — procedura unei rulări (09:00 · 14:30 · 19:00 București, luni–vineri)

Rulezi singur, nimeni nu te urmărește. Nu pui întrebări: iei interpretarea cea mai rezonabilă și o notezi în raport.
Regulile de analiză sunt în `prompts/mtf/ANALYST.md` (le citești întâi și le aplici întocmai). Aici e doar procedura.
Raportul e în română. Fișierele de stare sunt JSON.

## 1. Datele
1. Repo-ul `calexi07/Analyst` (cd în el, `git pull`).
2. Pornești exportul proaspăt: `gh workflow run fsb-export.yml -R calexi07/Analyst`, apoi aștepți să se termine
   (`gh run list -w fsb-export.yml -L 1 -R calexi07/Analyst` + `gh run watch <id> -R calexi07/Analyst`, maxim 10 minute) și `git pull`.
   Dacă nu reușește, continui cu fișierele existente și scrii în raport „date neactualizate” cu ora ultimului rând.
3. `node scripts/fsb-digest.mjs` → `data/fsb/digest.json`: starea celor 9 structuri, zonele (proaspătă / testată / invalidată), ATR(14) 1H și schimbările din ultimele 48 de ore, pentru fiecare pereche.
   Folosești digest-ul ca bază și deschizi `data/fsb/<PERECHE>.csv` doar pentru verificări punctuale (de exemplu dacă un nivel a fost atins după o anumită oră). Toate calculele (R:R, pips, atingeri) le faci în cod.
4. Fundamentalul e local, în `imports/`: din `imports/index.json` iei cel mai nou `kind:"fundamentals"` (`YYYY-Www-final.json`, altfel `phase1`) și cel mai nou `kind:"check"`.
5. Setup-urile existente:
   - `reports/mtf/state.json`: setup-urile propuse de rulările anterioare.
   - `data/fsb/watchlist.json`: planurile mele active din Daily Observer (pair, dir, trend, text = motivație, for_day). Le verifici și pe ele, dar nu le modifici; le marchezi „din Watchlist”.

O pereche fără CSV sau cu ultimul rând mai vechi de 3 ore (în timpul pieței) apare în tabel cu „date lipsă” și nu primește setup-uri noi.

## 2. Verificarea setup-urilor existente (întâi)
Pentru fiecare setup din `state.json` cu starea `waiting`, `armed` sau `open`, pe lumânările 1H de după `checked_at`:
- `waiting` (prețul n-a ajuns în zonă) → `armed` când atinge zona; → `invalidated` dacă se îndeplinește condiția de invalidare; → `expired` după `valid_until`.
- `armed` → la varianta 2: `confirmed` când apare declanșatorul. Atunci calculezi entry-ul și SL-ul reale după formulă (cu extrema reală atinsă în zonă) și le scrii.
- Intrarea limit (varianta 1) sau entry-ul confirmat atins → `open` (virtual). Apoi `sl_hit` sau `tp1_hit` / `tp2_hit` / `tp3_hit`. Dacă o lumânare atinge și SL și TP, se socotește SL.
- Orice schimbare de stare: motivul pe un rând și ora lumânării.
Pentru planurile din Watchlist spui doar: încă valid / validat / invalidat, cu motivul din structură.

## 3. Setup-uri noi
Pentru fiecare pereche cu date: aplici `ANALYST.md` (piloni, clasă, conviction, plan de execuție cu ambele variante).
- Setup-uri `[4H]` și `[1H]`, cu pragul de calitate și regula SKIP din ANALYST.md 4b. Maxim 2 active pe pereche. Nu dublezi un setup care există deja în aceeași zonă și direcție: îl actualizezi.
- Declanșatoarele 4H le verifici pe lumânări 4H construite din CSV-ul de 1H (intervale 00–04, 04–08, 08–12, 12–16, 16–20, 20–24, ora București). Digest-ul are deja `atr14_4h`.
- Setup-urile C și NO TRADE nu intră în `state.json`; apar doar în tabel.
- `valid_until`: cel mult vineri 22:00, sau mai devreme dacă planul o cere.

## 4. Ce scrii
1. `reports/mtf/YYYY-MM-DD-HHMM.md` (ora rulării, București), în ordinea:
   - un rând cu ora datelor (cel mai vechi și cel mai nou „ultimul rând”), săptămâna fundamentală și check-ul folosit;
   - **Schimbări de la ultima rulare**: setup-uri confirmate, deschise, invalidate, TP/SL lovite, plus planurile din Watchlist validate sau invalidate;
   - **Pe scurt** (prima parte, ANALYST.md 5.2a): toate perechile cu setup activ sau schimbat, în cuvinte simple, fără prețuri de structură; perechile SKIP grupate într-un singur rând („SKIP: EURGBP, CHFJPY, … — nimic calitativ”);
   - **Tabelul sumar**, toate cele 29 de perechi (formatul din ANALYST.md 5.1);
   - **Tehnic**: detaliu complet doar pentru setup-urile A+, A și B noi sau schimbate, cu planul de execuție; restul perechilor câte un rând.
2. `reports/mtf/latest.md`: copie a raportului.
3. `reports/mtf/state.json`: actualizat. Fiecare setup are: `id` (PERECHE-YYYYMMDD-HHMM-n), `pair`, `tf` (4H / 1H), `dir`, `type` (pro-trend / counter-trend), `class`, `zone` [low, high], `invalidation`, `plan_limit` {entry, sl, tp[]}, `plan_confirm` {trigger_level, trigger_tf, formula, entry, sl, tp[]} (entry și sl null până la confirmare), `valid_until`, `status`, `history` [{time, status, why}], `created_at`, `checked_at`. Setup-urile închise rămân în fișier 7 zile, apoi le scoți.
4. Commit și push: `git add reports/mtf && git commit -m "MTF analysis <data ora>" && git pull --rebase && git push`.

## 5. Mesajul către mine
Un singur mesaj scurt (SendUserMessage), pentru telefon:
- primul rând: ora și „X schimbări · Y setup-uri A+/A noi”;
- schimbările importante (maxim 5 rânduri);
- setup-urile A+/A noi, în stilul „Pe scurt”: o propoziție cu povestea plus rândul „Entry · SL · TP”;
- link: https://github.com/calexi07/Analyst/blob/main/reports/mtf/latest.md
Dacă nu s-a schimbat nimic și nu există setup A+/A nou, mesajul are un singur rând.

## Reguli
- Nu inventezi date. Ce lipsește apare ca „indisponibil”.
- Nu modifici nimic în afara `reports/mtf/` (scripturile și datele nu se ating).
- Nu tranzacționezi și nu trimiți nimic altundeva.
