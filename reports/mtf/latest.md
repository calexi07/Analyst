# Analiza MTF — vineri 27 nov 2026, 14:06 București (sesiunea de prânz, înainte de New York)

**Date:** cel mai vechi și cel mai nou „ultimul rând” = 27 nov 13:00 (lumânarea 13:00–14:00, închisă; sub pragul de 2h) pentru toate cele 28 de perechi cu CSV. XAUUSD: fără CSV. Export `fsb-export` pornit la 14:06 (run 45995866982), terminat cu succes; `meta.json` 12:06:35 UTC. · **Fundamental:** `imports/2026-W48-final.json` · **Check:** `imports/check-2026-11-27-morning.json` (06:00 București).

Presupuneri notate (rulare nesupravegheată):
- **Date inconsistente (nou):** exportul de acum verifică istoria seed vs alertele live. La GBPUSD, USDJPY, USDCHF, USDCAD, AUDUSD și NZDUSD `seed_vs_live.diff = 1` (coloane diferite pe aceeași lumânare: de ex. swing D la USDJPY/USDCAD/AUDUSD, zone rafinate). Conform RUN.md, aceste 6 perechi nu primesc setup-uri noi până se rezolvă; structura e descrisă doar orientativ. EURUSD nu are diferențe (`seed_vs_live: null`).
- **EURUSD:** setup-ul acceptat a fost anulat de propria regulă (TP1 atins fără intrare). Nu îl repropun în aceeași zonă în aceeași zi: ar însemna să ignor regula de anulare. Supply-ul 1H 1.09933–1.100585 rămâne proaspăt și poate fi reluat săptămâna viitoare, cu date noi.
- Nicio știre CRITICAL în următoarele 24h. HIGH: S&P review Franța (dată neconfirmată); luni 30 nov Canada GDP Q3 și discursul Ueda; duminică OPEC+ (MEDIUM). Azi: date comerciale SUA și cont curent Canada 15:30, Wall Street închide la 20:00 București.

## Overview
🎯 **Setup-uri bune acum**
- —

📍 **Aproape**
- EURUSD — la 9.8 pips peste 1.09573 (BOS internal 4H; ATR 4H 19.4 pips). Fitilul de la 11:00–12:00 a coborât sub el (1.09552), dar lumânarea 4H 08–12 a închis deasupra. O închidere 4H sub = continuare bearish confirmată pe 4H.
- GBPUSD _(date inconsistente)_ — la 14.0 pips sub 1.314395 (CHoCH fractal 4H, vârful supply-ului 4H). O închidere 4H peste = fractalul 4H se întoarce în sus, contra biasului bearish.
- AUDUSD _(date inconsistente)_ — 4.4 pips peste 0.66649 (CHoCH fractal D, pos 104%). O închidere zilnică peste = fractalul D bullish, contra biasului bearish.
- USDJPY _(date inconsistente)_ — 24.9 pips peste 159.142 (noul CHoCH fractal 4H). O închidere 4H sub = fractalul 4H din nou bearish.

👀 **De interes**
- USDJPY — fractalul 4H s-a întors **bullish** la lumânarea 4H 08–12 (în direcția fundamentalului bullish); a lăsat un demand 4H proaspăt 159.142–159.3455. Fără setup (date inconsistente).
- Watchlist: planul tău EURUSD (din propunerea MTF) — **invalidat** la 11:00: prima țintă atinsă fără ca prețul să ajungă în zonă.

## Schimbări de la ultima rulare
- **EURUSD-20261127-0945-1 → invalidated** (lumânarea 11:00): minimul 1.095585 a atins TP1 1.09573 fără intrare (maximul de după 10:00 = 1.096745, sub proximalul 1.09933). Decizie: acceptat. Mutat în `closed.jsonl`.
- Date: 6 perechi USD marcate „date inconsistente” (verificare nouă seed vs live) → fără setup-uri noi.
- USDJPY: fractal 4H ↓ → ↑ la 12:00.

## Pe scurt
**EURUSD** — Daily și 4H rămân bearish, ca și fundamentalul. Prețul a coborât azi aproape de minimele de pe 4H fără să mai urce în zona de supply, așa că ideea de sell din supply s-a anulat singură (prima țintă atinsă fără intrare). Acum prețul e la mijloc, sub o zonă de supply uzată pe Daily/4H și deasupra demand-ului de pe 1H: nimic de luat azi. Zona de supply proaspătă de pe 1H rămâne de urmărit săptămâna viitoare.

**Date inconsistente:** GBPUSD, USDJPY, USDCHF, USDCAD, AUDUSD, NZDUSD — istoria manuală și alertele live nu coincid pe aceeași lumânare; fără setup-uri până se rezolvă.

