# Bitcoin Multi-Horizon Prediction Framework

**A research and design document for a composite, indicator-weighted model that produces a
directional view on Bitcoin at three horizons: 1 week, 1 month, and 6 months.**

Version 1.0 · Status: Design document (not an implementation) · Horizons: 1W / 1M / 6M

---

## 0. How to read this document (and an honest warning)

You asked for a model that is correct ~80% of the time. This document is built on the premise that
**a credible model is worth more than a flattering one**, so the first thing it does is tell you the
truth about what is achievable. The rest is a concrete, rankable, weightable catalog of 120+ signals
you can actually build from.

If you only read one section, read **§1 (Reality Check)** and **§5 (Scoring)**.

---

## 1. Reality check — what accuracy is actually achievable

**Short version: sustained 80% correct directional calls — especially at the 1-week horizon — is not
realistically achievable, and any product advertising it is almost certainly overfit, cherry-picked,
or dishonest.** Here is the evidence, not an opinion:

- **Short horizons are near-efficient.** Peer-reviewed ML studies forecasting Bitcoin *direction* at
  intraday-to-daily frequency cluster at **~50–56% accuracy** for high-frequency and **~65–66% for
  daily** forecasts. Models that report 82–83% almost always use aggressive feature selection on
  small samples and show **look-ahead bias / data leakage** — their out-of-sample performance
  collapses. ([Financial Innovation, 2024](https://jfin-swufe.springeropen.com/articles/10.1186/s40854-024-00643-1); [PMC review](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10216962/))
- **On-chain signals are not short-term tools.** They "reveal long-term holder behavior and macro
  cycles, but [are] less useful for short-term day trading." Their edge shows up over **weeks to
  months**, not days. ([on-chain analytics overview](https://www.gate.com/learn/articles/overview-of-popular-btc-on-chain-indicators/5888))
- **Popular "models" are statistically broken.** Stock-to-Flow regresses a quantity largely on time,
  has "limited to no ability to predict out-of-sample," and was off by **>500% in 2024**. It is
  included in this document only in the *excluded* list (§4.K) so you understand why we don't weight
  it. ([Bitcoin Magazine](https://bitcoinmagazine.com/markets/why-bitcoin-stock-to-flow-is-not-useful); [MDPI, 2024](https://www.mdpi.com/1911-8074/17/10/443))

### Honest target accuracy bands (directional, confidence-weighted)

| Horizon | Realistic ceiling for a *disciplined* model | What it should output | Why |
|---|---|---|---|
| **1 week** | ~52–58% directional | Probability + low default confidence | Dominated by noise, leverage flushes, reflexive liquidity; barely better than a coin flip |
| **1 month** | ~58–66% directional | Probability + medium confidence | Flows (ETF/stablecoin), positioning, and macro surprises start to dominate noise |
| **6 months** | ~62–72% directional | Probability + higher confidence in clear regimes | Slow variables (global liquidity, cycle, on-chain valuation) carry real signal |

**What "80%" would actually require** (and why it's a red flag): perfect macro foresight, no regime
shifts, no exogenous shocks (regulation, exchange failures, geopolitics), and a stationary market —
none of which hold. The honest design goal is therefore **calibrated probabilities, not binary
oracles**: a model that says "65% up, medium confidence" and is *right 65% of the time when it says
65%* is far more valuable (and tradeable) than one that claims 80% and isn't.

> Throughout this document, every indicator carries an **Evidence** rating — *Strong / Moderate /
> Weak / Contextual* — and nothing is presented as a measured win-rate unless it is cited. No
> fabricated backtests appear anywhere in this document.

---

## 2. Design philosophy

1. **Composite over single-signal.** No indicator predicts Bitcoin. The model is a weighted ensemble.
2. **Horizon-specific weighting.** The drivers of next-week price (leverage, sentiment, technicals)
   are *not* the drivers of next-six-months price (liquidity, cycle, valuation). The same indicator
   gets **three different weights**.
3. **Regime-awareness.** Weights and confidence are modulated by the prevailing regime (bull / bear /
   chop / high-volatility), because correlations are unstable across regimes.
4. **Probabilistic output.** Output is a directional score *and* a confidence band — never a bare
   yes/no.
5. **Evidence-gated.** Weak/contested signals get small or zero weight and are labeled as such.
6. **Anti-redundancy.** Many indicators are collinear (e.g., MVRV vs. NUPL). The model down-weights
   correlated clusters so it doesn't "double-count" one underlying factor.

---

## 3. Indicator taxonomy (overview)

| # | Category | Code | What it captures | Primarily drives |
|---|---|---|---|---|
| A | On-chain valuation & holder behavior | ONCH | Over/undervaluation, holder conviction | 1M, 6M |
| B | Miner metrics | MINE | Supply-side stress & capitulation | 1M, 6M |
| C | Derivatives & market structure | DERIV | Leverage, positioning, fragility | 1W, 1M |
| D | Exchange flows & liquidity | FLOW | Buy/sell pressure, fiat on-ramp | 1W, 1M |
| E | Technical | TECH | Trend, momentum, mean-reversion | 1W, 1M |
| F | Sentiment & social | SENT | Crowd positioning (often contrarian) | 1W |
| G | Global macro & liquidity | MACRO | Risk appetite & monetary tide | 1M, 6M |
| H | Regional economies | REGN | US/China/EU/Japan/India drivers | 1M, 6M |
| I | Cross-asset & crypto structure | XASSET | Correlation regime, rotation | 1W, 1M |
| J | Cycle / reflexivity / fundamental | CYCLE | Halving cycle, adoption | 6M |
| K | **Excluded** (low validity) | — | Documented for transparency | none |

---

## 4. The indicator catalog (120+ signals)

**Column key:** *Source* = where data comes from · *Freq* = update frequency · *Bullish when* =
direction that pushes the sub-score positive · *Hz* = horizons where it carries meaningful weight
(W=week, M=month, 6=6-month) · *Ev* = evidence strength.

### A. On-chain valuation & holder behavior (ONCH)

| # | Indicator | What it measures | Source | Freq | Bullish when | Hz | Ev |
|---|---|---|---|---|---|---|---|
| 1 | MVRV Ratio | Market value vs. realized (cost-basis) value | Glassnode, CoinMetrics | Daily | Low / rising off lows | M,6 | Strong |
| 2 | MVRV Z-Score | MVRV standardized; cycle top/bottom gauge | Glassnode | Daily | Deeply negative/low | M,6 | Strong |
| 3 | Realized Price | Aggregate on-chain cost basis | Glassnode, CoinMetrics | Daily | Price reclaims it | M,6 | Strong |
| 4 | Realized Cap | Capital actually stored in BTC | CoinMetrics | Daily | Rising (inflows) | M,6 | Strong |
| 5 | SOPR (adjusted) | Profit/loss ratio of spent coins | Glassnode | Daily | Resets to 1 then rises in uptrend | M | Moderate |
| 6 | STH-SOPR | Short-term holder realized P/L | Glassnode | Daily | <1 capitulation then recovery | W,M | Moderate |
| 7 | LTH-SOPR | Long-term holder realized P/L | Glassnode | Daily | Low (no distribution) | 6 | Moderate |
| 8 | NUPL | Net unrealized profit/loss (whole market) | Glassnode | Daily | Capitulation/Hope zone | M,6 | Strong |
| 9 | LTH-NUPL | Conviction of long-term holders | Glassnode | Daily | Low, accumulating | 6 | Moderate |
| 10 | Puell Multiple | Miner revenue vs. 1-yr avg | Glassnode | Daily | Low (miner stress bottoms) | 6 | Moderate |
| 11 | Reserve Risk | Conviction vs. price (HODLer confidence) | Glassnode | Daily | Low | 6 | Moderate |
| 12 | Dormancy / CDD | Age of coins being moved | Glassnode | Daily | Low (old coins dormant) | M,6 | Moderate |
| 13 | RHODL Ratio | Realized value of young vs. old coins | Glassnode | Daily | Low | 6 | Moderate |
| 14 | LTH Supply | Coins held >155 days | Glassnode | Daily | Rising (accumulation) | M,6 | Strong |
| 15 | STH Supply | Coins held <155 days | Glassnode | Daily | Falling (coins maturing) | M | Moderate |
| 16 | Supply in Profit % | Share of supply in profit | Glassnode | Daily | Very low (washout) | M,6 | Moderate |
| 17 | NVT Ratio | Network value vs. transaction volume | CoinMetrics | Daily | Low | M | Weak |
| 18 | NVT Signal (NVTS) | Smoothed NVT | CoinMetrics | Daily | Low | M | Weak |
| 19 | Mayer Multiple | Price / 200-day MA | bitbo, derived | Daily | <1 (undervalued) | M,6 | Moderate |
| 20 | Thermocap ratio | Mkt cap / cumulative miner revenue | Glassnode | Daily | Low | 6 | Moderate |
| 21 | Active Addresses | Daily active network participants | CoinMetrics | Daily | Rising trend | M | Moderate |
| 22 | New Addresses | Network adoption growth | CoinMetrics | Daily | Rising trend | M,6 | Moderate |
| 23 | Adjusted Tx Volume | Real economic throughput | CoinMetrics | Daily | Rising | M | Weak |
| 24 | Realized P/L ratio | Realized profit vs. loss flow | Glassnode | Daily | Loss-dominated washout | M | Moderate |

### B. Miner metrics (MINE)

| # | Indicator | What it measures | Source | Freq | Bullish when | Hz | Ev |
|---|---|---|---|---|---|---|---|
| 25 | Hash Rate | Total network compute | blockchain.com, CoinMetrics | Daily | Rising/recovering | M,6 | Moderate |
| 26 | Mining Difficulty | Difficulty adjustment trend | blockchain.com | ~2 wks | Rising | 6 | Weak |
| 27 | Difficulty Ribbon | Difficulty MAs compression | Glassnode | Daily | Compression then expansion | 6 | Moderate |
| 28 | Hash Ribbons | Miner capitulation/recovery (MA cross) | Glassnode | Daily | Recovery cross | M,6 | Moderate |
| 29 | Miner Reserves | BTC held by miners | CryptoQuant | Daily | Stable/rising | M | Moderate |
| 30 | Miner Position Index (MPI) | Miner outflow vs. 1-yr avg | CryptoQuant | Daily | Low (no dumping) | M | Moderate |

### C. Derivatives & market structure (DERIV)

| # | Indicator | What it measures | Source | Freq | Bullish when | Hz | Ev |
|---|---|---|---|---|---|---|---|
| 31 | Perp Funding Rate | Cost of long leverage | Coinglass, exchange APIs | 8h | Neutral/slightly +; extreme + is bearish | W,M | Strong |
| 32 | OI-weighted Funding | Funding weighted by venue OI | Coinglass | 8h | Same; less noisy | W,M | Strong |
| 33 | Open Interest (total) | Total leverage outstanding | Coinglass | Real-time | Rising *with* price | W,M | Moderate |
| 34 | OI / Market Cap | Leverage relative to size (fragility) | Coinglass, derived | Daily | Low | W | Moderate |
| 35 | Futures Basis (annualized) | Carry / demand for leverage | Coinglass, CME | Daily | Healthy positive (not extreme) | M | Moderate |
| 36 | Term Structure | Contango vs. backwardation | Laevitas, exchange | Daily | Mild contango | M | Moderate |
| 37 | Options 25Δ Skew | Put vs. call pricing (fear/greed) | Deribit, Laevitas | Daily | Put skew washout | W,M | Moderate |
| 38 | Put/Call Ratio | Options positioning | Deribit | Daily | Extreme puts (contrarian) | W | Weak |
| 39 | Implied Vol / DVOL | Expected volatility | Deribit | Daily | Capitulation spike fading | W,M | Moderate |
| 40 | Liquidation Heatmap | Where leverage gets flushed | Coinglass | Real-time | Below-price liq cleared | W | Moderate |
| 41 | Long/Short Ratio | Retail positioning | Coinglass | Real-time | Crowd net-short (contrarian) | W | Weak |
| 42 | CME Futures Basis | Institutional leverage demand | CME, Coinglass | Daily | Healthy positive | M | Moderate |
| 43 | CME Gap | Weekend price gap (often fills) | TradingView | Weekly | Gap below acts as magnet | W | Weak |
| 44 | Coinbase Premium | US spot demand vs. offshore | CryptoQuant | Real-time | Positive (US buying) | W,M | Moderate |
| 45 | Perp-Spot Premium | Derivatives lead vs. spot | Coinglass | Real-time | Spot-led rallies healthier | W | Moderate |

### D. Exchange flows & liquidity (FLOW)

| # | Indicator | What it measures | Source | Freq | Bullish when | Hz | Ev |
|---|---|---|---|---|---|---|---|
| 46 | Exchange Net Flows | BTC in vs. out of exchanges | CryptoQuant, Glassnode | Daily | Net outflows (self-custody) | M | Moderate |
| 47 | Exchange Reserves | BTC sitting on exchanges | CryptoQuant | Daily | Falling | M,6 | Moderate |
| 48 | Whale Exchange Inflows | Large deposits (sell intent) | CryptoQuant | Real-time | Absent | W,M | Moderate |
| 49 | Stablecoin Total Supply | Dry powder on-chain | CoinMetrics, DefiLlama | Daily | Expanding | M,6 | Moderate |
| 50 | Stablecoin Supply Δ | Rate of stablecoin minting | DefiLlama | Daily | Positive | M | Moderate |
| 51 | Stablecoin Supply Ratio (SSR) | BTC cap vs. stablecoin cap | Glassnode | Daily | Low (more buying power) | M | Moderate |
| 52 | USDT Issuance | Tether mint/burn | Tether, on-chain | Real-time | Minting | M | Moderate |
| 53 | USDC Issuance | Circle mint/burn | Circle, on-chain | Real-time | Minting | M | Moderate |
| 54 | **Spot BTC ETF Net Flows** | US institutional demand | Farside, Coinglass, theblock | Daily | Sustained inflows | M,6 | Strong* |
| 55 | Spot ETF Cumulative Holdings | Structural ownership | Farside, Glassnode | Daily | Rising | 6 | Strong* |
| 56 | Realized Cap Netflow | Net capital entering/leaving | Glassnode | Daily | Positive | M | Moderate |

\* *Strong since Jan 2024 only — see §6 caveat on short ETF history. In 2024 ~$35B and 2025 ~$34B
flowed into US crypto ETFs (IBIT alone ~$25B in 2025); inflow/outflow swings now track price closely,
but the dataset is barely two years long.* ([etf.com](https://www.etf.com/sections/features/34-billion-entered-crypto-etfs-2025-investors-still-lost); [Farside](https://farside.co.uk/btc/))

### E. Technical (TECH)

| # | Indicator | What it measures | Source | Freq | Bullish when | Hz | Ev |
|---|---|---|---|---|---|---|---|
| 57 | 200-Week MA | Long-term cycle floor | TradingView | Weekly | Price holds above | 6 | Moderate |
| 58 | 200-Day MA | Primary trend | TradingView | Daily | Price above & MA rising | M | Moderate |
| 59 | 50/200-Day Cross | Golden/Death cross | TradingView | Daily | Golden cross | M | Weak |
| 60 | 21-Week EMA | Bull-market support band | TradingView | Weekly | Price holds above | M,6 | Moderate |
| 61 | RSI (Daily) | Short-term momentum | TradingView | Daily | Oversold turning up | W | Moderate |
| 62 | RSI (Weekly) | Cycle momentum | TradingView | Weekly | Rising from <40 | M,6 | Moderate |
| 63 | MACD | Trend/momentum cross | TradingView | Daily/Weekly | Bullish cross | W,M | Weak |
| 64 | Bollinger Band Width | Volatility compression | TradingView | Daily | Squeeze before expansion | W | Weak |
| 65 | Ichimoku Cloud | Trend/support system | TradingView | Daily | Price above cloud | M | Weak |
| 66 | Realized Volatility (30d) | Actual recent vol | derived | Daily | Low base before trend | W,M | Moderate |
| 67 | ATR | Volatility / stop sizing | TradingView | Daily | (risk context) | W | Contextual |
| 68 | Volume / VWAP | Participation & fair value | TradingView | Daily | Rising vol on up moves | W,M | Moderate |
| 69 | Pi Cycle Top | Cycle-top timing (111/350 MA) | bitbo | Daily | Far from trigger | 6 | Weak |
| 70 | Market Structure | Higher-highs/higher-lows | manual/derived | Daily | Uptrend structure intact | W,M | Moderate |
| 71 | Key S/R Levels | Supply/demand zones | derived | Daily | Reclaim of resistance | W,M | Moderate |

### F. Sentiment & social (SENT) — *mostly contrarian at extremes*

| # | Indicator | What it measures | Source | Freq | Bullish when | Hz | Ev |
|---|---|---|---|---|---|---|---|
| 72 | Crypto Fear & Greed | Composite sentiment 0–100 | alternative.me | Daily | Extreme Fear (contrarian) | W,M | Moderate |
| 73 | Positioning Sentiment | Funding/skew-implied crowd lean | Coinglass/Deribit | Real-time | Crowd fearful | W | Moderate |
| 74 | Social Volume | Mention counts across platforms | Santiment, LunarCrush | Daily | Quiet bottoms / euphoric tops | W | Weak |
| 75 | Google Trends | Public search interest | Google Trends | Daily/Weekly | Rising from low base | M | Weak |
| 76 | X / Twitter Sentiment | NLP sentiment of posts | LunarCrush, Santiment | Real-time | Capitulation (contrarian) | W | Weak |
| 77 | Reddit Sentiment/Volume | Forum tone & activity | Reddit API/NLP | Daily | Capitulation (contrarian) | W | Weak |
| 78 | App Store Rank (Coinbase) | Retail onboarding proxy | App stores | Daily | Rising = late-cycle caution | M | Weak |
| 79 | Retail/Institutional Mix | Who is driving flow | CryptoQuant proxies | Daily | Institutional-led | M | Weak |
| 80 | News/Regulatory Tone | Headline sentiment | NLP feeds | Daily | Positive catalysts | W,M | Contextual |

### G. Global macro & liquidity (MACRO)

| # | Indicator | What it measures | Source | Freq | Bullish when | Hz | Ev |
|---|---|---|---|---|---|---|---|
| 81 | **Global M2** | World money supply (lead ~70–90d) | central banks, BM Pro | Weekly/Monthly | Expanding (lagged) | 6 | Moderate† |
| 82 | US Net Liquidity | Fed BS − RRP − TGA | FRED, derived | Weekly | Rising | M,6 | Moderate† |
| 83 | Fed Balance Sheet | QE/QT stance | FRED | Weekly | Expanding/QT ending | 6 | Moderate |
| 84 | Reverse Repo (RRP) | Drained = liquidity to markets | FRED | Daily | Falling | M | Moderate |
| 85 | Treasury General Acct | TGA build drains liquidity | FRED | Daily | Falling/spending | M | Moderate |
| 86 | DXY (Dollar Index) | USD strength | FRED, TradingView | Daily | Falling | M,6 | Moderate |
| 87 | US 2Y Yield | Rate-path expectations | FRED | Daily | Falling (easing priced) | M | Moderate |
| 88 | US 10Y Yield | Long-end / discount rate | FRED | Daily | Stable/falling | M,6 | Moderate |
| 89 | Real Yields (10Y TIPS) | Inflation-adjusted rate | FRED | Daily | Falling | M,6 | Moderate |
| 90 | Yield Curve (2s10s) | Cycle/recession signal | FRED | Daily | Re-steepening from inversion | 6 | Weak |
| 91 | MOVE Index | Bond-market volatility | ICE/TradingView | Daily | Falling (calm) | M | Moderate |
| 92 | VIX | Equity volatility / risk-off | CBOE/FRED | Daily | Low/falling | W,M | Moderate |
| 93 | Financial Conditions Index | Aggregate ease/tightness | Chicago Fed (NFCI) | Weekly | Loosening | M,6 | Moderate |
| 94 | HY Credit Spreads | Risk appetite / stress | FRED (BAML OAS) | Daily | Tightening | M,6 | Moderate |
| 95 | Gold | Debasement / safe-haven bid | TradingView | Daily | Rising (debasement narrative) | 6 | Weak |
| 96 | Crude Oil | Inflation/growth input | TradingView | Daily | (context) | M | Contextual |
| 97 | Copper | Global growth proxy | TradingView | Daily | Rising (risk-on) | M | Weak |

† *The Bitcoin–M2/net-liquidity relationship is real but unstable: a ~70–90 day lag is well
documented, yet it "fractured" in 2023–2025 partly due to TGA/Treasury operations. Treat as a tide,
not a trigger.* ([CFB](https://www.cfbenchmarks.com/blog/the-m2-bitcoin-relationship-what-the-data-actually-shows); [Macro Mechanics](https://pierce-pierce.ghost.io/macro-mechanics-5-global-m2-the-liquidity-lag/))

### H. Regional economies (REGN)

| # | Indicator | What it measures | Source | Freq | Bullish when | Hz | Ev |
|---|---|---|---|---|---|---|---|
| 98 | Fed Funds Rate-Path | Cuts/hikes priced (FF futures) | CME FedWatch | Daily | Cuts being priced | M,6 | Moderate |
| 99 | US CPI / Inflation Surprise | Inflation vs. expectations | BLS, FRED | Monthly | Cooling (eases policy) | M | Moderate |
| 100 | US NFP / Labor | Jobs vs. expectations | BLS | Monthly | Goldilocks (soft, not crashing) | M | Weak |
| 101 | US ISM / PMI | Growth momentum | ISM, S&P | Monthly | Re-accelerating from trough | M,6 | Weak |
| 102 | China PBOC Liquidity | RRR/MLF/OMO injections | PBOC | Irregular | Easing/injecting | M,6 | Weak |
| 103 | USD/CNY & Capital Flows | Yuan stress / capital flight | FRED, TradingView | Daily | Stable CNY / capital seeking BTC | M | Weak |
| 104 | China Credit Impulse | Credit-driven global growth | derived/research | Monthly | Rising | 6 | Weak |
| 105 | ECB Policy / EUR | Eurozone monetary stance | ECB, FRED | Per-meeting | Easing | M | Weak |
| 106 | BoJ Policy / JGB Yields | Yen carry conditions | BoJ, FRED | Per-meeting | Stable (no carry unwind) | M,6 | Moderate |
| 107 | USD/JPY (Carry Stress) | Yen-carry unwind risk | TradingView | Daily | Stable; sharp JPY strength = risk-off | W,M | Moderate |
| 108 | India Regulation/Tax & Adoption | Policy & EM demand | news/research | Irregular | Favorable shifts | 6 | Weak |
| 109 | EM Risk Appetite / FX | Emerging-market risk-on | MSCI EM, FX | Daily | Risk-on | M | Weak |

### I. Cross-asset & crypto structure (XASSET)

| # | Indicator | What it measures | Source | Freq | Bullish when | Hz | Ev |
|---|---|---|---|---|---|---|---|
| 110 | BTC–Nasdaq/S&P Correlation | Risk-asset coupling | derived | Daily | Decoupling up / equities strong | W,M | Moderate |
| 111 | BTC–Gold Correlation | Safe-haven narrative | derived | Daily | Positive in debasement regime | M,6 | Weak |
| 112 | BTC Dominance | BTC share of crypto cap | TradingView | Daily | Rising in risk-off; falling = alt risk-on | M | Moderate |
| 113 | Total Crypto Market Cap | Asset-class capital | TradingView | Daily | Rising | M,6 | Moderate |
| 114 | ETH/BTC Ratio | Risk appetite within crypto | TradingView | Daily | Rising = risk-on | M | Weak |
| 115 | Altcoin Season Index | Rotation breadth | blockchaincenter | Daily | Late-cycle caution when extreme | M | Weak |
| 116 | TOTAL2 / TOTAL3 | Cap ex-BTC / ex-BTC&ETH | TradingView | Daily | Healthy breadth | M | Weak |

### J. Cycle / reflexivity / fundamental (CYCLE)

| # | Indicator | What it measures | Source | Freq | Bullish when | Hz | Ev |
|---|---|---|---|---|---|---|---|
| 117 | Halving Cycle Position | Days since last halving | derived | Daily | 6–18 months post-halving | 6 | Moderate‡ |
| 118 | Drawdown from ATH | Cyclical positioning | derived | Daily | Deep drawdown (value) | 6 | Moderate |
| 119 | Realized-Cap Cycle Position | Cost-basis cycle stage | Glassnode | Daily | Early-cycle | 6 | Moderate |
| 120 | Institutional/Treasury Adoption | Corporate & sovereign holdings trend | bitcointreasuries, filings | Irregular | Accelerating accumulation | 6 | Moderate |
| 121 | Regulatory Catalysts | ETF options, accounting (FASB), policy | news/research | Irregular | Favorable rulings | M,6 | Contextual |
| 122 | Network Fundamentals | Lightning capacity, fees, security budget | various | Weekly | Healthy growth | 6 | Weak |
| 123 | Macro Catalyst Calendar | Scheduled events (FOMC, CPI, options expiry) | calendars | — | (risk timing) | W | Contextual |

‡ *The 4-year halving cycle has only ~3–4 observations and is partly self-fulfilling narrative. Use
as a soft prior, not a hard rule — see §6.*

### K. Excluded from scoring (documented for transparency)

These are popular but lack robust out-of-sample predictive validity. **They are listed so you know we
deliberately do *not* weight them**, not because they belong in the model:

| Signal | Why excluded |
|---|---|
| **Stock-to-Flow (S2F)** | Spurious regression of value largely on time; no out-of-sample power; off >500% in 2024. ([source](https://www.mdpi.com/1911-8074/17/10/443)) |
| **Rainbow Chart** | A log regression band fitted to past price; descriptive, not predictive. |
| **Naive Metcalfe price targets** | Sensitive to specification; weak out-of-sample. |
| **"Price oracle" log-regression models** | Curve-fit to history; break on regime change. |

---

## 5. Scoring methodology

### 5.1 Per-indicator sub-score

Each indicator `i` is normalized to a sub-score `sᵢ ∈ [−100, +100]`:

- **Z-score normalization** against its own trailing window (e.g., 1–4 years), then squashed to
  ±100 via `tanh`, **or**
- **Percentile/threshold mapping** for bounded indicators (e.g., RSI, Fear & Greed), **or**
- **Rule-based** for event/regime indicators (e.g., golden cross = +X).

Positive = bullish for the relevant horizon. **Contrarian indicators are inverted** (extreme greed →
negative sub-score).

### 5.2 Horizon-specific category weights

Indicators contribute through their category. **Category weights differ per horizon** and sum to 100%:

| Category | 1-Week | 1-Month | 6-Month |
|---|---:|---:|---:|
| C — Derivatives (DERIV) | 25% | 12% | 4% |
| E — Technical (TECH) | 20% | 12% | 5% |
| F — Sentiment (SENT) | 15% | 8% | 3% |
| D — Flows/Liquidity (FLOW) | 12% | 20% | 15% |
| A — On-chain (ONCH) | 8% | 18% | 20% |
| G+H — Macro + Regional (MACRO/REGN) | 12% | 18% | 26% |
| I — Cross-asset (XASSET) | 8% | 8% | 6% |
| B — Miners (MINE) | 0% | 2% | 5% |
| J — Cycle (CYCLE) | 0% | 2% | 16% |
| **Total** | **100%** | **100%** | **100%** |

*Rationale:* weekly leans on leverage/positioning/technicals/sentiment (the things that actually move
price over days); the 6-month view is dominated by the monetary tide, on-chain valuation, and cycle
position. These are **starting weights to be calibrated** (§7), not gospel.

Within a category, each indicator gets an **intra-category share** (default: equal-weight, then
tilt toward *Strong*-evidence indicators and **down-weight collinear clusters** — e.g., MVRV, MVRV-Z,
NUPL share one "valuation" budget rather than counting three times).

### 5.3 Composite score

For horizon `h`:

```
RawScoreₕ = Σ  Wₕ(category) × ( Σ  share(i) × sᵢ )
           categories        i ∈ category

CompositeₕRegime  =  RawScoreₕ × RegimeMultiplierₕ        (multiplier ∈ ~0.6–1.0, lowers
                                                           confidence/size in chop & high-vol)
```

### 5.4 Regime detection (gate, not a signal)

A lightweight classifier tags the current regime from: 200-day MA slope, realized volatility,
BTC–equity correlation, and trend structure → {Bull, Bear, Chop, High-Vol}. The regime:
- **re-weights** categories (e.g., in high-vol risk-off, MACRO and DERIV-fragility dominate),
- **scales confidence** (chop and high-vol → wider bands, smaller conviction).

### 5.5 Output (per horizon)

```
Direction   : Up / Down / Neutral   (sign of Composite, Neutral if |Composite| < deadband)
Conviction  : |Composite| → 0–100
Probability : calibrated P(up) from Composite via isotonic/Platt calibration on backtest
Confidence  : f(Conviction, Regime, signal agreement, data freshness)
Drivers     : top +/− contributing indicators (for explainability)
```

**Example (illustrative, not a measured result):**
> *6-Month: P(up) ≈ 64%, Conviction 41/100, Confidence Medium. Top bullish drivers: rising US net
> liquidity, ETF inflows, MVRV-Z off lows. Top bearish: stretched weekly RSI, elevated funding.*

---

## 6. Honest limitations & failure modes

1. **Short data history for the best modern signals.** Spot ETF flows (the strongest recent driver)
   only exist since **Jan 2024** — barely two years. Any weight is fit on a tiny sample.
2. **Regime instability.** BTC's correlation to equities, gold, and DXY flips between regimes. A model
   tuned on one regime degrades in the next. This is the #1 reason naive backtests overstate accuracy.
3. **Reflexivity & overfitting.** With 120+ inputs it is trivial to overfit. Guardrails: out-of-sample
   /walk-forward validation, collinearity pruning, capping the number of effective free parameters.
4. **Exogenous shocks dominate short horizons.** Exchange failures (FTX), regulation, hacks, ETF
   approvals, and geopolitics routinely override every indicator for days–weeks. No indicator set
   predicts these; they are why the 1-week ceiling is ~55%.
5. **The halving "cycle" has n≈3.** Treat it as a weak prior, not a law. It may already be weakening
   as ETFs/institutions reshape the marginal buyer.
6. **Macro lags are variable.** The M2/liquidity lead time wanders (≈70–90d historically) and has
   recently broken down due to Treasury operations. Don't hard-code a lag.
7. **Garbage-in risk.** On-chain metrics depend on the provider's clustering heuristics (entity
   adjustment) and differ between Glassnode/CryptoQuant/CoinMetrics. Pin one provider's methodology.
8. **Survivorship in "what works."** Indicators that look great in hindsight are selected *because*
   they fit history. The Evidence ratings here flag this; verify before trusting.

### "Don't trust it until" checklist
- [ ] Walk-forward / out-of-sample test across ≥2 distinct regimes (bull, bear).
- [ ] Probability **calibration** check (a 60% call should be right ~60% of the time).
- [ ] Compare against dumb baselines (always-up, momentum, buy-and-hold) — beat them *net of cost*.
- [ ] Stress-test on shock windows (Mar-2020, May-2021, FTX Nov-2022).
- [ ] Confirm no look-ahead bias (point-in-time data; lag macro releases to publication dates).

---

## 7. Calibration approach (kept high-level — implementation is Phase 2)

The weights in §5.2 are **priors**, not answers. To set them honestly:
1. Assemble point-in-time history per indicator (respect publication lags).
2. Walk-forward optimize category/indicator weights per horizon, **regularized** to prevent overfit.
3. Calibrate the score→probability mapping (isotonic/Platt) on out-of-sample folds.
4. Re-estimate periodically; monitor for regime drift and decay.

A reasonable build order: **(1) data ingestion → (2) per-indicator normalization → (3) composite +
regime gate → (4) calibration & backtest → (5) monitoring.** Detailed implementation is intentionally
out of scope for this document.

---

## 8. Appendix — data sources

| Source | Covers | Free / Paid |
|---|---|---|
| **FRED** (St. Louis Fed) | Macro: rates, M2, Fed BS, RRP, TGA, spreads, DXY | Free |
| **CoinMetrics** (community) | On-chain basics, realized cap, addresses | Free tier |
| **Glassnode** | Full on-chain suite (MVRV-Z, NUPL, SOPR, ETF) | Mostly paid |
| **CryptoQuant** | Exchange flows, miner metrics, premiums | Free/paid |
| **Coinglass** | Funding, OI, liquidations, ETF flows | Free/paid |
| **Deribit / Laevitas** | Options skew, IV/DVOL, term structure | Free/paid |
| **Farside / theblock / Coinglass** | Spot BTC ETF flows | Free |
| **TradingView** | Price, technicals, cross-asset | Free/paid |
| **Santiment / LunarCrush** | Social volume & sentiment | Free/paid |
| **alternative.me** | Crypto Fear & Greed Index | Free |
| **CME FedWatch** | Rate-path probabilities | Free |
| **Google Trends** | Search interest | Free |

---

## 9. One-paragraph summary

This framework scores 120+ evidence-rated indicators across on-chain, derivatives, flows, technicals,
sentiment, macro, regional economies, cross-asset, and cycle categories, combining them with
**horizon-specific weights** and a **regime gate** into a **calibrated probability** for 1-week,
1-month, and 6-month direction. It is explicitly designed to be honest about its ceiling: roughly
**55% / 60–66% / 65–72%** directional accuracy at the three horizons in favorable conditions — useful
and tradeable, but **not the 80% oracle that no credible system can deliver**. Its value comes from
calibration, explainability, and discipline, not from a magic number.

---

### Sources
- [Deep learning for Bitcoin price direction prediction — Financial Innovation (2024)](https://jfin-swufe.springeropen.com/articles/10.1186/s40854-024-00643-1)
- [Predicting Bitcoin Prices Using ML — review (PMC)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10216962/)
- [Overview of popular BTC on-chain indicators — Gate Learn](https://www.gate.com/learn/articles/overview-of-popular-btc-on-chain-indicators/5888)
- [Why the Bitcoin Stock-to-Flow model is not useful — Bitcoin Magazine](https://bitcoinmagazine.com/markets/why-bitcoin-stock-to-flow-is-not-useful)
- [Bitcoin Return Prediction (S2F, Metcalfe, TA, sentiment) — MDPI (2024)](https://www.mdpi.com/1911-8074/17/10/443)
- [The M2–Bitcoin relationship: what the data shows — CFB](https://www.cfbenchmarks.com/blog/the-m2-bitcoin-relationship-what-the-data-actually-shows)
- [Global M2 & the liquidity lag — Macro Mechanics](https://pierce-pierce.ghost.io/macro-mechanics-5-global-m2-the-liquidity-lag/)
- [$34B entered crypto ETFs in 2025 — etf.com](https://www.etf.com/sections/features/34-billion-entered-crypto-etfs-2025-investors-still-lost)
- [Bitcoin ETF flow data — Farside Investors](https://farside.co.uk/btc/)
- [How to interpret funding, OI, liquidations — Gate Wiki](https://www.gate.com/crypto-wiki/article/how-to-interpret-crypto-derivatives-market-signals-funding-rates-open-interest-and-liquidation-data-explained-20251227)
