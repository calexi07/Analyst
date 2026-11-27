# Analiza MTF — vineri 27 nov 2026, 11:02 București (sesiunea de dimineață, înainte de Londra)

**Date:** cel mai vechi și cel mai nou „ultimul rând” = 27 nov 10:00 (lumânarea 10:00–11:00, închisă; sub pragul de 2h) pentru toate cele 28 de perechi cu CSV. XAUUSD: fără CSV. Export `fsb-export` pornit la 11:01 (run 45970207117), terminat cu succes; `meta.json` 09:01:18 UTC. EURUSD 302 rânduri (300 seed + 2 live); celelalte 27 de perechi au **1 rând** (export live abia pornit). · **Fundamental:** `imports/2026-W48-final.json` · **Check:** `imports/check-2026-11-27-morning.json` (06:00 București).

Presupuneri notate (rulare nesupravegheată):
- Cele 27 de perechi noi au un singur rând → „istorie insuficientă (1 rând)”, fără setup-uri noi (RUN.md §1). Structura lor apare doar ca săgeți în tabel.
- Setup-ul EURUSD e **acceptat** în Watchlist (`wl:mtf:EURUSD-20261127-0945-1`, status active). Cardul din Watchlist păstrează declanșatorul vechi „1.0934” (sub TP1), corectat ulterior în `state.json`; urmăresc planul meu original, corectat.
- Buffer-ul SL actualizat la noul ATR(14) 1H (0.0000863) → SL limit 1.10067.

## Overview
🎯 **Setup-uri bune acum**
- EURUSD · Short · [1H] · A — așteaptă atingerea zonei 1.09933–1.100585 (acum 29 pips sub ea).

📍 **Aproape**
- EURUSD — la 7 pips de 1.09573 (BOS internal 4H = TP1 al setup-ului). Atingerea = continuare bearish pe 4H, dar anulează setup-ul short (TP1 atins fără intrare).

👀 **De interes**
- —

## Schimbări de la ultima rulare
- Nicio schimbare de stare. EURUSD-20261127-0945-1 rămâne **waiting** (lumânarea 10:00: max 1.09779 < 1.09933, min 1.0961 > TP1 1.09573). Decizie: **acceptat** de tine.
- Watchlist: planul tău EURUSD (din propunerea MTF) — **încă valid**: 1H swing tot bearish, zona de supply 1H proaspătă, neatinsă.
- Date noi: 27 de perechi au început exportul live (1 rând fiecare); XAUUSD încă lipsește.

## Pe scurt
**EURUSD** — Daily și 4H sunt bearish, fundamentalul la fel (dolarul mult mai puternic decât euro). Pullback-ul în sus de pe 1H a obosit: ultima oră a coborât spre minimele de pe 4H, departe de zona de supply.
- [1H] Sell (A): dacă prețul revine în supply-ul de pe 1H (partea scumpă), structura fractală de pe 1H se rupe în jos → intri la jumătatea mișcării de rupere (sau cu limit la marginea zonei). SL deasupra vârfului zonei. Ținte: minimele de pe 4H, demand-ul de pe 1H, minimul mare de dedesubt.
  Limit: Entry ~1.09933 · SL 1.10067 · TP 1.09573 / 1.09486 / 1.08812 (2.7R / 3.3R / 8.4R)
  Confirmare (exemplu): Entry ~1.09845 · SL 1.10009 · TP 1.09573 / 1.09486 / 1.08812 (1.7R / 2.2R / 6.3R)
- Ce anulează ideea: o închidere 1H deasupra zonei, sau atingerea primei ținte fără intrare — acum e foarte aproape (7 pips). Valabil până azi 22:00. Atenție: posibila revizuire S&P a Franței și ziua scurtă pe Wall Street.
- [4H] SKIP: zonele de pe Daily și 4H au fost testate de prea multe ori.

**Istorie insuficientă (1 rând):** GBPUSD, USDJPY, USDCHF, USDCAD, AUDUSD, NZDUSD, EURGBP, EURJPY, EURCHF, EURAUD, EURNZD, EURCAD, GBPJPY, GBPCHF, GBPAUD, GBPNZD, GBPCAD, AUDJPY, AUDCHF, AUDNZD, AUDCAD, NZDJPY, NZDCHF, NZDCAD, CADJPY, CADCHF, CHFJPY — nu se pot verifica zonele, fără setup-uri. **XAUUSD:** date lipsă.

