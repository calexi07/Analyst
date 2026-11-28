# Analiza MTF — bilanț săptămânal 2026-W48 (23–27 nov 2026) + ce urmăresc în W49 (30 nov – 4 dec)

Generat sâmbătă 28 nov 2026 (rulare programată, nesupravegheată), după procedura `prompts/mtf/WEEKLY.md` v2.0. **Înlocuiește versiunea de la 09:50** (care e în istoria git): între timp WEEKLY.md a primit părțile „Săptămâna care a trecut” și „Ce urmăresc”. Bilanțul setup-urilor e neschimbat. Toate cifrele sunt calculate în cod.

**Surse și presupuneri**
- Structura (BE FSB Export, `data/fsb/*.csv`): **EURUSD** are toată săptămâna (seed v1.2, până vineri 23:00). **Celelalte 6 perechi cu USD** au doar seed-ul manual, până **vineri 10:00** (rândurile live de vineri nu mai sunt în CSV); seed-urile lor sunt mai vechi decât v1.2, deci pot fi încă pe parametrii vechi (swing 30 / internal 5) — structura poate părea mai lentă. **Cele 21 de cross-uri și XAUUSD**: 14 rânduri (vineri 10:00–23:00), respectiv nimic → istorie insuficientă.
- Ca să acopăr toate cele 29 de perechi am folosit, **etichetat „(ta)”**, `exports/ta-2026-11-28.json` (motorul bias-engine-ta, bare Yahoo Finance, închidere vineri). E alt motor decât indicatorul tău: nivelurile pot diferi cu câțiva pips, iar structura lui poate diferi de FSB (exemplu: la EURUSD ta vede 4H întors în sus, FSB vede 4H bearish). Unde am FSB, FSB are prioritate.
- Mișcarea săptămânii și puterea monedelor: `exports/price-action-2026-W48.json` (închideri zilnice Daily Observer, 28 perechi × 5 zile), log-randamente, media celor 7 perechi ale fiecărei monede cu semn; σ din `exports/fx-vol-2026-W48.json` (26 săptămâni).
- ATR 4H: din lumânări 4H construite din 1H (ora București), ATR(14) de dinaintea ferestrei. Pentru cross-uri (fără istorie) am folosit ATR 4H din (ta) — sursă amestecată, notată.
- Fundamental W49: `imports/2026-W49-phase1.json` (PHASE 1; FINAL-ul vine după delta check-ul de duminică seara și poate schimba scoruri). Verificare zilnică pentru W49: **încă nu există** (ultima, `check-2026-11-27-morning`, e pentru W48), deci nu am status/hook pentru săptămâna viitoare.
- „Primul paragraf” din story = primul paragraf de text de după titlul îngroșat (titlul e deja dat separat).
- Tunelul EMA 144/169: nu e în CSV → indisponibil.

## Pe scurt
- **Piața W48:** CAD și CHF au fost cele mai puternice, JPY și EUR cele mai slabe; aurul +3.3%. USD aproape neutru (−0.10%) după o săptămână cu dus-întors: luni USD puternic (EURUSD a rupt minimul săptămânii trecute), marți–joi pullback, vineri din nou în jos la EURUSD.
- **Setup-uri:** unul singur (EURUSD [1H] short A, acceptat de tine), anulat fără intrare — prețul a căzut direct la TP1 fără să revină în zonă. **0 R din 0 intrări (n = 1).** Direcția a fost corectă.
- **Ce a lipsit:** vineri, EURUSD (2.2× ATR 4H) — exact setup-ul nostru, fără pullback; EURGBP (2.1×) și EURCAD (2.1×, contra biasului bullish W48) — blocate de istoria insuficientă a cross-urilor, nu de reguli.
- **Problema principală rămâne datele:** 22 din 29 de perechi n-au istorie FSB suficientă, iar 6 perechi USD se opresc vineri 10:00.
- **Propuneri:** niciuna — n = 1, sub pragul de 15.
- **W49 de urmărit:** EURUSD și NZDUSD short (Daily + fundamental aliniate), GBPNZD long după pullback, EURGBP și CADJPY short pe supply. Săptămână cu HICP (mar), ISM (mar/joi), PIB Australia și CPI Elveția (mie), NFP + LFS Canada (vin).

