# Analiza MTF — vineri 27 nov 2026, 20:11 București (sesiunea de seară)

**Date:** cel mai vechi și cel mai nou „ultimul rând” = 27 nov 19:00 (lumânarea 19:00–20:00, închisă; sub pragul de 2h) pentru toate cele 28 de perechi cu CSV. XAUUSD: fără CSV. Export `fsb-export` pornit la 20:11 (run 46047587950), terminat cu succes; `meta.json` 18:11:46 UTC. · **Fundamental:** `imports/2026-W48-final.json` · **Check:** `imports/check-2026-11-27-morning.json` (check-ul de seară din 27 nov nu apare încă în `imports/index.json`).

Presupuneri notate (rulare nesupravegheată):
- **Date inconsistente (neschimbat):** GBPUSD, USDJPY, USDCHF, USDCAD, AUDUSD, NZDUSD au în continuare `seed_vs_live.diff = 1` → fără setup-uri noi; structura doar orientativ. Cele 21 de cross-uri au 10 rânduri (istorie insuficientă).
- **Vineri seara:** `valid_until` maxim e azi 22:00, iar piața se închide la miezul nopții. Un setup nou ar avea sub 2 ore de valabilitate pe lichiditate de vineri seara; nu propun nimic doar ca să existe ceva. Zonele proaspete rămân de reevaluat luni dimineață.
- Nicio știre CRITICAL în următoarele 24h. HIGH: S&P review Franța (dată neconfirmată, posibil vineri seara după închidere); duminică OPEC+ (MEDIUM); luni 30 nov Canada GDP Q3 și discursul Ueda; marți 1 dec HICP flash zona euro.

## Overview
🎯 **Setup-uri bune acum**
- —

📍 **Aproape**
- NZDUSD _(date inconsistente)_ — 7.9 pips peste 0.54559 (CHoCH fractal 4H, ATR 4H 17.2 pips). O închidere 4H sub = fractalul 4H se întoarce bearish, în direcția fundamentalului.
- AUDUSD _(date inconsistente)_ — 17.9 pips sub 0.66649 (CHoCH fractal D) și 19.9 pips peste 0.66271 (CHoCH fractal 4H; ATR 4H 20.4 pips). Închidere 4H sub 0.66271 = fractalul 4H bearish (cu fundamentalul); închidere zilnică peste 0.66649 = fractalul D bullish (contra).

👀 **De interes**
- EURUSD — 4H a confirmat continuarea bearish (lumânarea 4H 12–16 a închis la 1.094965, sub BOS-ul internal 4H 1.09573), iar fractalul 1H s-a întors din nou **bearish** la 19:00, lăsând un supply 1H proaspăt 1.094965–1.09553. De reevaluat luni: pullback în el = short pro-trend, dacă prețul ajunge în premium.
- USDCHF _(date inconsistente)_ — fractalul 4H s-a întors **bullish** la lumânarea 4H 12–16 (cu fundamentalul bullish); demand 4H proaspăt 0.833255–0.834085.
- Watchlist: planul tău EURUSD (din propunerea MTF) e încă „active” în Watchlist, dar e **invalidat** de la 11:00 (TP1 atins fără intrare).

## Schimbări de la ultima rulare
- Niciun setup activ; nicio schimbare de stare în `state.json`.
- EURUSD: BOS internal 4H 1.09573 spart cu închidere 4H (12–16, 1.094965); minim 1.09336 la 19:00, sub vârful demand-ului 1H 1.093405 (închidere 1.093715 deasupra → demand-ul nu e invalidat, testat 1x); fractal 1H ↑ → ↓ la 19:00.
- USDCHF: fractal 4H ↓ → ↑ (16:00). AUDUSD: fractal 1H ↑ → ↓ (15:00). USDCAD: fractal 1H ↑ → ↓ (18:00). (toate trei cu date inconsistente)

## Pe scurt
**EURUSD** — Daily, 4H și fundamentalul sunt bearish, iar după-amiază prețul a coborât din nou și a confirmat continuarea pe 4H. Structura rapidă de pe 1H s-a întors și ea în jos și a lăsat o zonă de supply nouă, chiar deasupra prețului. Problema: prețul e acum în partea „ieftină” a range-ului, iar până la închiderea săptămânii mai sunt doar câteva ore, așa că un sell aici ar fi o intrare târzie. SKIP azi; luni, dacă prețul urcă înapoi în supply-ul nou de pe 1H și se rupe în jos, ideea de sell redevine interesantă.

**Date inconsistente:** GBPUSD, USDJPY, USDCHF, USDCAD, AUDUSD, NZDUSD — istoria manuală și alertele live nu coincid pe aceeași lumânare; fără setup-uri până se rezolvă.

**Istorie insuficientă (10 rânduri):** EURGBP, EURJPY, EURCHF, EURAUD, EURNZD, EURCAD, GBPJPY, GBPCHF, GBPAUD, GBPNZD, GBPCAD, AUDJPY, AUDCHF, AUDNZD, AUDCAD, NZDJPY, NZDCHF, NZDCAD, CADJPY, CADCHF, CHFJPY — fără setup-uri. **XAUUSD:** date lipsă.

