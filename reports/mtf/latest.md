# Analiza MTF — vineri 27 nov 2026, 10:13 București (sesiunea de dimineață, înainte de Londra)

**Date:** cel mai vechi și cel mai nou „ultimul rând” = EURUSD 27 nov 09:00 (lumânarea 09:00–10:00, închisă; 1h13 la rulare, sub pragul de 2h). Celelalte 28 de perechi: fără CSV. Exportul `fsb-export` pornit la 10:13 (run 45964039180) s-a terminat cu succes; `meta.json` (08:13:49 UTC): EURUSD 301 rânduri (300 seed + 1 live), nicio lumânare nouă față de rularea de 10:02. · **Fundamental:** `imports/2026-W48-final.json` · **Check:** `imports/check-2026-11-27-morning.json` (cel mai nou din `index.json`).

Presupuneri notate (rulare nesupravegheată):
- `ANALYST.md` a fost actualizat la v1.2 după rularea de 10:02 (setup-uri [4H] și [1H], prag de calitate, SKIP). Rularea aceasta reaplică aceleași date cu regulile v1.2; nu există date noi.
- Setup-ul existent primește eticheta `[1H]` (zonă 1H, declanșator pe închidere 1H, ținte 4H/1H) și câmpul `tf` în `state.json`.
- Setup-ul 2 (long counter-trend C din demand 1H) nu mai apare: v1.2 nu raportează clasa C și permite counter-trend doar din zone HTF (D/4H) proaspete.

## Schimbări de la ultima rulare
- Nicio lumânare nouă (ultimul rând tot 09:00). EURUSD-20261127-0945-1 rămâne **waiting**; etichetat `[1H]`, trece pragul de calitate v1.2.
- Long-ul counter-trend C din demand 1H retras (sub pragul v1.2). Watchlist: gol.

## Tabel sumar
| Pereche | D / 4H / 1H swing | Fundamental | Conviction | Cel mai bun setup | Clasă |
|---|---|---|---|---|---|
| EURUSD | ↓ / ↓ / ↓ (1H internal + fractal ↑ = pullback) | bearish (medium) · check: ✅ CONFIRMED | High | [1H] Short pro-trend din supply 1H proaspăt 1.09933–1.100585 · [4H] SKIP | A |
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

**Structura acum** (rândul 27 nov 09:00, close 1.09764; ATR(14) 1H = 0.00076536; ATR(14) 4H = 0.0019493):
- D: swing ↓ CHoCH 1.17116, BOS gol · internal ↓ CHoCH 1.127315, BOS gol · fractal ↓ CHoCH 1.101015, BOS 1.088115, pos 73.8%
- 4H: swing ↓ CHoCH 1.127315, BOS gol · internal ↓ CHoCH 1.100585, BOS 1.09573, pos 39.3% · fractal ↓ CHoCH 1.100585, BOS 1.088115, pos 76.4%
- 1H: swing ↓ CHoCH 1.101015, BOS 1.088115, pos 73.8% · internal ↑ CHoCH 1.09313, BOS 1.09893, pos 77.8% · fractal ↑ CHoCH 1.093405, BOS 1.0993, pos 71.8% (internal/fractal ↑ contra swing = pullback)
- Zone: D supply rafinată 1.09664–1.101015, testată 4x · 4H supply rafinată 1.097345–1.100585, testată 5x (prețul în ea) · 1H supply 23 nov 14:00 rafinată 1.09933–1.100585 proaspătă · 1H demand 25 nov 19:00 rafinată 1.093405–1.09486 proaspătă.

**Știri 24h:** S&P review Franța (HIGH, dată neconfirmată, probabil după închidere), half-day Wall Street (închidere 20:00). Nicio știre CRITICAL.

**Ce urmăresc:** 1.100585 (4H internal/fractal CHoCH + distal supply 1H), 1.101015 (D fractal / 1H swing CHoCH), 1.09573 (4H internal BOS), 1.093405 (1H fractal CHoCH). Părerea se schimbă la o închidere 1H peste 1.101015 (1H swing întors).

### [1H] Setup 1 — pro-trend · SHORT · A — EURUSD-20261127-0945-1 (neschimbat, re-etichetat)
- Piloni: swing D ↓, swing 4H ↓, zonă 1H proaspătă în premium (1H swing pos > 73.8%), fundamental bearish → 4/5; lipsește structura de intrare (1H internal/fractal încă ↑).
- Prag v1.2: clasă A ✓ · zonă proaspătă ✓ · premium pe 1H swing ✓ · R:R confirmare 1.67R la TP1 (≥1.5) ✓ · fără CRITICAL ✓.
- Valid dacă: prețul atinge 1.09933–1.100585, apoi închidere 1H sub CHoCH-ul fractal 1H raportat de indicator. Invalidare: închidere 1H peste 1.100585; anulat dacă TP1 1.09573 e atins fără intrare.
- **Varianta 1 — limit:** entry 1.09933 · SL 1.100662 (1.100585 + 0.0000765 buffer) · 13.3 pips
  - TP1 1.09573 (BOS 4H internal) 2.70R · TP2 1.09486 (proximal demand 1H) 3.36R · TP3 1.088115 (BOS 1H swing / D fractal) 8.42R
- **Varianta 2 — confirmare:** declanșator = închidere 1H sub CHoCH-ul fractal 1H raportat de indicator după atingerea zonei (acum 1.093405; urcă după un nou maxim fractal în zonă).
  - Formula: entry = 50% din piciorul dintre maximul atins în zonă și minimul lumânării de break; SL = maximul atins + 0.0000765.
  - Exemplu: maxim 1.10000, minim lumânare de break 1.09690 → entry 1.09845, SL 1.100077 (16.3 pips). TP1 1.67R · TP2 2.21R · TP3 6.35R.
- Valabil până vineri 27 nov, 22:00. Riscuri: SL sub lichiditatea 1.101015; 4H swing în discount; zone HTF testate repetat; S&P Franța → gap în weekend; lichiditate redusă SUA.

### [4H] — SKIP
Zonele D (testată 4x) și 4H (testată 5x) nu mai sunt proaspete/testate o singură dată; 4H swing BOS gol, pos indisponibil. Nimic calitativ pe 4H.

### Long counter-trend — nu se propune
Demand-ul disponibil e doar 1H (nu HTF), iar setup-ul ar fi C și contra fundamentalului.

## Restul perechilor
GBPUSD, USDJPY, USDCHF, USDCAD, AUDUSD, NZDUSD, EURGBP, EURJPY, EURCHF, EURAUD, EURNZD, EURCAD, GBPJPY, GBPCHF, GBPAUD, GBPNZD, GBPCAD, AUDJPY, AUDCHF, AUDNZD, AUDCAD, NZDJPY, NZDCHF, NZDCAD, CADJPY, CADCHF, CHFJPY, XAUUSD: **date lipsă** (fără CSV în `data/fsb/`), deci fără setup-uri. Biasul fundamental e în tabel doar ca referință.

_Analiză condiționată, nu semnal de tranzacționare. Mărimea poziției nu e dată._