## 🌍 Fundamental W49 (PHASE 1, generat 28 nov; fără verificare zilnică W49)
Scoruri: USD +7 (Strong) · XAU +6 (Strong) · AUD +4 (Improving) · GBP +3 (Improving) · EUR 0 · JPY 0 · CHF −1 · NZD −3 · CAD −6 (Weak).
Textul exact din postările TradingView (titlu, primul paragraf, rândul de bias):

- **EURUSD** — *EURUSD: Dollar on Full Price vs Calmer Euro | W49*  
  Europe got a lower energy bill and a calmer bond market this week, but it is hard to outrun a central bank that still has two hikes on its mind.  
  `Week 49 bias: BEARISH (USD favoured) | Medium conviction`
- **GBPUSD** — *GBPUSD: Dollar on Full Price vs Hawkish Sterling | W49*  
  Two hawkish central banks, one gap: the Bank of England talks tough, but the Fed talks tough with a 4.3% growth number behind it.  
  `Week 49 bias: BEARISH (USD favoured) | Low conviction`
- **USDJPY** — *USDJPY: Dollar on Full Price vs Torn Yen | W49*  
  A dollar backed by hot growth meets a yen pulled in two directions — a hawkish BoJ member on one side, softer Tokyo prices on the other.  
  `Week 49 bias: BULLISH (USD favoured) | Medium conviction`
- **USDCHF** — *USDCHF: Dollar on Full Price vs Taxed Franc | W49*  
  The franc woke up to a tariff letter from Washington this week, and it still pays nothing to hold.  
  `Week 49 bias: BULLISH (USD favoured) | Low conviction`
- **USDCAD** — *USDCAD: Dollar on Full Price vs Oil-Drained Loonie | W49*  
  The widest gap on the board again: a dollar with strong growth against a loonie still nursing an oil hangover.  
  `Week 49 bias: BULLISH (USD favoured) | Low conviction`
- **AUDUSD** — *AUDUSD: Dollar on Full Price vs Inflation Aussie | W49*  
  Australian inflation just ran hotter than forecast, giving the Aussie its best argument in weeks — but the dollar's argument is still louder.  
  `Week 49 bias: BEARISH (USD favoured) | Low conviction`
- **NZDUSD** — *NZDUSD: Dollar on Full Price vs Hung-Vote Kiwi | W49*  
  New Zealand woke up without a government majority, while America woke up to 4.3% growth — this pair has a clear favourite.  
  `Week 49 bias: BEARISH (USD favoured) | Medium conviction`
- **EURGBP** — *EURGBP: Hawkish Sterling vs Calmer Euro | W49*  
  Cheap oil helps Frankfurt, but hawkish voices at the Bank of England give London the sharper story this week.  
  `Week 49 bias: BEARISH (GBP favoured) | Low conviction`
- **EURJPY** — *EURJPY: Calmer Euro vs Torn Yen | W49*  
  Two energy importers, both helped by cheaper oil, and both stuck at zero — a true stand-off.  
  `Week 49 bias: TWO-SIDED | Low conviction`
- **EURCHF** — *EURCHF: Calmer Euro vs Taxed Franc | W49*  
  Neighbours at the bottom of the rate ladder — one helped by cheap energy, the other hit by a US tariff plan.  
  `Week 49 bias: TWO-SIDED | Low conviction`
- **EURAUD** — *EURAUD: Inflation Aussie vs Calmer Euro | W49*  
  Last week a tie; this week Australian inflation broke it, and the Aussie now holds the better hand against a cooling euro.  
  `Week 49 bias: BEARISH (AUD favoured) | Low conviction`
- **EURNZD** — *EURNZD: Calmer Euro vs Hung-Vote Kiwi | W49*  
  The kiwi lost its political footing this week, and that alone is enough to tilt this pair toward the euro.  
  `Week 49 bias: BULLISH (EUR favoured) | Low conviction`
- **EURCAD** — *EURCAD: Calmer Euro vs Oil-Drained Loonie | W49*  
  Oil is the hinge again: every dollar off a barrel helps Europe and hurts Canada.  
  `Week 49 bias: BULLISH (EUR favoured) | Low conviction`
- **GBPJPY** — *GBPJPY: Hawkish Sterling vs Torn Yen | W49*  
  The pound brings hawkish speeches and decent yield; the yen brings shelter and a divided BoJ — sterling has the edge.  
  `Week 49 bias: BULLISH (GBP favoured) | Low conviction`
