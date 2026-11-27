# Analiza MTF — vineri 27 nov 2026, 09:45 București (sesiunea de dimineață, înainte de Londra)

**Date:** cel mai vechi și cel mai nou „ultimul rând” = EURUSD 27 nov 08:00 (lumânarea 08:00–09:00, 1h45 la rulare, sub pragul de 2h). Celelalte 28 de perechi: fără CSV. Exportul `fsb-export` a rulat cu succes la 09:43, dar `meta.json` arată 0 rânduri live (webhook) și 300 rânduri seed doar pentru EURUSD. · **Fundamental:** `imports/2026-W48-final.json` · **Check:** `imports/check-2026-11-27-morning.json` (06:00 București).

Presupuneri notate (rulare nesupravegheată):
- Prima rulare: `state.json` era gol, Watchlist-ul e gol → nimic de verificat.
- Premium/discount pentru short-ul EURUSD: zona e în premium pe D fractal (~87%), 1H swing și 4H internal, dar în discount pe 4H swing (~29%). Am considerat pilonul zonei îndeplinit pe range-urile de execuție și am trecut 4H swing la riscuri.
- Declanșatorul variantei 2 = închiderea 1H dincolo de CHoCH-ul fractal 1H așa cum îl actualizează indicatorul după atingerea zonei; nivelul de azi e dat doar ca exemplu.

## Schimbări de la ultima rulare
Niciuna (prima rulare; Watchlist gol).

## Tabel sumar
| Pereche | D / 4H / 1H swing | Fundamental | Conviction | Cel mai bun setup | Clasă |
|---|---|---|---|---|---|
| EURUSD | ↓ / ↓ / ↓ (1H internal + fractal ↑ = pullback) | bearish (medium) · check: ✅ CONFIRMED | High | Short pro-trend din supply 1H proaspăt 1.09933–1.100585 | A |
| GBPUSD | date lipsă | bearish (medium) · check: ⚠️ UNDER PRESSURE | — | NO TRADE (date lipsă) | — |
| USDJPY | date lipsă | bullish (medium) · check: 👀 UNDER WATCH | — | NO TRADE (date lipsă) | — |
| USDCHF | date lipsă | bullish (low) · check: ✅ CONFIRMED | — | NO TRADE (date lipsă) | — |
| USDCAD | date lipsă | bullish (medium) · check: ✅ CONFIRMED | — | NO TRADE (date lipsă) | — |
| AUDUSD | date lipsă | bearish (medium) · check: ⚠️ UNDER PRESSURE | — | NO TRADE (date lipsă) | — |
| NZDUSD | date lipsă | bearish (low) · check: ✅ CONFIRMED | — | NO TRADE (date lipsă) | — |
| EURGBP | date lipsă | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (date lipsă) | — |
| EURJPY | date lipsă | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (date lipsă) | — |
| EURCHF | date lipsă | two-sided (low) · check: ⚪ STILL TWO-SIDED | — | NO TRADE (date lipsă) | — |
| EURAUD | date lipsă | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (date lipsă) | — |
| EURNZD | date lipsă | two-sided (low) · check: ❌ INVALIDATED | — | NO TRADE (date lipsă) | — |
| EURCAD | date lipsă | bullish (medium) · check: 👀 UNDER WATCH | — | NO TRADE (date lipsă) | — |
| GBPJPY | date lipsă | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (date lipsă) | — |
| GBPCHF | date lipsă | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (date lipsă) | — |
| GBPAUD | date lipsă | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (date lipsă) | — |
| GBPNZD | date lipsă | two-sided (low) · check: ❌ INVALIDATED | — | NO TRADE (date lipsă) | — |
| GBPCAD | date lipsă | bullish (medium) · check: ✅ CONFIRMED · could get even stronger | — | NO TRADE (date lipsă) | — |
| AUDJPY | date lipsă | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (date lipsă) | — |
| AUDCHF | date lipsă | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (date lipsă) | — |
| AUDNZD | date lipsă | two-sided (low) · check: ❌ INVALIDATED | — | NO TRADE (date lipsă) | — |
| AUDCAD | date lipsă | bullish (medium) · check: ✅ CONFIRMED · could get even stronger | — | NO TRADE (date lipsă) | — |
| NZDJPY | date lipsă | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (date lipsă) | — |
| NZDCHF | date lipsă | two-sided (low) · check: ❌ INVALIDATED | — | NO TRADE (date lipsă) | — |
| NZDCAD | date lipsă | bullish (low) · check: ⚠️ UNDER PRESSURE | — | NO TRADE (date lipsă) | — |
| CADJPY | date lipsă | bearish (medium) · check: ✅ CONFIRMED · could get even stronger | — | NO TRADE (date lipsă) | — |
| CADCHF | date lipsă | bearish (low) · check: ✅ CONFIRMED | — | NO TRADE (date lipsă) | — |
| CHFJPY | date lipsă | two-sided (low) · check: ⚪ STILL TWO-SIDED | — | NO TRADE (date lipsă) | — |
| XAUUSD | date lipsă | two-sided (low) · check: ⚪ STILL TWO-SIDED | — | NO TRADE (date lipsă) | — |

