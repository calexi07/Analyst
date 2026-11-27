# Analiza MTF — vineri 27 nov 2026, 11:10 București (sesiunea de dimineață, înainte de Londra)

**Date:** cel mai vechi și cel mai nou „ultimul rând” = 27 nov 10:00 (lumânarea 10:00–11:00, închisă; sub pragul de 2h) pentru toate cele 28 de perechi cu CSV. XAUUSD: fără CSV. Export `fsb-export` pornit la 11:07 (run 45971064922), terminat cu succes; `meta.json` 09:07:40 UTC. Lumânarea 11:00 nu e încă închisă, deci nu există lumânări noi față de rularea de la 11:02. Nou: GBPUSD, USDJPY, USDCHF, USDCAD, AUDUSD, NZDUSD au acum istorie (298 rânduri seed + 1 live = 299) și sunt analizate complet. Celelalte 21 de cross-uri au tot 1 rând. · **Fundamental:** `imports/2026-W48-final.json` · **Check:** `imports/check-2026-11-27-morning.json` (06:00 București).

Presupuneri notate (rulare nesupravegheată):
- **Cusătura seed / live:** la USDJPY, USDCAD și AUDUSD, swing-ul D își schimbă direcția între ultimul rând seed (09:00) și primul rând live (10:00) fără ca prețul să spargă vreun nivel (ex. USDJPY CHoCH D 163.99 → 139.58). E un efect al adâncimii diferite de istorie dintre exportul manual și cel live, nu un CHoCH real. Tratez swing-ul D al acestor trei perechi ca **neclar** (pilonul D nu se numără) și nu le trec la „De interes”. La fel, zonele cu „since 27 nov 10:00” care au aceeași zonă completă ca una mai veche le tratez ca zona veche (cu numărul ei de testări).
- Setup-ul EURUSD rămâne **acceptat** (`wl:mtf:EURUSD-20261127-0945-1`). Cardul din Watchlist păstrează declanșatorul vechi „1.0934”; urmăresc planul original corectat din `state.json`.
- Nicio știre CRITICAL în următoarele 24h pe USD, EUR, GBP, JPY, CHF, CAD, AUD, NZD. HIGH: S&P review Franța (dată neconfirmată); luni Canada GDP Q3 și discursul Ueda; duminică OPEC+ (MEDIUM). Wall Street închide la 20:00 București.

## Overview
🎯 **Setup-uri bune acum**
- EURUSD · Short · [1H] · A — așteaptă atingerea zonei 1.09933–1.100585 (acum 29 pips sub ea).

📍 **Aproape**
- EURUSD — la 7.0 pips de 1.09573 (BOS internal 4H = TP1 al setup-ului). Atingerea = continuare bearish pe 4H, dar anulează setup-ul short (TP1 fără intrare).
- USDJPY — la 1.6 pips sub 159.458 (CHoCH fractal 4H). O închidere 4H peste = fractalul 4H se întoarce în sus, în direcția fundamentalului (bullish).
- USDCHF — la 8.3 pips sub 0.837135 (CHoCH fractal 4H). O închidere 4H peste = 4H fractal din nou bullish, aliniat cu swing-ul D/4H și cu fundamentalul.
- GBPUSD — la 19.6 pips sub 1.314395 (CHoCH fractal 4H = vârful supply-ului 4H/1H). O închidere peste = supply-ul invalidat, contra biasului bearish.
- AUDUSD — 11.7 pips peste 0.66649 (CHoCH fractal D, pos 111%). O închidere zilnică peste = fractalul D bullish și supply-ul D invalidat, contra biasului bearish.

👀 **De interes**
- AUDUSD — CHoCH 4H internal și fractal în sus azi la 08:00 (raliu puternic, contra fundamentalului bearish).
- USDJPY — fractalul 4H a trecut bearish pe 25 nov 20:00; acum prețul îi testează CHoCH-ul.
- USDCHF — internal 4H bearish din 25 nov 16:00 (pullback în swing-ul 4H bullish); 1H internal și fractal au revenit bullish la 10:00.

## Schimbări de la ultima rulare
- Nicio schimbare de stare (nicio lumânare nouă). EURUSD-20261127-0945-1 rămâne **waiting**, decizie: **acceptat**.
- Watchlist: planul tău EURUSD (din propunerea MTF) — **încă valid**: 1H swing tot bearish, supply-ul 1H proaspăt, neatins.
- Date: 6 perechi USD au primit istorie (seed manual) → analizate; niciuna nu trece pragul de calitate acum.