- **GBPCHF** — *GBPCHF: Hawkish Sterling vs Taxed Franc | W49*  
  Sterling found its voice this week; the franc found a tariff bill — a small but clear tilt toward the pound.  
  `Week 49 bias: BULLISH (GBP favoured) | Low conviction`
- **GBPAUD** — *GBPAUD: Hawkish Sterling vs Inflation Aussie | W49*  
  Two currencies with hawkish news this week — sterling from speeches, the Aussie from hard data — and the score calls it nearly even.  
  `Week 49 bias: TWO-SIDED | Low conviction`
- **GBPNZD** — *GBPNZD: Hawkish Sterling vs Hung-Vote Kiwi | W49*  
  A hawkish Bank of England meets a kiwi with no government majority — the pound is favoured.  
  `Week 49 bias: BULLISH (GBP favoured) | Medium conviction`
- **GBPCAD** — *GBPCAD: Hawkish Sterling vs Oil-Drained Loonie | W49*  
  Hawkish Britain against oil-hit Canada: this is the widest sterling gap of the week.  
  `Week 49 bias: BULLISH (GBP favoured) | Low conviction`
- **AUDJPY** — *AUDJPY: Inflation Aussie vs Torn Yen | W49*  
  A hot Australian inflation print meets a yen whose central bank cannot agree with its data — the Aussie is favoured.  
  `Week 49 bias: BULLISH (AUD favoured) | Low conviction`
- **AUDCHF** — *AUDCHF: Inflation Aussie vs Taxed Franc | W49*  
  High yield and hot inflation against zero yield and a new tariff bill — the Aussie leads this matchup.  
  `Week 49 bias: BULLISH (AUD favoured) | Low conviction`
- **AUDNZD** — *AUDNZD: Inflation Aussie vs Hung-Vote Kiwi | W49*  
  Hot inflation in Australia, a hung parliament in New Zealand — the trans-Tasman gap widens.  
  `Week 49 bias: BULLISH (AUD favoured) | Medium conviction`
- **AUDCAD** — *AUDCAD: Inflation Aussie vs Oil-Drained Loonie | W49*  
  The Aussie has fresh inflation news; the loonie still has an oil problem — this is the widest Aussie gap of the week.  
  `Week 49 bias: BULLISH (AUD favoured) | Low conviction`
- **NZDJPY** — *NZDJPY: Torn Yen vs Hung-Vote Kiwi | W49*  
  A kiwi without a government majority against a yen with a divided central bank — the yen is favoured.  
  `Week 49 bias: BEARISH (JPY favoured) | Low conviction`
- **NZDCHF** — *NZDCHF: Hung-Vote Kiwi vs Taxed Franc | W49*  
  Two currencies with political or trade headaches — a near tie, with a slight lean to the franc.  
  `Week 49 bias: TWO-SIDED | Low conviction`
- **NZDCAD** — *NZDCAD: Hung-Vote Kiwi vs Oil-Drained Loonie | W49*  
  Two commodity currencies with different problems — politics for the kiwi, oil for the loonie — and the kiwi edges ahead.  
  `Week 49 bias: BULLISH (NZD favoured) | Low conviction`
- **CADJPY** — *CADJPY: Torn Yen vs Oil-Drained Loonie | W49*  
  An oil exporter against an oil importer in a month when crude fell sharply — the yen is favoured.  
  `Week 49 bias: BEARISH (JPY favoured) | Low conviction`
- **CADCHF** — *CADCHF: Taxed Franc vs Oil-Drained Loonie | W49*  
  Oil-hit Canada against tariff-hit Switzerland — the franc is favoured, but with low conviction.  
  `Week 49 bias: BEARISH (CHF favoured) | Low conviction`
- **CHFJPY** — *CHFJPY: Taxed Franc vs Torn Yen | W49*  
  Two havens, both with a new US tariff threat — the scale calls it two-sided.  
  `Week 49 bias: TWO-SIDED | Low conviction`
- **XAUUSD** — *XAUUSD: Leaking Gold vs Dollar on Full Price | W49*  
  Gold bounced almost 4% on Friday, but its own fundamentals slipped — the stand-off leans slightly toward the dollar.  
  `Week 49 bias: TWO-SIDED | Low conviction`

## 1. Săptămâna care a trecut (W48, piața)

**Puterea monedelor** (media celor 7 perechi, log-randament săptămânal, n = 7 fiecare): CAD **+0.69%** · CHF +0.44% · AUD +0.41% · GBP +0.01% · USD −0.10% · NZD −0.20% · EUR −0.43% · JPY **−0.82%**. XAUUSD +3.29%.