**Istorie insuficientă (4 rânduri):** EURGBP, EURJPY, EURCHF, EURAUD, EURNZD, EURCAD, GBPJPY, GBPCHF, GBPAUD, GBPNZD, GBPCAD, AUDJPY, AUDCHF, AUDNZD, AUDCAD, NZDJPY, NZDCHF, NZDCAD, CADJPY, CADCHF, CHFJPY — fără setup-uri. **XAUUSD:** date lipsă.

## Tabel sumar
| Pereche | D / 4H / 1H swing | Fundamental | Conviction | Cel mai bun setup | Clasă |
|---|---|---|---|---|---|
| EURUSD | ↓ / ↓ / ↓ (1H internal + fractal ↑ = pullback) | bearish (medium) · check: ✅ CONFIRMED · could get even stronger | High | SKIP — setup-ul anterior anulat (TP1 fără intrare); D/4H zone testate 5x | — |
| GBPUSD | ↓ / ↑ / ↓ · date inconsistente (seed ≠ live) | bearish (medium) · check: ⚠️ UNDER PRESSURE | — | NO TRADE (date inconsistente) | — |
| USDJPY | ↑ / ↓ / ↓ · date inconsistente (seed ≠ live) | bullish (medium) · check: 👀 UNDER WATCH | — | NO TRADE (date inconsistente) | — |
| USDCHF | ↑ / ↑ / ↑ · date inconsistente (seed ≠ live) | bullish (low) · check: ✅ CONFIRMED | — | NO TRADE (date inconsistente) | — |
| USDCAD | ↓ / ↑ / ↓ · date inconsistente (seed ≠ live) | bullish (medium) · check: ✅ CONFIRMED | — | NO TRADE (date inconsistente) | — |
| AUDUSD | ↑ / ↓ / ↑ · date inconsistente (seed ≠ live) | bearish (medium) · check: ⚠️ UNDER PRESSURE | — | NO TRADE (date inconsistente) | — |
| NZDUSD | ↓ / ↓ / ↓ · date inconsistente (seed ≠ live) | bearish (low) · check: ✅ CONFIRMED | — | NO TRADE (date inconsistente) | — |
| EURGBP | ↓ / ↓ / ↑ · istorie insuficientă (4 rânduri) | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| EURJPY | ↓ / ↓ / ↓ · istorie insuficientă (4 rânduri) | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| EURCHF | ↓ / ↓ / ↓ · istorie insuficientă (4 rânduri) | two-sided (low) · check: ⚪ STILL TWO-SIDED | — | NO TRADE (istorie insuficientă) | — |
| EURAUD | ↓ / ↑ / ↓ · istorie insuficientă (4 rânduri) | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| EURNZD | ↑ / ↓ / ↑ · istorie insuficientă (4 rânduri) | two-sided (low) · check: ❌ INVALIDATED | — | NO TRADE (istorie insuficientă) | — |
| EURCAD | ↑ / ↓ / ↓ · istorie insuficientă (4 rânduri) | bullish (medium) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| GBPJPY | ↓ / ↓ / ↓ · istorie insuficientă (4 rânduri) | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| GBPCHF | ↓ / ↓ / ↓ · istorie insuficientă (4 rânduri) | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| GBPAUD | ↑ / ↑ / ↑ · istorie insuficientă (4 rânduri) | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| GBPNZD | ↓ / ↑ / ↓ · istorie insuficientă (4 rânduri) | two-sided (low) · check: ❌ INVALIDATED | — | NO TRADE (istorie insuficientă) | — |
| GBPCAD | ↑ / ↑ / ↓ · istorie insuficientă (4 rânduri) | bullish (medium) · check: ✅ CONFIRMED · could get even stronger | — | NO TRADE (istorie insuficientă) | — |
| AUDJPY | ↑ / ↓ / ↑ · istorie insuficientă (4 rânduri) | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| AUDCHF | ↓ / ↓ / ↓ · istorie insuficientă (4 rânduri) | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| AUDNZD | ↑ / ↓ / ↓ · istorie insuficientă (4 rânduri) | two-sided (low) · check: ❌ INVALIDATED | — | NO TRADE (istorie insuficientă) | — |
| AUDCAD | ↓ / ↓ / ↓ · istorie insuficientă (4 rânduri) | bullish (medium) · check: ✅ CONFIRMED · could get even stronger | — | NO TRADE (istorie insuficientă) | — |
| NZDJPY | ↑ / ↓ / ↓ · istorie insuficientă (4 rânduri) | two-sided (low) · check: 👀 UNDER WATCH | — | NO TRADE (istorie insuficientă) | — |
| NZDCHF | ↓ / ↓ / ↓ · istorie insuficientă (4 rânduri) | two-sided (low) · check: ❌ INVALIDATED | — | NO TRADE (istorie insuficientă) | — |
| NZDCAD | ↑ / ↓ / ↓ · istorie insuficientă (4 rânduri) | bullish (low) · check: ⚠️ UNDER PRESSURE | — | NO TRADE (istorie insuficientă) | — |
| CADJPY | ↓ / ↑ / ↑ · istorie insuficientă (4 rânduri) | bearish (medium) · check: ✅ CONFIRMED · could get even stronger | — | NO TRADE (istorie insuficientă) | — |
| CADCHF | ↑ / ↑ / ↑ · istorie insuficientă (4 rânduri) | bearish (low) · check: ✅ CONFIRMED | — | NO TRADE (istorie insuficientă) | — |
| CHFJPY | ↑ / ↓ / ↑ · istorie insuficientă (4 rânduri) | two-sided (low) · check: ⚪ STILL TWO-SIDED | — | NO TRADE (istorie insuficientă) | — |
| XAUUSD | date lipsă (fără CSV) | two-sided (low) · check: ⚪ STILL TWO-SIDED | — | NO TRADE (date lipsă) | — |