## EURUSD — Bias: bearish · Conviction: High
Swing D și 4H sunt bearish, la fel ca biasul fundamental (EUR 0 vs USD +7, conviction medium, confirmat în check-ul de azi) → High.

**Structura acum** (rândul 27 nov 08:00, close 1.097685; ATR(14) 1H = 0.00069464 → buffer 0.1×ATR = 0.00007):
- D: swing ↓ CHoCH 1.17116, BOS gol (nu s-a format încă) · internal ↓ CHoCH 1.127315, BOS gol · fractal ↓ CHoCH 1.101015, BOS 1.088115, pos 74.2%
- 4H: swing ↓ CHoCH 1.127315, BOS 1.088115, pos 24.4% · internal ↓ CHoCH 1.100585, BOS 1.09573, pos 40.3% · fractal ↓ CHoCH 1.100585, BOS 1.088115, pos 76.7%
- 1H: swing ↓ CHoCH 1.101015, BOS 1.088115, pos 74.2% · internal ↑ CHoCH 1.09313, BOS 1.09893, pos 78.5% · fractal ↑ CHoCH 1.093405, BOS 1.0993, pos 72.6%
- Zone: D supply 1.09664–1.101015 (rafinată), testată de 4 ori · 4H supply 1.097345–1.100585 (rafinată), testată de 5 ori, prețul e acum în ea · 1H supply 23 nov 14:00, rafinată 1.09933–1.100585, **proaspătă** (maximul de după e 1.0993, cu 0.3 pips sub proximal; zona completă 1.09556–1.100585 a fost atinsă) · 1H demand 25 nov 19:00, rafinată 1.093405–1.09486, proaspătă (minimul de după e 1.09573).
- Ultima schimbare (48h): 1H internal ↓→↑ pe 25 nov 18:00. Interpretare: internal și fractal 1H contra swing-ului = pullback (ierarhia swing > internal > fractal).

**Fundamental:** bearish medium, gap −7 (check: −7 central, −9 dacă eșecul comisiei franceze e scorat ca stres). În următoarele 24–48h: PIB Franța T3 09:45 (MEDIUM), review-ul S&P pentru Franța (HIGH, data neconfirmată, de obicei după închiderea de vineri), balanța comercială SUA 15:30, ședință scurtă pe Wall Street (închidere 20:00). Nicio știre CRITICAL până la FOMC (9 dec).

**Ce urmăresc:**
- 1.100585: distalul zonei supply 1H/4H (CHoCH 4H internal și fractal)
- 1.101015: CHoCH 1H swing și D fractal. O închidere 1H peste el întoarce swing-ul 1H și îmi schimbă părerea pe termen scurt.
- 1.0993: BOS fractal 1H, adică lichiditatea chiar sub zonă
- 1.09573 / 1.09313: BOS 4H internal / CHoCH 1H internal. Sub 1.09313, pullback-ul 1H s-a terminat.

