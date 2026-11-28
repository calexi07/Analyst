# Analiza MTF programată — procedura unei rulări (luni–vineri: DIMINEAȚA 08:35 și SEARA 18:47, ora București)

Tipul rulării îl stabilești din ora București la pornire: înainte de 12:00 = **dimineață**, după = **seară**.
- **Dimineață**: recapitulezi **sesiunea New York de ieri** (15:30–23:00) și **sesiunea Asia de azi** (00:00–09:00), apoi ce urmăresc **azi** (Londra și New York).
- **Seară**: recapitulezi **sesiunea Londra de azi** (10:00–18:30) și ce urmăresc pe **New York** în continuare și peste noapte.
Analiza se face după regulile mele din `ANALYST.md` secțiunea 2b (HTF → LTF, veto de HTF, lichiditate, zone, intrări E1/E2/E3).

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
   - `data/fsb/watchlist.json`: planurile mele active din Daily Observer (`setups`: pair, dir, trend, text = motivație, for_day). Le verifici și pe ele, dar nu le modifici; le marchezi „din Watchlist”.
   - Setup-urile tale apar în Daily Observer → Watchlist ca „🤖 Propuse”. Decizia mea e în `watchlist.json` → `all`, cheia `wl:mtf:<id>`: lipsă = nedecis, `status` active = acceptat (poate fi editat de mine; atunci planul meu are prioritate la mesaj, dar tu urmărești în continuare planul tău original), `rejected` = respins. Pe cele respinse le urmărești mai departe în `state.json` (pentru statistică), dar nu le mai pomenești în mesaj. În `state.json` notezi la fiecare setup `decision`: undecided / accepted / rejected.

O pereche fără CSV sau cu ultimul rând mai vechi de 3 ore (în timpul pieței) apare în tabel cu „date lipsă” și nu primește setup-uri noi.
Dacă `data/fsb/meta.json` arată la o pereche `seed_vs_live.diff > 0` (istoria manuală și alertele nu coincid pe aceleași lumânări), perechea primește „date inconsistente” și nu primește setup-uri noi până se rezolvă; spui asta într-un rând.
O pereche cu mai puțin de 120 de rânduri în CSV (sub ~5 zile de istorie) apare cu „istorie insuficientă (n rânduri)” și nu primește setup-uri noi: starea zonelor (proaspătă / testată) nu se poate verifica. Poți descrie structura curentă într-un rând. Pentru a scurta perioada, utilizatorul poate trimite exporturi CSV manuale care se pun în `data/fsb/seed/`.

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

## 3b. Recapitularea sesiunii (în cod, din CSV-urile 1H)
Pentru fiecare pereche, pe lumânările sesiunii (vezi orele de sus):
- range-ul sesiunii (high, low, mișcarea în pips și în multipli de ATR 1H), direcția;
- ce lichiditate s-a luat: high/low-ul zilei anterioare, high/low-ul sesiunii precedente, stop hunt-uri (regula din ANALYST 2b-C5, pe 1H și pe 4H), cu fitil sau corp și ce a făcut prețul după;
- schimbările de structură din sesiune (D / 4H / 1H, swing / internal / fractal), din digest `changes_48h`;
- dacă prețul a intrat într-o zonă D sau 4H și cum a reacționat.
Plus, pe toată piața: puterea monedelor în sesiune (media celor 7 perechi ale fiecărei monede, cu semn), din cele 28 de perechi.
Dacă o sesiune nu are date (luni dimineață nu există NY „de ieri” = vinerea; folosești sesiunea NY de vineri), spui ce ai folosit.