## Tabel sumar
| Pereche | D / 4H / 1H swing | Fundamental | Conviction | Cel mai bun setup | Clasă |
|---|---|---|---|---|---|
| EURUSD | ↓ / ↓ / ↓ (1H fractal ↓ din nou la 19:00; internal ↑) | bearish (medium) · check: ✅ CONFIRMED · could get even stronger | High | SKIP — preț în discount sub supply-ul 1H nou, fereastră până vineri 22:00 | — |
| GBPUSD | ↓ / ↑ / ↓ · date inconsistente (seed ≠ live) | bearish (medium) · check: ⚠️ UNDER PRESSURE | — | NO TRADE (date inconsistente) | — |
| USDJPY | ↑ / ↓ / ↓ · date inconsistente (seed ≠ live) | bullish (medium) · check: 👀 UNDER WATCH | — | NO TRADE (date inconsistente) | — |
| USDCHF | ↑ / ↑ / ↑ · date inconsistente (seed ≠ live) | bullish (low) · check: ✅ CONFIRMED | — | NO TRADE (date inconsistente) | — |
| USDCAD | ↓ / ↑ / ↓ · date inconsistente (seed ≠ live) | bullish (medium) · check: ✅ CONFIRMED | — | NO TRADE (date inconsistente) | — |
| AUDUSD | ↑ / ↓ / ↑ · date inconsistente (seed ≠ live) | bearish (medium) · check: ⚠️ UNDER PRESSURE | — | NO TRADE (date inconsistente) | — |
| NZDUSD | ↓ / ↓ / ↓ · date inconsistente (seed ≠ live) | bearish (low) · check: ✅ CONFIRMED | — | NO TRADE (date inconsistente) | — |
| EURGBP | ↓ / ↓ / ↑ · istorie insuficientă (10 rânduri) | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| EURJPY | ↓ / ↓ / ↓ · istorie insuficientă (10 rânduri) | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| EURCHF | ↓ / ↓ / ↓ · istorie insuficientă (10 rânduri) | two-sided (low) · check: ⚪ STILL TWO-SIDED | — | NO TRADE (istorie insuficientă) | — |
| EURAUD | ↓ / ↑ / ↓ · istorie insuficientă (10 rânduri) | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| EURNZD | ↑ / ↓ / ↑ · istorie insuficientă (10 rânduri) | two-sided (low) · check: ❌ INVALIDATED | — | NO TRADE (istorie insuficientă) | — |
| EURCAD | ↑ / ↓ / ↓ · istorie insuficientă (10 rânduri) | bullish (medium) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| GBPJPY | ↓ / ↓ / ↓ · istorie insuficientă (10 rânduri) | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| GBPCHF | ↓ / ↓ / ↓ · istorie insuficientă (10 rânduri) | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| GBPAUD | ↑ / ↑ / ↑ · istorie insuficientă (10 rânduri) | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| GBPNZD | ↓ / ↑ / ↓ · istorie insuficientă (10 rânduri) | two-sided (low) · check: ❌ INVALIDATED | — | NO TRADE (istorie insuficientă) | — |
| GBPCAD | ↑ / ↑ / ↓ · istorie insuficientă (10 rânduri) | bullish (medium) · check: ✅ CONFIRMED · could get even stronger | — | NO TRADE (istorie insuficientă) | — |
| AUDJPY | ↑ / ↓ / ↑ · istorie insuficientă (10 rânduri) | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| AUDCHF | ↓ / ↓ / ↓ · istorie insuficientă (10 rânduri) | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| AUDNZD | ↑ / ↓ / ↓ · istorie insuficientă (10 rânduri) | two-sided (low) · check: ❌ INVALIDATED | — | NO TRADE (istorie insuficientă) | — |
| AUDCAD | ↓ / ↓ / ↓ · istorie insuficientă (10 rânduri) | bullish (medium) · check: ✅ CONFIRMED · could get even stronger | — | NO TRADE (istorie insuficientă) | — |
| NZDJPY | ↑ / ↓ / ↓ · istorie insuficientă (10 rânduri) | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| NZDCHF | ↓ / ↓ / ↓ · istorie insuficientă (10 rânduri) | two-sided (low) · check: ❌ INVALIDATED | — | NO TRADE (istorie insuficientă) | — |
| NZDCAD | ↑ / ↓ / ↓ · istorie insuficientă (10 rânduri) | bullish (low) · check: ⚠️ UNDER PRESSURE | — | NO TRADE (istorie insuficientă) | — |
| CADJPY | ↓ / ↑ / ↑ · istorie insuficientă (10 rânduri) | bearish (medium) · check: ✅ CONFIRMED · could get even stronger | — | NO TRADE (istorie insuficientă) | — |
| CADCHF | ↑ / ↑ / ↑ · istorie insuficientă (10 rânduri) | bearish (low) · check: ✅ CONFIRMED | — | NO TRADE (istorie insuficientă) | — |
| CHFJPY | ↑ / ↓ / ↑ · istorie insuficientă (10 rânduri) | two-sided (low) · check: ⚪ STILL TWO-SIDED | — | NO TRADE (istorie insuficientă) | — |
| XAUUSD | date lipsă (fără CSV) | two-sided (low) · check: ⚪ STILL TWO-SIDED | — | NO TRADE (date lipsă) | — |