**În cuvinte simple**
- Luni a fost ziua mare: USD a urcat, EURUSD, GBPUSD, AUDUSD și NZDUSD au luat minimul săptămânii trecute (EURUSD cu închidere de corp sub el), iar USDCAD a luat maximul săptămânii trecute. Apoi marți–joi a venit pullback-ul contra USD.
- CAD a dominat săptămâna: USDCAD a coborât de la maximul de luni sub minimul săptămânii trecute, iar fractalul Daily s-a întors în jos (25 nov). Toate cross-urile cu CAD au mers contra biasului fundamental W48 (EURCAD −1.8σ, GBPCAD −1.2σ, CADJPY +1.1σ).
- JPY a fost cel mai slab: toate cross-urile JPY au urcat (CADJPY +1.29%, CHFJPY +1.13%, AUDJPY +1.09%), dar pe Daily cele mai multe sunt încă bearish (ta) — urcarea e pullback pe 4H.
- CHF puternic: USDCHF a coborât miercuri în demand-ul Daily proaspăt și a reacționat în sus; EURCHF −1.4σ.
- Vineri: EURUSD a reluat scăderea (2.2× ATR 4H), EURGBP și EURCAD la fel; aurul a recuperat după ce a luat minimul săptămânii trecute miercuri.
- Structuri D/4H: puține schimbări pe Daily (doar USDCAD fractal D → bearish); pe 4H multe întoarceri fractale/interne — piața a stat în pullback-uri, nu în trenduri noi.

**Pereche cu pereche — perechile cu USD (FSB; EURUSD până vineri 23:00, restul până vineri 10:00)**

| Pereche | Săpt. (DO) | σ | Range / ATR 4H | Lichiditate luată | Structură D/4H în săptămână | Zone D/4H |
|---|---|---|---|---|---|---|
| EURUSD | −0.29% | −0.44 | 5.4× | luni: fitil peste maximul de vineri, apoi minimul săpt. trecute 1.09532 rupt cu corp (14:00), minim 1.088115 (19:00); vineri: minimul de joi 1.09573 luat (fitil, 11:00), apoi continuare la 1.09312 | 4H fractal → bearish (luni 16:00); D și 4H swing/internal bearish toată săptămâna | supply D 1.09532–1.101015 și 4H 1.09532–1.100585 atinse de 5×, au ținut (neinvalidate) |
| GBPUSD | +0.11% | +0.16 | 4.9× | luni: minimul săpt. trecute 1.30759 luat, minim 1.301075 | 4H fractal: 3 întoarceri luni, final bearish; 4H swing bullish (contra D) | supply 4H 1.30759–1.314395 atins de 5×, a ținut |
| USDJPY | +0.65% | +0.52 | 3.1× | marți: maximul de luni 159.507 luat cu corp (max 159.5835); miercuri: minimul de marți luat; (ta) vineri: equal highs 159.527 luate și respinse | 4H fractal → bullish luni, → bearish miercuri 20:00 | în supply-ul D 155.2285–160.394 (premium); demand 4H 158.417–158.9315 a ținut |
| USDCHF | −0.47% | −0.52 | 7.2× | luni: minimul săpt. trecute 0.83732 luat cu fitil, respins; marți–miercuri: minimele zilelor luate cu corp | 4H internal → bearish (miercuri 16:00) | demand D 0.813285–0.83133 atins miercuri 14:00 → reacție în sus; supply 4H 0.834395–0.837135 atins de 4× |
| USDCAD | −0.69% | −1.01 | 8.3× | luni: maximul săpt. trecute 1.435755 luat (max 1.43847), apoi minimul săpt. trecute 1.426685 luat marți–miercuri (min 1.41901) | 4H internal → bearish (marți 20:00), **D fractal → bearish (25 nov)** | demand D/4H 1.429925–1.435755 invalidat marți 16:00 |
| AUDUSD | +0.47% | +0.46 | 5.0× | luni: minimul săpt. trecute 0.66086 luat; minim 0.65591 miercuri | 4H internal → bullish (vineri 08:00), 4H fractal 3 întoarceri | supply D 0.6598–0.66649 **invalidat** vineri 04:00 |
| NZDUSD | −0.07% | −0.06 | 4.1× | luni: minimul săpt. trecute 0.54635 luat (min 0.543325); (ta) vineri 21:00: din nou sub 0.54657, respins | 4H fractal → bullish (marți 20:00) | supply D 0.548225–0.553375 atins de 7×, a ținut |

