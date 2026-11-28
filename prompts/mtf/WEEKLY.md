# Analiza MTF — săptămâna încheiată + ce urmăresc săptămâna viitoare (sâmbătă, după închidere)

Raportul are trei părți, în ordinea asta:
1. **Săptămâna care a trecut** (piața): pentru toate cele 29 de perechi, citite după `ANALYST.md` 2b (Daily → 4H → 1H): ce s-a schimbat în structura D și 4H, ce lichidități importante s-au luat, ce zone D/4H au fost atinse și cum au reacționat, puterea monedelor pe săptămână (din cele 28 de perechi). În cuvinte simple: 6–10 rânduri pe toată piața, apoi un rând pe pereche (perechile fără nimic notabil grupate).
2. **Bilanțul setup-urilor** (secțiunile 2–3 de mai jos, neschimbate).
3. **Ce urmăresc săptămâna viitoare**: pentru fiecare pereche cu context clar, povestea HTF în stilul ANALYST 2b-J (direcția Daily, unde e prețul în swing / internal, zonele D și 4H relevante cu lichiditatea din jurul lor, ce ar valida și ce ar anula ideea), plus biasul fundamental al săptămânii viitoare (`imports/`, cea mai nouă săptămână `phase1` sau `final`) și știrile HIGH/CRITICAL cu ziua. Perechile fără context clar: un rând „fără idee — motiv”. Fără ordine, doar niveluri și condiții.


Rulezi singur, fără întrebări. Raportul e în română, scurt, ușor de citit pe telefon. Datele sunt în repo-ul `calexi07/Analyst`.

## 1. Ce citești
- `reports/mtf/closed.jsonl`: toate setup-urile închise (fiecare linie are `history` cu stările și orele).
- `reports/mtf/state.json`: setup-urile încă deschise.
- Rapoartele săptămânii: `reports/mtf/YYYY-MM-DD-HHMM.md`.
- `data/fsb/<PERECHE>.csv`: ce a făcut prețul după fiecare setup, plus perechile marcate SKIP.
- `imports/`: analiza fundamentală a săptămânii și verificările zilnice.
- `reports/mtf/proposals.md`: propunerile de îmbunătățire anterioare și statutul lor.

## 2. Bilanțul (în cod, nu din memorie)
Pentru săptămâna încheiată și cumulat de la început:
- Câte setup-uri pe fiecare stare: expirate fără atingere, invalidate, intrate, SL, TP1, TP2, TP3.
- Rezultatul virtual în R, la varianta folosită de setup (limit sau confirmare). Dacă o lumânare atinge și SL și TP, se socotește SL.
- Defalcat pe: clasă (A+/A/B), timeframe (4H/1H), pro-trend vs counter-trend, pro- vs contra-fundamental, pereche, și decizia mea (acceptat / respins / nedecis). Dacă cele respinse de mine ies mai bine sau mai rău decât cele acceptate, spui asta cu cifre.
- MFE și MAE în R pentru setup-urile intrate: cât a mers în favoarea ta și cât împotrivă, înainte de ieșire.
- **Ce a lipsit:** mișcările mari (peste 2 × ATR 4H) de pe perechile SKIP sau fără setup. Spui doar dacă regulile le-ar fi putut prinde și ce a blocat (zonă testată, R:R, contra fundamentalului etc.). E descriptiv, nu un semnal.
- Lângă fiecare cifră pui eșantionul (n). Sub 20 de setup-uri într-o categorie scrii „eșantion mic — orientativ”.

## 3. Propuneri de îmbunătățire (cu reguli stricte)
Poți propune îmbunătățiri ale regulilor din `prompts/mtf/ANALYST.md`, dar:
1. **Doar pe date reale.** Fiecare propunere citează cifrele care o susțin (n, R mediu, rata de reușită) și exemplele concrete (id-urile setup-urilor).
2. **Prag minim.** Nicio propunere pe mai puțin de 15 cazuri în categoria vizată. Sub prag scrii doar „de urmărit” și cifrele.
3. **Nu aplici nimic.** Nu modifici `ANALYST.md` sau `RUN.md`. Propunerea o aprob eu.
4. **Una câte una.** Maximum 2 propuneri pe săptămână, cele mai bine susținute. Fiecare spune exact ce regulă se schimbă (textul vechi → textul nou) și ce ar fi schimbat retroactiv pe cazurile existente.
5. **Atenție la ajustarea pe trecut.** Pentru fiecare propunere spui cum o verificăm în săptămânile următoare (pe setup-uri noi, nu pe aceleași). O regulă aprobată se reevaluează după minimum 3 săptămâni de date noi.
6. Ce s-a întâmplat în piață (știri, schimbări de fundamental) poate explica rezultatele, dar nu justifică singur o schimbare de regulă.

Propunerile le adaugi în `reports/mtf/proposals.md` (append): data, propunerea, datele, statut „propusă”. La propunerile vechi aprobate actualizezi rezultatul pe datele noi.

## 4. Ce scrii
- `reports/mtf/weekly-YYYY-Www.md`, în ordine:
  - **Pe scurt**: 5–6 rânduri despre ce a mers, ce n-a mers și propunerea principală, în cuvinte simple;
  - tabelele bilanțului;
  - ce a lipsit;
  - propunerile, cu datele lor.
- Actualizezi `reports/mtf/proposals.md`.
- Commit și push doar pentru `reports/mtf/`.
- Un mesaj scurt (SendUserMessage): 3 rânduri despre săptămâna pieței, top 5 perechi de urmărit săptămâna viitoare (câte un rând), rezultatul setup-urilor în R și n, cea mai bună și cea mai slabă categorie, propunerile pe un rând fiecare, link: https://github.com/calexi07/Analyst/blob/main/reports/mtf/ (fișierul weekly).

Dacă săptămâna n-a avut niciun setup închis, spui asta într-un rând și scrii doar „ce a lipsit”.