## 4. Ce scrii
1. `reports/mtf/YYYY-MM-DD-HHMM.md` (ora rulării, București), în ordinea:
   - **🌍 Fundamental (contextul săptămânii)** — PRIMA secțiune, înaintea oricărei analize tehnice, din `imports/` (cel mai nou `YYYY-Www-final.json`, altfel `phase1`, și cel mai nou `check-*.json`):
     - un rând cu săptămâna, starea (FINAL / PHASE 1) și ora verificării zilnice folosite;
     - pentru fiecare din cele 29 de perechi, **textul exact** din postările TradingView, fără să-l rescrii: titlul din `stories[PERECHE].title` și primul paragraf al `stories[PERECHE].text` (de după rândul cu simbolul; scoți doar tag-urile BBCode și emoji-urile de formatare, păstrezi cuvintele), plus rândul de bias (`Week NN bias: … | … conviction`); apoi din verificarea zilnică `status` și `hook`, tot exact. Dacă `stories` lipsește, folosești `pairs[].summary`, `main_driver` și `currencies[].note`, exact;
     - perechile la care verificarea zilnică spune că biasul e slăbit sau pus sub semnul întrebării le marchezi ⚠.
     Fundamentalul se folosește **contextual** în toată analiza: la fiecare idee spui dacă e pro- sau contra-fundamental, citezi într-o frază motivul fundamental (din textul de mai sus) și știrile care o pot schimba. Nu schimbi și nu reinterpretezi biasul; nu inventezi cifre.
   - **Recapitularea sesiunii** (3b), în cuvinte simple: 5–8 rânduri despre ce a făcut piața (cine a fost puternic / slab, ce lichidități s-au luat, ce structuri s-au schimbat), apoi câte un rând pentru perechile cu mișcări sau evenimente notabile; restul grupate;
   - **De urmărit** (azi / pe New York): maxim 8 perechi, fiecare cu povestea în stilul ANALYST 2b-J (Daily → 4H → 1H, scurt), nivelul sau zona de urmărit și ce ar valida / anula ideea; plus știrile HIGH/CRITICAL ale intervalului (din `imports/`, cu ora București);
   - un rând cu ora datelor (cel mai vechi și cel mai nou „ultimul rând”), săptămâna fundamentală și check-ul folosit;
   - **Schimbări de la ultima rulare**: setup-uri confirmate, deschise, invalidate, TP/SL lovite, plus planurile din Watchlist validate sau invalidate;
   - **Overview** (chiar la început, înainte de orice detaliu), trei liste scurte, calculate în cod unde e posibil, câte un rând pe pereche:
     - 🎯 **Setup-uri bune acum**: setup-urile A+/A active (waiting/armed/confirmed), cu direcția, [4H]/[1H] și ce mai lipsește („așteaptă atingerea zonei” / „în zonă, așteaptă confirmarea” / „confirmat, limit la X”).
     - 📍 **Aproape**: perechile la care prețul e la cel mult 1 × ATR(14) 4H de zona unui setup activ (oricare clasă) sau de un nivel CHoCH/BOS de pe 4H sau D. Spui distanța în pips și ce ar însemna atingerea.
     - 👀 **De interes**: setup-urile B, schimbările de structură din ultimele ore (CHoCH pe 4H sau D, din digest `changes_48h`) și planurile mele din Watchlist validate sau invalidate.
     Dacă o listă e goală, scrii „—”. Restul perechilor nu apar în overview.
   - **Pe scurt** (după overview, ANALYST.md 5.2a), pereche cu pereche: toate perechile cu setup activ sau schimbat, în cuvinte simple, fără prețuri de structură; perechile SKIP grupate într-un singur rând („SKIP: EURGBP, CHFJPY, … — nimic calitativ”);
   - **Tabelul sumar**, toate cele 29 de perechi (formatul din ANALYST.md 5.1);
   - **Tehnic**: detaliu complet doar pentru setup-urile A+, A și B noi sau schimbate, cu planul de execuție; restul perechilor câte un rând.
2. `reports/mtf/latest.md`: copie a raportului.
3. `reports/mtf/state.json`: actualizat. Fiecare setup are: `id` (PERECHE-YYYYMMDD-HHMM-n), `pair`, `tf` (4H / 1H), `dir`, `summary` (partea „Pe scurt” a setup-ului: 2–3 propoziții simple plus rândul Entry · SL · TP; apare pe cardul din Daily Observer), `type` (pro-trend / counter-trend), `class`, `zone` [low, high], `invalidation`, `plan_limit` {entry, sl, tp[]}, `plan_confirm` {trigger_level, trigger_tf, formula, entry, sl, tp[]} (entry și sl null până la confirmare), `valid_until`, `status`, `history` [{time, status, why}], `created_at`, `checked_at`. Când un setup se închide (invalidated, expired, sl_hit, tp hit), adaugi în același timp o linie JSON cu setup-ul complet în `reports/mtf/closed.jsonl` (append-only; nu rescrii și nu ștergi liniile vechi). În `state.json` setup-urile închise rămân 7 zile, apoi le scoți.
4. Commit și push: `git add reports/mtf && git commit -m "MTF analysis <data ora>" && git pull --rebase && git push`.

## 5. Mesajul către mine
Un singur mesaj scurt (SendUserMessage), pentru telefon:
- primul rând: „🌅 Dimineață” sau „🌆 Seară”, ora și „X schimbări · Y setup-uri A+/A noi”;
- 🌍 fundamentalul în 2–3 rânduri: biasurile cele mai puternice ale săptămânii și hook-ul verificării zilnice pentru perechile din „De urmărit” (textul exact, scurtat doar dacă e prea lung);
- recapitularea sesiunii în 3–4 rânduri (moneda cea mai puternică / slabă, lichiditățile importante luate, schimbările de structură pe D/4H);
- „De urmărit”: maxim 5 rânduri, câte unul pe pereche;
- overview-ul pe scurt: 🎯 setup-uri bune, 📍 aproape, 👀 de interes, maxim 3 rânduri fiecare;
- schimbările importante (maxim 5 rânduri);
- setup-urile A+/A noi, în stilul „Pe scurt”: o propoziție cu povestea plus rândul „Entry · SL · TP”;
- link: https://github.com/calexi07/Analyst/blob/main/reports/mtf/latest.md
Dacă nu s-a schimbat nimic și nu există setup A+/A nou, mesajul are un singur rând.
Răspunsul final al sesiunii (textul de după ultimul tool) e tot în română și are cel mult 3 rânduri. Nu repeta mesajul și nu descrie pașii tehnici (git, hook-uri, fișiere de lucru).

## Reguli
- Nu inventezi date. Ce lipsește apare ca „indisponibil”.
- Nu modifici nimic în afara `reports/mtf/` (scripturile și datele nu se ating).
- Nu tranzacționezi și nu trimiți nimic altundeva.