### Setup 1 — pro-trend · SHORT · A (4/5: D ✓ 4H ✓ zonă ✓ fundamental ✓; structura de intrare încă ↑)
- Zona: supply 1H rafinată 1.09933–1.100585 (în interiorul supply-ului 4H/D)
- Când e valid: prețul atinge 1.09933. Pentru A+, fractalul 1H trebuie să se întoarcă ↓ (varianta 2), cu condiția să nu apară o știre CRITICAL.
- Invalidare: închidere 1H peste 1.100585 (distal). Anulat și dacă se atinge TP1 1.09573 fără intrare.
- **Varianta 1 — limit:** entry 1.09933 · SL 1.100655 (1.100585 + 0.00007) · 13.2 pips
  - TP1 1.09573 (BOS 4H internal) 2.72R · TP2 1.09486 (proximal demand 1H) 3.37R · TP3 1.088115 (BOS swing 4H/1H) 8.47R
- **Varianta 2 — confirmare:** declanșator = închidere 1H sub CHoCH-ul fractal 1H după atingerea zonei (azi, ultimul fractal low e 1.097045, de la 06:00; nivelul se actualizează când se sparge 1.0993).
  - Formula: entry = 50% din piciorul dintre maximul atins în zonă și minimul lumânării de break; SL = maximul atins + 0.00007.
  - Exemplu: maxim 1.10000, minimul lumânării de break 1.09690 → entry 1.09845, SL 1.10007 (16.2 pips). TP1 1.09573 1.68R · TP2 1.09486 2.22R · TP3 1.088115 6.38R.
- Valabil până vineri 27 nov, 22:00.
- Riscuri:
  - SL-ul stă sub 1.101015 (CHoCH 1H swing), unde e lichiditate și poate fi vânat.
  - Pe 4H swing prețul e în discount (~29% la zonă).
  - Zonele 4H și D din jur sunt deja testate de mai multe ori.
  - Review-ul S&P pentru Franța poate veni după închidere: risc de gap în weekend.
  - Lichiditate redusă în SUA (half-day).

### Setup 2 — counter-trend · LONG · C ⚠ contra fundamentalului (2/5: structura de intrare ✓, zona ✓) — doar de urmărit, nu intră în state.json
- Zona: demand 1H rafinată 1.093405–1.09486, proaspătă. Invalidare: închidere 1H sub 1.093405.
- **Varianta 1:** entry 1.09486 · SL 1.093335 (15.2 pips) · TP1 1.097345 (proximal supply 4H) 1.63R · TP2 1.0993 2.91R
- **Varianta 2:** închidere 1H peste CHoCH-ul fractal 1H bearish după atingere.
  - Exemplu: minim 1.09400, maximul lumânării de break 1.09560 → entry 1.09480, SL 1.09393 (8.7 pips). TP1 2.93R, TP2 5.18R.
- Valabil până vineri, 22:00.

## Restul perechilor
GBPUSD, USDJPY, USDCHF, USDCAD, AUDUSD, NZDUSD, EURGBP, EURJPY, EURCHF, EURAUD, EURNZD, EURCAD, GBPJPY, GBPCHF, GBPAUD, GBPNZD, GBPCAD, AUDJPY, AUDCHF, AUDNZD, AUDCAD, NZDJPY, NZDCHF, NZDCAD, CADJPY, CADCHF, CHFJPY, XAUUSD: **date lipsă**. Nu există CSV în `data/fsb/` (nici seed, nici rânduri live de la webhook), deci nu primesc setup-uri. Biasul fundamental e în tabel doar ca referință.

_Analiză condiționată, nu semnal de tranzacționare. Mărimea poziției nu e dată._