## Tabel sumar
| Pereche | D / 4H / 1H swing | Fundamental | Conviction | Cel mai bun setup | Clasă |
|---|---|---|---|---|---|
| EURUSD | ↓ / ↓ / ↓ (1H internal + fractal ↑ = pullback) | bearish (medium) · check: ✅ CONFIRMED · could get even stronger | High | [1H] Short pro-trend din supply 1H proaspăt 1.09933–1.100585 · [4H] SKIP | A |
| GBPUSD | ↓ / ↑ / ↓ · istorie insuficientă (1 rând) | bearish (medium) · check: ⚠️ UNDER PRESSURE | — | NO TRADE (istorie insuficientă) | — |
| USDJPY | ↑ / ↓ / ↓ · istorie insuficientă (1 rând) | bullish (medium) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| USDCHF | ↑ / ↑ / ↑ · istorie insuficientă (1 rând) | bullish (low) · check: ✅ CONFIRMED | — | NO TRADE (istorie insuficientă) | — |
| USDCAD | ↓ / ↑ / ↓ · istorie insuficientă (1 rând) | bullish (medium) · check: ✅ CONFIRMED | — | NO TRADE (istorie insuficientă) | — |
| AUDUSD | ↑ / ↓ / ↑ · istorie insuficientă (1 rând) | bearish (medium) · check: ⚠️ UNDER PRESSURE | — | NO TRADE (istorie insuficientă) | — |
| NZDUSD | ↓ / ↓ / ↓ · istorie insuficientă (1 rând) | bearish (low) · check: ✅ CONFIRMED | — | NO TRADE (istorie insuficientă) | — |
| EURGBP | ↓ / ↓ / ↑ · istorie insuficientă (1 rând) | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| EURJPY | ↓ / ↓ / ↓ · istorie insuficientă (1 rând) | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| EURCHF | ↓ / ↓ / ↓ · istorie insuficientă (1 rând) | two-sided (low) · check: ⚪ STILL TWO-SIDED | — | NO TRADE (istorie insuficientă) | — |
| EURAUD | ↓ / ↑ / ↓ · istorie insuficientă (1 rând) | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| EURNZD | ↑ / ↓ / ↑ · istorie insuficientă (1 rând) | two-sided (low) · check: ❌ INVALIDATED | — | NO TRADE (istorie insuficientă) | — |
| EURCAD | ↑ / ↓ / ↓ · istorie insuficientă (1 rând) | bullish (medium) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| GBPJPY | ↓ / ↓ / ↓ · istorie insuficientă (1 rând) | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| GBPCHF | ↓ / ↓ / ↓ · istorie insuficientă (1 rând) | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| GBPAUD | ↑ / ↑ / ↑ · istorie insuficientă (1 rând) | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| GBPNZD | ↓ / ↑ / ↓ · istorie insuficientă (1 rând) | two-sided (low) · check: ❌ INVALIDATED | — | NO TRADE (istorie insuficientă) | — |
| GBPCAD | ↑ / ↑ / ↓ · istorie insuficientă (1 rând) | bullish (medium) · check: ✅ CONFIRMED · could get even stronger | — | NO TRADE (istorie insuficientă) | — |
| AUDJPY | ↑ / ↓ / ↑ · istorie insuficientă (1 rând) | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| AUDCHF | ↓ / ↓ / ↓ · istorie insuficientă (1 rând) | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| AUDNZD | ↑ / ↓ / ↓ · istorie insuficientă (1 rând) | two-sided (low) · check: ❌ INVALIDATED | — | NO TRADE (istorie insuficientă) | — |
| AUDCAD | ↓ / ↓ / ↓ · istorie insuficientă (1 rând) | bullish (medium) · check: ✅ CONFIRMED · could get even stronger | — | NO TRADE (istorie insuficientă) | — |
| NZDJPY | ↑ / ↓ / ↓ · istorie insuficientă (1 rând) | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| NZDCHF | ↓ / ↓ / ↓ · istorie insuficientă (1 rând) | two-sided (low) · check: ❌ INVALIDATED | — | NO TRADE (istorie insuficientă) | — |
| NZDCAD | ↑ / ↓ / ↓ · istorie insuficientă (1 rând) | bullish (low) · check: ⚠️ UNDER PRESSURE | — | NO TRADE (istorie insuficientă) | — |
| CADJPY | ↓ / ↑ / ↑ · istorie insuficientă (1 rând) | bearish (medium) · check: ✅ CONFIRMED · could get even stronger | — | NO TRADE (istorie insuficientă) | — |
| CADCHF | ↑ / ↑ / ↑ · istorie insuficientă (1 rând) | bearish (low) · check: ✅ CONFIRMED | — | NO TRADE (istorie insuficientă) | — |
| CHFJPY | ↑ / ↓ / ↑ · istorie insuficientă (1 rând) | two-sided (low) · check: ⚪ STILL TWO-SIDED | — | NO TRADE (istorie insuficientă) | — |
| XAUUSD | date lipsă (fără CSV) | two-sided (low) · check: ⚪ STILL TWO-SIDED | — | NO TRADE (date lipsă) | — |
## Tehnic
### EURUSD — Bias: bearish · Conviction: High (neschimbat)
Swing D și 4H bearish, fundamental bearish medium (EUR 0 vs USD +7, check ✅ CONFIRMED · could get even stronger).