**Cross-uri și aur (doar Daily Observer + ta; FSB fără istorie)** — mișcarea în σ și starea (ta) la închiderea de vineri:
- **Mișcări notabile:** EURCAD −0.97% (−1.84σ; D1 și H4 jos), EURCHF −0.77% (−1.36σ; D1 și H4 jos, equal lows luate joi), GBPCAD −0.59% (−1.21σ; equal lows luate vineri 21:00), CADJPY +1.29% (+1.10σ; H4 sus, maximul săpt. trecute 112.005 luat vineri și respins), EURGBP −0.38% (−1.0σ; D1 și H4 jos), NZDCAD −0.77% (−0.99σ), CHFJPY +1.13% (+0.92σ; H4 sus), XAUUSD +3.29% (+0.89σ; minimul săpt. trecute luat miercuri, apoi revenire), EURAUD −0.71% (−0.86σ; H4 s-a întors jos vineri).
- **Pullback bullish pe 4H, D1 încă jos (ta)**: GBPJPY +0.75%, AUDJPY +1.09%, NZDJPY +0.51%, GBPCHF −0.41% (H4 sus, D1 jos).
- **Fără nimic notabil** (|mișcare| < 0.7σ): EURJPY, EURNZD, GBPAUD, GBPNZD, AUDCHF, AUDNZD, AUDCAD, NZDCHF, CADCHF.

## 2. Bilanțul setup-urilor

Analiza MTF programată a rulat doar vineri 27 nov (8 rulări, 09:45–20:11). Cumulat = săptămâna (nu există istorie anterioară). Toate categoriile au n ≤ 1 → **eșantion mic — orientativ**.

### Stări (săptămână = cumulat)
| Stare | n |
|---|---|
| Expirate fără atingere | 0 |
| Invalidate (TP1 atins fără intrare) | 1 |
| Intrate | 0 |
| SL | 0 |
| TP1 / TP2 / TP3 | 0 / 0 / 0 |
| Încă deschise în `state.json` | 0 |
| **Total închise** | **1** |

Rezultat virtual: **0 R** (n intrate = 0; varianta limit și varianta cu confirmare: niciuna atinsă). MFE / MAE: indisponibil (niciun setup intrat).

### Defalcare
| Categorie | n | Intrate | R |
|---|---|---|---|
| Clasa A+ / A / B | 0 / 1 / 0 | 0 | 0 |
| 4H / 1H | 0 / 1 | 0 | 0 |
| Pro-trend / counter-trend | 1 / 0 | 0 | 0 |
| Pro- / contra-fundamental (W48 FINAL) | 1 / 0 | 0 | 0 |
| EURUSD | 1 | 0 | 0 |
| Decizie: acceptat / respins / nedecis | 1 / 0 / 0 | 0 | 0 |

Acceptat vs respins: nu se poate compara (0 respinse). Cea mai bună / cea mai slabă categorie: nu există diferențe (toate 0 R, n ≤ 1).

### Setup-ul închis
| id | Plan | Ce s-a întâmplat |
|---|---|---|
| EURUSD-20261127-0945-1 | [1H] short A, pro-trend, pro-fundamental, acceptat; zona 1.09933–1.100585, limit 1.09933, SL 1.100671, TP 1.09573 / 1.09486 / 1.088115 | Maximul după creare 1.09779 (10:00) = 15.4 pips sub zonă. La 11:00 minimul 1.095585 a atins TP1 → anulat „TP1 fără intrare”. Prețul a continuat la 1.09312 (21:00). |

### Ce a lipsit (descriptiv, nu e semnal)
Fereastra în care au existat rulări: vineri 08:00–24:00.