## Tehnic
### EURUSD — Bias: bearish · Conviction: High (neschimbat)
Swing D și 4H bearish, fundamental bearish medium (EUR 0 vs USD +7, check dimineață ✅ CONFIRMED · could get even stronger).

**Structura acum** (rândul 27 nov 19:00, close 1.093715; ATR(14) 1H = 0.0011521; ATR(14) 4H = 0.0021089):
- D: swing ↓ CHoCH 1.17116, BOS gol · internal ↓ CHoCH 1.127315, BOS gol · fractal ↓ CHoCH 1.101015, BOS 1.088115, pos 43.4%
- 4H: swing ↓ CHoCH 1.127315, BOS gol · internal ↓ CHoCH 1.09893, BOS gol (după spargerea 1.09573) · fractal ↓ CHoCH 1.100585, BOS 1.088115, pos 44.9%
- 1H: swing ↓ CHoCH 1.101015, BOS 1.088115, pos 43.4% · internal ↑ CHoCH 1.09313, BOS 1.09867, pos 10.6% · fractal ↓ CHoCH 1.09553, BOS gol (întors la 19:00)
- Zone: D supply rafinată 1.09664–1.101015, testată 5x · 4H supply rafinată 1.097345–1.100585, testată 5x · 1H supply 27 nov 19:00 rafinată 1.094965–1.09553, proaspătă · 1H demand 25 nov 19:00 rafinată 1.093405–1.09486, testată 1x · 1H demand 24 nov 13:00 rafinată 1.089635–1.09085, proaspătă.

**Ce urmăresc:** 1.09553 (CHoCH fractal 1H = distalul supply-ului 1H nou), 1.09313 (CHoCH internal 1H: o închidere 1H sub = 1H complet bearish), 1.09085 / 1.089635 (demand 1H proaspăt), 1.088115 (BOS fractal D/4H). Părerea bearish se schimbă la o închidere 1H peste 1.101015.

- **[1H] SKIP** — short din supply-ul 1H 1.094965–1.09553 (proaspăt, pro-trend, pro-fundamental): pragul 4b.3 nu e îndeplinit — prețul e în discount pe range-ul 4H (pos 44.9%) și pe swing-ul 1H (43.4%). Calcul orientativ (nepropus): limit 1.094965, SL 1.095645 (buffer 0.1 × ATR 1H = 1.15 pips; risc 6.8 pips), TP 1.09085 = 6.0R. În plus, valabilitatea ar fi sub 2 ore (vineri 22:00). Long din demand-ul 1H: contra swing-ului D/4H și contra fundamentalului → nu se propune.
- **[4H] SKIP** — zonele D și 4H testate de 5 ori; prețul în discount.

### Perechile cu date inconsistente (orientativ, fără setup-uri)
- **GBPUSD** — D ↓, 4H swing ↑ (internal/fractal ↓), 1H swing ↓ / internal ↑ / fractal ↓. Preț 1.30994 sub supply-ul 4H 1.31138–1.314395 (testat 1x). Diferență seed/live: 4H zone refined low.
- **USDJPY** — D swing ↑ (diferență seed/live pe D swing), 4H swing ↓ cu fractal ↑, 1H internal/fractal ↑. Preț 159.522, deasupra demand-ului 4H proaspăt 159.142–159.3455.
- **USDCHF** — D ↑, 4H swing ↑ (fractal ↑ de la 16:00, internal ↓), 1H ↑. Preț 0.8362; demand 4H proaspăt 0.833255–0.834085.
- **USDCAD** — D swing ↓ (diferență seed/live), 4H swing ↑ (internal/fractal ↓), 1H ↓. Preț 1.42458; supply 4H proaspăt 1.427955–1.429435.
- **AUDUSD** — D swing ↑ (diferență seed/live) cu internal/fractal ↓, 4H swing ↓ cu internal/fractal ↑, 1H fractal ↓ de la 15:00. Preț 0.6647, între 0.66271 și 0.66649.
- **NZDUSD** — D ↓, 4H swing ↓ (fractal ↑), 1H swing ↓ (internal/fractal ↑). Preț 0.546385, la 7.9 pips de CHoCH-ul fractal 4H 0.54559.

### Restul perechilor
21 de cross-uri: istorie insuficientă (10 rânduri, 27 nov 10:00–19:00) — fără setup-uri. XAUUSD: date lipsă (fără CSV). Biasul fundamental din tabel e doar referință.

_Analiză condiționată, nu semnal de tranzacționare. Mărimea poziției nu e dată._
