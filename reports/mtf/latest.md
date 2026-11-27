# Analiza MTF — vineri 27 nov 2026, 10:02 București (sesiunea de dimineață, înainte de Londra)

**Date:** cel mai vechi și cel mai nou „ultimul rând” = EURUSD 27 nov 09:00 (lumânarea 09:00–10:00, închisă; 1h02 la rulare, sub pragul de 2h). Celelalte 28 de perechi: fără CSV. Exportul `fsb-export` pornit la 10:01 (run 45962487071) s-a terminat cu succes; `meta.json`: EURUSD 301 rânduri (300 seed + 1 live). · **Fundamental:** `imports/2026-W48-final.json` · **Check:** `imports/check-2026-11-27-morning.json` (06:00 București, neschimbat de la rularea de 09:45).

Presupuneri notate (rulare nesupravegheată):
- Rularea de 09:45 a fost făcută cu 17 minute înainte; singura lumânare nouă e 09:00. Analiza de fond rămâne cea din `2026-11-27-0945.md`; aici sunt doar verificarea și actualizările.
- Buffer-ul SL e recalculat cu ATR(14) 1H actual = 0.00076536 → 0.1×ATR = 0.0000765 (era 0.00007). Planul setup-ului existent e actualizat, nu dublat.
- **Corecție la varianta 2:** la 09:45 declanșatorul a fost dat ca 1.097045 (minimul fractal de la 06:00). Lumânarea 09:00 a coborât la 1.096955, sub acest nivel, fără ca fractalul 1H să se întoarcă (indicatorul păstrează trend 1H fractal ↑, CHoCH 1.093405). Deci 1.097045 nu era CHoCH-ul indicatorului. Declanșatorul corect = CHoCH-ul fractal 1H așa cum îl raportează indicatorul după atingerea zonei (acum 1.093405; după un nou maxim fractal în zonă, nivelul urcă). În `state.json` `trigger_level` = 1.093405 (valoarea curentă), cu această notă.

## Schimbări de la ultima rulare
- EURUSD-20261127-0945-1 (short A): rămâne **waiting**. Lumânarea 09:00: maxim 1.098235 < proximal 1.09933; minim 1.096955 > TP1 1.09573 (nu e anulat).
- Structură: 4H swing BOS a devenit gol (era 1.088115) — nivelul nou nu s-a format încă; restul structurilor identice. Watchlist: gol.

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

## EURUSD — Bias: bearish · Conviction: High (neschimbat)
Swing D și 4H bearish, fundamental bearish medium (EUR 0 vs USD +7, check ✅ CONFIRMED · could get even stronger).

**Structura acum** (rândul 27 nov 09:00, close 1.09764; ATR(14) 1H = 0.00076536):
- D: swing ↓ CHoCH 1.17116, BOS gol · internal ↓ CHoCH 1.127315, BOS gol · fractal ↓ CHoCH 1.101015, BOS 1.088115, pos 73.8%
- 4H: swing ↓ CHoCH 1.127315, BOS gol (nou) · internal ↓ CHoCH 1.100585, BOS 1.09573, pos 39.3% · fractal ↓ CHoCH 1.100585, BOS 1.088115, pos 76.4%
- 1H: swing ↓ CHoCH 1.101015, BOS 1.088115, pos 73.8% · internal ↑ CHoCH 1.09313, BOS 1.09893, pos 77.8% · fractal ↑ CHoCH 1.093405, BOS 1.0993, pos 71.8%
- Zone: D supply rafinată 1.09664–1.101015, testată 4x · 4H supply rafinată 1.097345–1.100585, testată 5x (prețul în ea) · 1H supply 23 nov 14:00 rafinată 1.09933–1.100585 proaspătă (maxim de atunci 1.0993) · 1H demand 25 nov 19:00 rafinată 1.093405–1.09486 proaspătă.

**Știri 24h:** S&P review Franța (HIGH, dată neconfirmată, probabil după închidere), half-day Wall Street (închidere 20:00). Nicio știre CRITICAL.

### Setup 1 — pro-trend · SHORT · A (actualizat) — EURUSD-20261127-0945-1
- Zona: supply 1H rafinată 1.09933–1.100585 · Invalidare: închidere 1H peste 1.100585; anulat dacă TP1 1.09573 e atins fără intrare.
- **Varianta 1 — limit:** entry 1.09933 · SL 1.100662 (1.100585 + 0.0000765) · 13.3 pips
  - TP1 1.09573 (BOS 4H internal) 2.70R · TP2 1.09486 (proximal demand 1H) 3.36R · TP3 1.088115 (BOS 1H swing / D fractal) 8.42R
- **Varianta 2 — confirmare:** declanșator = închidere 1H sub CHoCH-ul fractal 1H raportat de indicator după atingerea zonei (acum 1.093405).
  - Formula: entry = 50% din piciorul dintre maximul atins în zonă și minimul lumânării de break; SL = maximul atins + 0.0000765.
  - Exemplu: maxim 1.10000, minim lumânare de break 1.09690 → entry 1.09845, SL 1.100077 (16.3 pips). TP1 1.67R · TP2 2.21R · TP3 6.35R.
- Valabil până vineri 27 nov, 22:00. Riscuri: neschimbate (SL sub lichiditatea 1.101015; 4H swing în discount; zone HTF testate repetat; S&P Franța → gap în weekend; lichiditate redusă SUA).

### Setup 2 — counter-trend · LONG · C ⚠ contra fundamentalului — doar de urmărit
- Demand 1H 1.093405–1.09486. V1: entry 1.09486 · SL 1.093328 (15.3 pips) · TP1 1.097345 1.62R · TP2 1.0993 2.90R. V2 exemplu: minim 1.09400, break 1.09560 → entry 1.09480, SL 1.093923 (8.8 pips), TP1 2.90R, TP2 5.13R. Valabil până vineri 22:00.

## Restul perechilor
GBPUSD, USDJPY, USDCHF, USDCAD, AUDUSD, NZDUSD, EURGBP, EURJPY, EURCHF, EURAUD, EURNZD, EURCAD, GBPJPY, GBPCHF, GBPAUD, GBPNZD, GBPCAD, AUDJPY, AUDCHF, AUDNZD, AUDCAD, NZDJPY, NZDCHF, NZDCAD, CADJPY, CADCHF, CHFJPY, XAUUSD: **date lipsă**. Nu există CSV în `data/fsb/` (nici seed, nici rânduri live de la webhook), deci nu primesc setup-uri. Biasul fundamental e în tabel doar ca referință.

_Analiză condiționată, nu semnal de tranzacționare. Mărimea poziției nu e dată._