## Tehnic
### EURUSD — Bias: bearish · Conviction: High (neschimbat)
Swing D și 4H bearish, fundamental bearish medium (EUR 0 vs USD +7, check ✅ CONFIRMED · could get even stronger).

**Structura acum** (rândul 27 nov 13:00, close 1.09671; ATR(14) 1H = 0.0010093; ATR(14) 4H = 0.0019446):
- D: swing ↓ CHoCH 1.17116, BOS gol · internal ↓ CHoCH 1.127315, BOS gol · fractal ↓ CHoCH 1.101015, BOS 1.088115, pos 66.6%
- 4H: swing ↓ CHoCH 1.127315, BOS gol · internal ↓ CHoCH 1.100585, BOS 1.09573, pos 20.2% · fractal ↓ CHoCH 1.100585, BOS 1.088115, pos 68.9%
- 1H: swing ↓ CHoCH 1.101015, BOS 1.088115, pos 66.6% · internal ↑ CHoCH 1.09313, BOS 1.09867, pos 64.6% · fractal ↑ CHoCH 1.093405, BOS 1.0993, pos 56.1% (pullback contra swing)
- Zone: D supply rafinată 1.09664–1.101015, testată 5x · 4H supply rafinată 1.097345–1.100585, testată 5x · 1H supply 23 nov 14:00 rafinată 1.09933–1.100585 proaspătă · 1H demand 25 nov 19:00 rafinată 1.093405–1.09486 proaspătă.

**Ce urmăresc:** 1.09573 (BOS internal 4H, la 9.8 pips), 1.093405 (CHoCH fractal 1H = vârful demand-ului 1H), 1.100585 (CHoCH internal/fractal 4H + distal supply 1H), 1.101015 (CHoCH fractal D / swing 1H). Părerea se schimbă la o închidere 1H peste 1.101015.

- **[1H] SKIP** — short: preț 1.09671 sub zonă (26 pips), la 9.8 pips de prima țintă → intrare târzie; zona aceeași cu setup-ul anulat. Long din demand 1H: contra swing-ului D/4H și contra fundamentalului → nu se propune.
- **[4H] SKIP** — zonele D și 4H testate de 5 ori.

### Perechile cu date inconsistente (orientativ, fără setup-uri)
- **GBPUSD** — D ↓, 4H swing ↑ (internal/fractal ↓), 1H swing ↓. Preț 1.31299 în supply 4H 1.31138–1.314395 (testat 1x) / 1H (testat 5x). Diferență seed/live: 4H zone refined low.
- **USDJPY** — D swing ↑/↓ neclar (diferență seed/live pe D swing); 4H swing ↓, fractal 4H ↑ de la 12:00; 1H internal/fractal ↑. Demand 4H proaspăt 159.142–159.3455.
- **USDCHF** — D ↑, 4H swing ↑ (internal/fractal ↓), 1H ↑. Preț 0.834315 sub supply 4H 0.834595–0.837135 (testat 4x).
- **USDCAD** — D swing neclar (diferență seed/live), 4H swing ↑, 1H swing ↓ / fractal ↑. Supply 4H proaspăt 1.427955–1.429435; demand 1H 1.422275–1.423825 testat 1x.
- **AUDUSD** — D swing neclar (diferență seed/live), 4H swing ↓ cu internal/fractal ↑, 1H ↑. Preț 0.666935 peste CHoCH fractal D 0.66649 (break neconfirmat pe D).
- **NZDUSD** — D ↓, 4H swing ↓ (fractal ↑), 1H swing ↓ (internal/fractal ↑). Preț 0.54866 în supply D 0.548445–0.553375 testat 7x.

### Restul perechilor
21 de cross-uri: istorie insuficientă (4 rânduri, 27 nov 10:00–13:00) — fără setup-uri. XAUUSD: date lipsă (fără CSV). Biasul fundamental din tabel e doar referință.

_Analiză condiționată, nu semnal de tranzacționare. Mărimea poziției nu e dată._