**Structura acum** (rândul 27 nov 10:00, close 1.09643; ATR(14) 1H = 0.00086286; ATR(14) 4H = 0.0020104):
- D: swing ↓ CHoCH 1.17116, BOS gol · internal ↓ CHoCH 1.127315, BOS gol · fractal ↓ CHoCH 1.101015, BOS 1.088115, pos 64.5%
- 4H: swing ↓ CHoCH 1.127315, BOS gol · internal ↓ CHoCH 1.100585, BOS 1.09573, pos 14.4% · fractal ↓ CHoCH 1.100585, BOS 1.088115, pos 66.7%
- 1H: swing ↓ CHoCH 1.101015, BOS 1.088115, pos 64.5% · internal ↑ CHoCH 1.09313, BOS 1.09893, pos 56.9% · fractal ↑ CHoCH 1.093405, BOS 1.0993, pos 51.3% (pullback contra swing)
- Zone: D supply rafinată 1.09664–1.101015, testată 4x · 4H supply rafinată 1.097345–1.100585, testată 5x · 1H supply 23 nov 14:00 rafinată 1.09933–1.100585 proaspătă · 1H demand 25 nov 19:00 rafinată 1.093405–1.09486 proaspătă.

**Știri 24h:** S&P review Franța (HIGH, dată neconfirmată), half-day Wall Street (închidere 20:00 București). Nicio știre CRITICAL.

**Ce urmăresc:** 1.100585 (4H internal/fractal CHoCH + distal supply 1H), 1.101015 (D fractal / 1H swing CHoCH), 1.09573 (4H internal BOS = TP1, la 7 pips), 1.093405 (1H fractal CHoCH). Părerea se schimbă la o închidere 1H peste 1.101015.

#### [1H] Setup 1 — pro-trend · SHORT · A — EURUSD-20261127-0945-1 (waiting, acceptat)
- Piloni: swing D ↓, swing 4H ↓, zonă 1H proaspătă în premium, fundamental bearish → 4/5; lipsește structura de intrare (1H internal/fractal încă ↑).
- Prag: A ✓ · zonă proaspătă ✓ · premium pe 1H swing (zona e peste 50% din range) ✓ · R:R confirmare 1.66R la TP1 ✓ · fără CRITICAL ✓.
- Invalidare: închidere 1H peste 1.100585; anulat dacă TP1 1.09573 e atins fără intrare.
- **Varianta 1 — limit:** entry 1.09933 · SL 1.100671 (1.100585 + 0.0000863) · 13.4 pips · TP1 1.09573 2.68R · TP2 1.09486 3.33R · TP3 1.088115 8.36R
- **Varianta 2 — confirmare:** declanșatorul se stabilește la atingerea zonei: închidere 1H **sub** ultimul low protejat (CHoCH internal/fractal 1H) în vigoare atunci. Entry = 50% din piciorul maxim-în-zonă → minimul lumânării de break; SL = maximul + 0.0000863.
  - Exemplu: maxim 1.10000, minim break 1.09690 → entry 1.09845, SL 1.100086 (16.4 pips) · TP1 1.66R · TP2 2.19R · TP3 6.32R.
- Valabil până vineri 27 nov, 22:00. Riscuri: prețul se îndepărtează de zonă și e lângă TP1; SL sub lichiditatea 1.101015; zone HTF testate repetat; S&P Franța; lichiditate redusă în SUA.

#### [4H] — SKIP
Zonele D (testată 4x) și 4H (testată 5x) nu mai sunt proaspete; nimic calitativ pe 4H.

### Restul perechilor
27 de perechi: istorie insuficientă (1 rând, 27 nov 10:00) — zonele nu se pot verifica, fără setup-uri. XAUUSD: date lipsă (fără CSV). Biasul fundamental din tabel e doar referință.

_Analiză condiționată, nu semnal de tranzacționare. Mărimea poziției nu e dată._
