# Analiza MTF — bilanț săptămânal 2026-W48 (23–27 nov 2026)

Generat sâmbătă 28 nov 2026 (rulare programată, nesupravegheată). Cifrele sunt calculate în cod din `reports/mtf/closed.jsonl`, `reports/mtf/state.json` și `data/fsb/*.csv`.

**Presupuneri notate**
- Analiza MTF programată a început vineri 27 nov (prima rulare 09:45, ultima 20:11; 8 rapoarte). Luni–joi nu a rulat, deci săptămâna = vineri. Cumulat = săptămâna (nu există istorie anterioară).
- „Mișcare mare” = range-ul max−min (în ordinea atinsă) în fereastra măsurată, raportat la ATR(14) 4H calculat pe lumânări 4H construite din 1H (ora București), cu ATR-ul de dinaintea ferestrei. Ferestre: vineri 08:00–24:00 (când au existat rulări) și, doar ca context, luni–vineri.
- Cele 21 de cross-uri au 14 rânduri (doar 27 nov): ATR 4H indisponibil, nu pot fi măsurate.
- Pro/contra fundamental față de `imports/2026-W48-final.json`.

## Pe scurt
- Săptămâna a avut **un singur setup** (EURUSD [1H] short, clasa A, acceptat de tine). Prețul n-a mai urcat în zonă (a rămas la 15.4 pips sub ea) și a coborât direct la prima țintă → setup anulat fără intrare. **Rezultat: 0 R din 0 intrări.**
- Direcția a fost corectă: EURUSD a scăzut vineri ~2.4 × ATR 4H, exact cum spuneau structura și fundamentalul, dar fără pullback în zona de vânzare.
- Ce a blocat cel mai mult nu au fost regulile, ci **datele**: cele 6 perechi cu USD (în afară de EURUSD) au stat toată ziua pe „date inconsistente”, iar cross-urile pe „istorie insuficientă”. NZDUSD a avut o mișcare bearish de 2.2 × ATR 4H, în direcția trendului și a fundamentalului, pe care n-am putut-o analiza.
- **Nicio propunere de regulă** săptămâna asta: eșantionul (n = 1) e mult sub pragul de 15. Rămân doar observații „de urmărit”.

## Bilanțul

### Stări (săptămână = cumulat)
| Stare | n |
|---|---|
| Expirate fără atingere | 0 |
| Invalidate (TP1 atins fără intrare) | 1 |
| Intrate (open) | 0 |
| SL | 0 |
| TP1 / TP2 / TP3 | 0 / 0 / 0 |
| Încă deschise în `state.json` | 0 |
| **Total închise** | **1** |

Rezultat virtual: **0 R** (n intrate = 0). MFE / MAE: indisponibil (niciun setup intrat). — eșantion mic, orientativ.

### Defalcare (toate n = 1 sau 0 — eșantion mic, orientativ)
| Categorie | n | Intrate | R |
|---|---|---|---|
| Clasa A+ / A / B | 0 / 1 / 0 | 0 | 0 |
| 4H / 1H | 0 / 1 | 0 | 0 |
| Pro-trend / counter-trend | 1 / 0 | 0 | 0 |
| Pro- / contra-fundamental | 1 / 0 | 0 | 0 |
| EURUSD | 1 | 0 | 0 |
| Decizie: acceptat / respins / nedecis | 1 / 0 / 0 | 0 | 0 |

Acceptat vs respins: nu se poate compara (0 setup-uri respinse).

### Setup-ul închis
| id | Plan | Ce s-a întâmplat |
|---|---|---|
| EURUSD-20261127-0945-1 | [1H] short A, zona 1.09933–1.100585, limit 1.09933, SL 1.100671, TP 1.09573 / 1.09486 / 1.088115 | Maxim după creare (10:00–22:00) 1.09779 = 15.4 pips sub marginea zonei. La 11:00 minimul 1.095585 a atins TP1 → anulat („TP1 fără intrare”). Prețul a continuat până la 1.09321 (21:00). |

## Ce a lipsit (descriptiv, nu e semnal)
Vineri 08:00–24:00, perechi cu ATR 4H disponibil:

| Pereche | Range / ATR 4H | Net / ATR 4H | Bias fundamental | Ar fi putut prinde regulile? Ce a blocat |
|---|---|---|---|---|
| EURUSD | 2.64× (1.098265 → 1.09312) | −2.19× | bearish, medium | Direcția era identificată (setup A acceptat). Blocat de condiția de pullback: prețul n-a ajuns în zonă (premium), apoi la 20:11 SKIP pentru intrare târzie în discount + vineri seara. Mișcare de continuare fără pullback — regulile actuale nu intră în astfel de mișcări, intenționat. |
| NZDUSD | 2.18× (0.54944 → 0.54576) | −1.47× | bearish, low | Swing D și 4H bearish toată ziua, în direcția fundamentalului → ar fi putut exista un setup pro-trend. Blocat de „date inconsistente” (`seed_vs_live.diff = 1`), nu de reguli. |
| AUDUSD | 1.92× | −0.97× | bearish | sub prag |
| USDCHF | 1.91× | +1.01× | bullish | sub prag |
| GBPUSD | 1.78× | −1.23× | bearish | sub prag |
| USDCAD | 1.65× | +0.56× | bullish | sub prag |
| USDJPY | 1.14× | +0.83× | bullish | sub prag |
| 21 cross-uri | indisponibil | — | — | 14 rânduri, fără ATR 4H; „istorie insuficientă” |

Context luni–joi (fără rulări MTF, deci nimic de atribuit regulilor): toate cele 7 perechi cu USD au avut range peste 2× ATR 4H; cele mai mari USDCAD 7.85× (net −4.04×, contra biasului bullish) și USDCHF 7.54× (net −1.93×, contra biasului bullish); USDJPY net +3.05× (cu biasul bullish).

## Propuneri
**Nicio propunere nouă.** Pragul minim e 15 cazuri pe categorie; săptămâna are n = 1. Propuneri anterioare: niciuna în `proposals.md`.

De urmărit (fără schimbare de regulă):
1. **Setup-uri anulate cu „TP1 atins fără intrare”** — n = 1 (EURUSD-20261127-0945-1), 0 R. Dacă se repetă în tendințe puternice, de măsurat câte setup-uri pro-trend ratează mișcarea fără pullback și cât ar fi dat o intrare pe confirmare la un nivel intermediar. Verificare: doar pe setup-uri noi din W49+; se discută la ≥ 15 cazuri.
2. **Blocaje din date, nu din reguli** — pe toată ziua de vineri, 6 din 7 perechi cu istorie (GBPUSD, USDJPY, USDCHF, USDCAD, AUDUSD, NZDUSD) au fost excluse pentru `seed_vs_live.diff = 1`, iar 21 de cross-uri pentru istorie insuficientă. Asta e o problemă de pipeline (seed-uri manuale vs alerte live), în afara regulilor din `ANALYST.md`; nu o rezolv aici (nu modific scripturi/date). Până se rezolvă, bilanțul nu va avea eșantion.