| Pereche | Range / ATR 4H | Net / ATR 4H | Bias W48 | Ar fi putut prinde regulile? Ce a blocat |
|---|---|---|---|---|
| EURUSD | 2.21× (FSB) | −1.84× | bearish | Direcția era identificată (setup A acceptat). Blocat de condiția de pullback: prețul n-a revenit în zonă; după 20:11 SKIP (intrare târzie în discount, vineri seara). Continuare fără pullback — regulile nu intră intenționat în astfel de mișcări. |
| EURGBP | 2.13× (10:00–23:00, ATR din ta) | −1.66× | two-sided | Blocat de **istorie insuficientă** (14 rânduri). Fundamental two-sided → oricum ar fi fost cel mult B/C (fără pilonul fundamental). |
| EURCAD | 2.09× (10:00–23:00, ATR din ta) | −1.63× | bullish | Blocat de istorie insuficientă; în plus mișcarea a fost **contra fundamentalului** (bearish vs bias bullish) → maxim B, „⚠ contra fundamentalului”. |
| celelalte 19 cross-uri | 0.8–1.95× | — | — | sub prag |
| GBPUSD, USDJPY, USDCHF, USDCAD, AUDUSD, NZDUSD | indisponibil după 10:00 | — | — | CSV-ul actual se oprește vineri 10:00. Versiunea de la 09:50 le măsurase pe rândurile live de atunci (NZDUSD 2.18×, bearish, pro-fundamental, blocat atunci de „date inconsistente”); acele rânduri nu mai sunt în repo, deci nu le pot recalcula. |

Context luni–joi (fără rulări MTF, nimic de atribuit regulilor): toate cele 7 perechi cu USD au avut range > 2× ATR 4H pe săptămână — USDCAD 8.3× (net −4.5×, contra biasului bullish W48), USDCHF 7.2× (net −1.8×, contra biasului bullish), EURUSD 5.4× (net −1.4×, cu biasul bearish), USDJPY 3.1× (net +2.6×, cu biasul bullish).

## 3. Propuneri
**Nicio propunere nouă.** Pragul minim e 15 cazuri pe categorie; săptămâna are n = 1. Propuneri anterioare aprobate: niciuna.

De urmărit (fără schimbare de regulă):
1. **Anulări „TP1 fără intrare” în tendințe fără pullback** — n = 1 (EURUSD-20261127-0945-1), 0 R. De măsurat pe setup-uri noi (W49+) câte setup-uri pro-trend ratează mișcarea și cât ar fi dat o intrare pe o zonă mai joasă (de exemplu supply-ul 1H lăsat de ruperea din zonă). Se discută la ≥ 15 cazuri.
2. **Acoperirea datelor** — 22 din 29 de perechi fără istorie FSB (≥ 120 rânduri), iar 6 perechi USD fără rândurile de vineri după 10:00. Fără ele bilanțul nu poate avea eșantion și „ce a lipsit” rămâne neverificabil. E o problemă de pipeline (seed-uri / export), nu de regulă; nu o modific aici. Seed-uri v1.2 ca cel de la EURUSD (12 mar – 27 nov) pentru celelalte perechi ar rezolva-o.

## 4. Ce urmăresc în W49 (30 nov – 4 dec)
Fără ordine: doar niveluri și condiții. „(FSB)” = indicatorul tău; „(ta)” = bias-engine-ta (Yahoo), nivelurile pot diferi cu câțiva pips. Fundamental = W49 PHASE 1.

**Știri HIGH/CRITICAL W49** (din `imports/`, doar data; orele nu sunt în fișier): lun 30 — BoJ Ueda (JPY), PIB Canada T3 (CAD) · mar 1 — HICP flash zona euro (EUR), ISM manufacturing + JOLTS (USD, XAU), Bullock RBA (AUD) · mie 2 — PIB Australia T3 (AUD), CPI Elveția (CHF) · joi 3 — ISM services (USD) · vin 4 — NFP (USD, XAU), LFS Canada (CAD). Prima știre CRITICAL: RBA marți 8 dec (în afara săptămânii).

### Cu context clar

**1. EURUSD — short, pro-trend, pro-fundamental** (bearish, medium; EUR 0 vs USD +7) — FSB complet, până vineri 23:00
- Daily: swing, internal și fractal bearish. Prețul e în discount-ul fractalului Daily, dar premium-ul a fost vizitat în pullback-ul din 24–27 nov (supply-ul D 1.09532–1.101015), deci sell-urile din discount sunt permise (2b-A2). Veto HTF: D complet bearish + 4H swing bearish → **fără long-uri**.
- 4H: swing, internal și fractal bearish; supply-ul 4H 1.09532–1.100585 e atins de 5× (zonă consumată, nu mai e „puternică”).
- 1H: totul bearish; vineri 19:00 fractalul 1H s-a întors în jos și a lăsat **supply 1H proaspăt 1.093405–1.09553** (rafinat 1.094965–1.09553). Sub preț: demand 1H proaspăt 1.089635–1.090585, apoi minimul de luni 1.088115 (BOS fractal D).
- Validare: revenire în 1.09497–1.09553, respingere și închidere 1H înapoi sub 1.0936 → ținte 1.0906–1.0896, apoi 1.088115.
- Anulare: închidere 4H peste 1.100585 (CHoCH fractal 4H); închidere Daily peste 1.101015 = începe pullback-ul Daily.
- Fundamental: „it is hard to outrun a central bank that still has two hikes on its mind”. Riscuri: HICP marți (≥ 3.9% ajută EUR), NFP vineri. Fractalul Daily e deja în discount → continuarea e mai riscantă (2b-A4).