## Pe scurt
**EURUSD** — Daily și 4H sunt bearish, fundamentalul la fel (dolarul mult mai puternic decât euro). Pullback-ul în sus de pe 1H a obosit: prețul e aproape de minimele de pe 4H, departe de zona de supply.
- [1H] Sell (A): dacă prețul revine în supply-ul de pe 1H (partea scumpă), structura fractală de pe 1H se rupe în jos → intri la jumătatea mișcării de rupere (sau cu limit la marginea zonei). SL deasupra vârfului zonei. Ținte: minimele de pe 4H, demand-ul de pe 1H, minimul mare de dedesubt.
  Limit: Entry ~1.09933 · SL 1.10067 · TP 1.09573 / 1.09486 / 1.08812 (2.7R / 3.3R / 8.4R)
  Confirmare (exemplu): Entry ~1.09845 · SL 1.10009 · TP 1.09573 / 1.09486 / 1.08812 (1.7R / 2.2R / 6.3R)
- Ce anulează ideea: o închidere 1H deasupra zonei, sau atingerea primei ținte fără intrare (foarte aproape). Valabil până azi 22:00.
- [4H] SKIP: zonele de pe Daily și 4H au fost testate de prea multe ori.

**USDCAD** — Fundamentalul e clar bullish (dolar puternic, CAD slab), 4H e bullish, dar de ieri prețul doar oscilează într-un interval îngust, iar 1H și-a schimbat direcția de patru ori peste noapte. Demand-ul nou de pe 1H n-a avut o plecare puternică și chiar deasupra stă un supply proaspăt de pe 4H. Nimic calitativ acum; devine interesant dacă prețul coboară curat în zona de discount și pleacă puternic.

**USDJPY** — Prețul e chiar sub nivelul care ar întoarce structura rapidă de pe 4H în sus. Fundamentalul e bullish, dar 4H e încă bearish și prețul e în partea scumpă: nimic de luat acum. O închidere 4H peste nivel ar fi primul semn pentru un long viitor.

**USDCHF** — Daily, 4H și fundamentalul sunt bullish, iar 1H tocmai a reluat urcarea. Problema: prețul e deja în partea scumpă a range-ului, nu în discount. Aștept un pullback mai adânc.

**AUDUSD** — Raliu puternic azi, contra fundamentalului bearish; Daily e aproape să-și întoarcă structura rapidă. Un short ar avea prea puțini piloni, un long ar fi contra fundamentalului.

**SKIP:** GBPUSD (supply testat de prea multe ori, 4H contra biasului), NZDUSD (supply D testat de 7 ori, preț la mijloc) — nimic calitativ.

**Istorie insuficientă (1 rând):** EURGBP, EURJPY, EURCHF, EURAUD, EURNZD, EURCAD, GBPJPY, GBPCHF, GBPAUD, GBPNZD, GBPCAD, AUDJPY, AUDCHF, AUDNZD, AUDCAD, NZDJPY, NZDCHF, NZDCAD, CADJPY, CADCHF, CHFJPY — fără setup-uri. **XAUUSD:** date lipsă.

## Tabel sumar
| Pereche | D / 4H / 1H swing | Fundamental | Conviction | Cel mai bun setup | Clasă |
|---|---|---|---|---|---|
| EURUSD | ↓ / ↓ / ↓ (1H internal + fractal ↑ = pullback) | bearish (medium) · check: ✅ CONFIRMED · could get even stronger | High | [1H] Short pro-trend din supply 1H proaspăt 1.09933–1.100585 · [4H] SKIP | A |
| GBPUSD | ↓ / ↑ / ↓ | bearish (medium) · check: ⚠️ UNDER PRESSURE | Medium | SKIP — preț în supply 4H/1H testat de 5 ori; 4H swing ↑ contra fundamentalului | — |
| USDJPY | D ? (seed ↓ / live ↑) / ↓ / ↓ | bullish (medium) · check: 👀 UNDER WATCH | Low | SKIP — short ar fi contra fundamentalului, supply 4H testat 2x; long în premium | — |
| USDCHF | ↑ / ↑ / ↑ | bullish (low) · check: ✅ CONFIRMED | Medium | SKIP — preț în premium pe swing 4H/1H, demand-ul nou tot în premium | — |
| USDCAD | D ? (seed ↑ / live ↓) / ↑ / ↓ | bullish (medium) · check: ✅ CONFIRMED | Medium | SKIP — chop 30 pips, demand 1H fără plecare puternică, supply 4H proaspăt la 15 pips | — |
| AUDUSD | D ? (seed ↓ / live ↑) / ↓ / ↑ | bearish (medium) · check: ⚠️ UNDER PRESSURE | Medium | SKIP — short 2/5 (C), long contra fundamentalului | C |
| NZDUSD | ↓ / ↓ / ↓ | bearish (low) · check: ✅ CONFIRMED | Medium | SKIP — supply D testat de 7 ori, preț la mijlocul range-ului 1H | — |
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