**2. NZDUSD — short, pro-trend, pro-fundamental** (bearish, medium) — FSB până vineri 10:00 + (ta)
- Daily: swing, internal și fractal bearish (FSB); supply-ul D 0.548225–0.553375 atins de 7× (slab, dar a ținut toată săptămâna). 4H: swing și internal bearish, fractalul 4H în pullback bullish de marți (FSB); (ta) H4 sus, CHoCH 0.54951.
- Vineri 21:00 (ta) prețul a luat din nou minimul săptămânii trecute (0.54657) și a fost respins → lichiditate luată sub preț, deci un pullback mai sus e posibil întâi.
- Zona de urmărit: supply 4H proaspăt 0.5487–0.54951 (ta), în interiorul supply-ului D.
- Validare: respingere din 0.5487–0.5495, apoi închidere 4H sub 0.54636 (ta) / sub 0.54559 (CHoCH fractal 4H, FSB) → ținta minimul de luni 0.543325 (FSB).
- Anulare: închidere Daily peste 0.553375 (CHoCH fractal D, FSB).
- Riscuri: prețul e în discount adânc (5% din range-ul de 3 luni, ta); China PMI luni și GDT marți (MEDIUM), ISM marți, NFP vineri.

**3. GBPUSD — short, pro-fundamental, clasă cel mult B spre A** (bearish, low; GBP +3 vs USD +7) — FSB până vineri 10:00 + (ta)
- Daily: swing, internal și fractal bearish (FSB). 4H: **swing bullish (contra)**, internal și fractal bearish → HTF > LTF, dar „B spre A” (2b-I).
- Zona: supply 4H 1.311145–1.314395 (FSB, atins de 5× — slab) / 1.31149–1.31442 (ta), la 0.2 ATR de preț; equal highs 1.31291 (ta) = lichiditate chiar sub zonă.
- Validare: lichiditatea 1.3129 luată + respingere din 1.3115–1.3144 + închidere 4H sub 1.30921 (minimul zilei, ta) → ținta minimul de luni 1.301075 (FSB).
- Anulare: închidere 4H peste 1.314395 (CHoCH fractal 4H, FSB).
- Fundamental: „the Bank of England talks tough, but the Fed talks tough with a 4.3% growth number behind it”. Știri: PMI UK marți (MEDIUM), ISM, NFP.

**4. GBPNZD — long, pro-trend, pro-fundamental** (bullish, medium; GBP +3 vs NZD −3) — doar (ta)
- Daily sus (BOS 2.38248), H4 în pullback jos (CHoCH 2.38728); prețul în premium-ul range-ului de 3 luni (86%).
- Zona: demand 4H 2.37927–2.38334 (atins o dată), la 1 ATR; equal lows 2.38794 deasupra lui = lichiditate de luat înainte.
- Validare: închidere 4H peste 2.39995 (ta) = pullback-ul s-a terminat; ideal după ce lichiditatea 2.38794 e luată și prețul revine din demand.
- Anulare (interpretarea mea): închidere 4H sub 2.37927 = demand-ul pierdut.

**5. EURGBP — short, pro-trend, pro-fundamental** (bearish, low; EUR 0 vs GBP +3) — doar (ta)
- D1 și H4 jos (aliniate); vineri range 2.1× ATR 4H, net −1.7×. Zona: supply 4H proaspăt 0.83642–0.83681, la 0.6 ATR; equal highs 0.83529 luate și respinse vineri.
- Validare: respingere din 0.8364–0.8368. Anulare: închidere Daily peste 0.8393 (ultimul swing D1, ta).
- Risc: discount adânc (10% din range-ul de 3 luni). HICP marți.