### Perechile USD noi (câte un rând; niciun setup nu trece pragul)
- **GBPUSD** — Bias bearish · Conviction Medium (D + fundamental, 4H swing ↑ contra). D ↓ (fractal CHoCH 1.345935, pos 25.3); 4H swing ↑ CHoCH 1.30102 pos 13.3, internal/fractal ↓; 1H swing ↓ pos 52.3, internal ↑. Preț 1.312435 în supply 4H 1.30759–1.314395 (testat 5x) și supply 1H rafinat 1.31231–1.314395 (testat 5x) → zonă uzată. SKIP. ATR 1H 0.00101 / 4H 0.00243.
- **USDJPY** — Bias bullish · Conviction Low (D neclar la cusătură, 4H ↓ contra). D internal/fractal ↓ CHoCH 160.394; 4H swing ↓ CHoCH 160.394 pos 87.3, fractal ↓ CHoCH 159.458; 1H internal ↓, fractal ↑ CHoCH 159.142. Long: 4H/1H swing ↓ și preț în premium → nu. Short: contra fundamentalului (max B) și supply 4H 159.374–159.458 testat 2x → nu. SKIP. Nivel-cheie 159.458.
- **USDCHF** — Bias bullish · Conviction Medium (D, 4H și fundamental aliniate, dar conviction fundamental low). D ↑ (internal BOS 0.844425); 4H swing ↑ pos 74.4 (premium), internal ↓ CHoCH 0.844425, fractal ↓ CHoCH 0.837135; 1H internal/fractal ↑ de la 10:00. Demand 1H nou 0.833385–0.835175 (proaspăt) = ~71% din range-ul swing 1H/4H → premium; preț în supply 4H 0.834395–0.837135 (testat 4x). Demand D 0.813285–0.83133 proaspăt, departe. SKIP.
- **USDCAD** — Bias bullish · Conviction Medium (4H + fundamental; D neclar). 4H swing ↑ CHoCH 1.39299; 4H internal ↓ CHoCH 1.43847 BOS 1.41901 pos 28.1 (discount); 1H fractal ↑ de la 10:00 CHoCH 1.422275. Demand 1H 1.422275–1.424345 (rafinat 1.422275–1.423825) proaspăt, dar plecarea e o lumânare de 12 pips într-un range 1.42228–1.42554 din care 1H fractal a ieșit de 4 ori de la 02:00 → zonă fără plecare puternică. Supply 4H proaspăt 1.42601–1.429435 la 15 pips: limit 1.423825 / SL 1.422169 (16.6 pips) dă TP1 1.42601 = 1.3R. Pilonii ar da 4/5, dar zona nu îndeplinește criteriul de calitate → SKIP (presupunere de calitate, notată). Supply D proaspăt 1.429925–1.43847.
- **AUDUSD** — Bias bearish · Conviction Medium (4H + fundamental; D neclar). D fractal ↓ CHoCH 0.66649 cu prețul peste (pos 111.1%, break neconfirmat pe D); 4H swing ↓ CHoCH 0.7238, internal ↑ și fractal ↑ de la 08:00; 1H swing/internal/fractal ↑ (BOS fractal 0.667785). Short: 4H ↓ + fundamental = 2/5 (C), preț peste distal-ul supply-ului D. Long: contra fundamentalului. SKIP.
- **NZDUSD** — Bias bearish · Conviction Medium (D, 4H și fundamental aliniate, conviction fundamental low). D ↓, 4H swing ↓, 4H internal ↓ CHoCH 0.553375 pos 43.4; 1H swing ↓ pos 52.1 (mijloc), internal/fractal ↑ (pullback, BOS 0.55052). Preț 0.54856 în supply D 0.548225–0.553375 testat 7x; supply D 0.55275–0.564965 (proaspăt) prea departe și prea lat pentru un SL rezonabil. SKIP.

### Restul perechilor
21 de cross-uri: istorie insuficientă (1 rând, 27 nov 10:00) — zonele nu se pot verifica, fără setup-uri. XAUUSD: date lipsă (fără CSV). Biasul fundamental din tabel e doar referință.

_Analiză condiționată, nu semnal de tranzacționare. Mărimea poziției nu e dată._