**6. CADJPY — short, pro-fundamental, pullback** (bearish, low; CAD −6 vs JPY 0) — doar (ta)
- D1 jos, H4 sus (pullback); vineri a luat maximul săptămânii trecute 112.005 și a fost respins. Supply 4H 112.134–112.27 (atins), la 0.2 ATR.
- Validare: închidere 4H sub 111.612 (ta). Anulare (interpretarea mea): acceptare peste 112.27.
- ⚠ CAD a fost cea mai puternică monedă în W48 (CADJPY +1.1σ contra biasului). Știri: Ueda și PIB Canada luni, LFS vineri.

**7. USDCHF — long, pro-trend, pro-fundamental, după confirmare** (bullish, low; USD +7 vs CHF −1) — FSB până vineri 10:00 + (ta)
- Daily: swing, internal și fractal bullish (FSB); demand-ul D proaspăt 0.813285–0.83133 a fost atins miercuri și a reacționat. 4H: swing bullish, internal și fractal în pullback bearish.
- Prețul e în supply-ul 4H 0.834395–0.837135 (FSB, atins de 4×) / 0.83534–0.8365 (ta).
- Validare: închidere 4H peste 0.83713 (CHoCH fractal 4H FSB 0.837135 / ta 0.83712) → ținta 0.844425 (BOS internal D = maximul săptămânii trecute).
- Anulare: închidere Daily sub 0.828545 (minimul săptămânii).
- ⚠ CHF a fost a doua cea mai puternică în W48. CPI Elveția miercuri.

**8. USDCAD — long doar după confirmare** (bullish, low; USD +7 vs CAD −6) — FSB până vineri 10:00 + (ta)
- Daily: swing și internal bullish, dar **fractalul Daily s-a întors în jos pe 25 nov cu închidere** → pullback Daily în curs (2b-A3). 4H: swing bullish, internal și fractal bearish.
- Validare: închidere 4H peste 1.42617 (ta) și menținere peste 1.41901 (minimul săptămânii, BOS fractal D) → abia atunci contextul de long revine.
- Anulare: închidere Daily sub 1.41901.
- Contra: CAD cea mai puternică monedă W48. PIB Canada luni, OPEC+ duminică (MEDIUM), LFS + NFP vineri.

**9. CADCHF și NZDJPY — short pe pullback** (bearish, low) — doar (ta)
- CADCHF: D1 jos, H4 sus; supply 4H proaspăt 0.59033–0.59057 (0.9 ATR). Validare: închidere 4H sub 0.58059.
- NZDJPY: D1 jos, H4 sus; supply 4H proaspăt 88.285–88.478 (1.3 ATR). Validare: închidere 4H sub 86.792.

**10. EURNZD — long pe pullback** (bullish, low) — doar (ta): D1 sus, H4 jos; demand 4H 1.99297–1.9962 (atins), la 0.5 ATR. Validare: închidere 4H peste 2.00899.

### Fără idee
- **USDJPY** — conflict: Daily complet bearish și 4H swing bearish (FSB) vs fundamental bullish medium; prețul în supply-ul D 155.2285–160.394. Ideea de long (pro-fundamental) apare doar la o închidere Daily peste 160.394 (CHoCH internal/fractal D). Ueda luni.
- **AUDUSD** — fractalul Daily e la limită (pos 111, supply-ul D invalidat vineri), 4H întors în sus; fundamental bearish low. Aștept închiderea Daily: peste 0.66649 = pullback Daily; (ta) închidere 4H sub 0.65617 = reluarea scăderii.
- **EURCAD, GBPCAD, AUDCAD, NZDCAD, AUDCHF, AUDNZD** — fundamental bullish, dar D1 și H4 jos (ta) → veto HTF pe long-uri, iar short-urile ar fi contra fundamentalului.
- **GBPJPY, AUDJPY, GBPCHF** — bullish low, H4 s-a întors sus, dar D1 încă jos (ta); niveluri de urmărit: 209.486 / 106.556 / 1.0979.
- **EURAUD** — bearish low, H4 s-a întors jos, dar D1 încă sus (ta).
- **EURJPY, EURCHF, NZDCHF** — tehnic D1 și H4 jos (ta), dar fundamental two-sided → fără pilonul fundamental.
- **GBPAUD, CHFJPY, XAUUSD** — two-sided și structuri D1/H4 opuse sau fără FSB.
