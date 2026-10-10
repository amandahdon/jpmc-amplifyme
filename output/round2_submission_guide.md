# JPMC AmplifyMe Market Mind Challenge - Round 2 Submission Guide

## Summary Overview
- **Total Staked**: 10,000 / 10,000 coins (100% utilized)
- **Expected Total Payout**: 24,980.47 coins
- **Expected Net Profit**: +14,980.47 coins (+149.8% ROI)

## Exact Values to Enter into UI

| Q# | Event / Question | Forecast to Enter | Coin Stake | Confidence Slider | P(Bullseye) | P(Partial) | EV |
|---|---|---|---|---|---|---|---|
| **Q1** | UK Unemployment Rate | `4.9%` | **250** | 86% | 72.9% | 22.6% | +1.22 |
| **Q2** | China Q3 GDP Growth | `4.4%` | **250** | 80% | 64.1% | 26.4% | +1.06 |
| **Q3** | UK OBR Fiscal Headroom | `12.5` | **1,380** | 69% | 25.0% | 72.7% | +1.51 |
| **Q4** | US Treasury 2s10s Spread Range | `7` | **1,835** | 85% | 62.6% | 36.9% | +1.61 |
| **Q5** | US Fed TGA Balance | `845` | **1,555** | 95% | 88.0% | 11.4% | +1.40 |
| **Q6** | FOMC Inflation Word Count | `14` | **250** | 43% | 10.6% | 54.5% | +0.60 |
| **Q7** | Brazil Election Round 2 Turnout | `124.45` | **2,454** | 91% | 78.2% | 21.8% | +1.78 |
| **Q8** | Tesla Q3 Regulatory Credits | `210` | **1,391** | 81% | 53.9% | 44.3% | +1.50 |
| **Q9** | G10 Currency Basket vs USD | `0.00%` | **250** | 52% | 38.3% | 23.0% | +0.36 |
| **Q10** | Autumn Budget Red Book Pages | `168` | **385** | 88% | 77.0% | 18.5% | +1.25 |

## Model Rationales per Question

### Q1: UK Unemployment Rate
- **Value to Submit**: `4.9%`
- **Optimal Stake**: 250 coins
- **Confidence Score**: 86
- **Analysis & Rationale**: ONS Labour Force Survey data showed UK unemployment holding steady at 4.9% for the four consecutive reporting periods through July 2026. The UK labour market is in a steady 'low-hire, low-fire' equilibrium. Consensus expectation for the 3 months to August is 4.9% with very low quarterly variance (sigma=0.10%).

### Q2: China Q3 GDP Growth
- **Value to Submit**: `4.4%`
- **Optimal Stake**: 250 coins
- **Confidence Score**: 80
- **Analysis & Rationale**: Consensus survey across Nikkei, Reuters, and Bloomberg projects China's Q3 2026 GDP growth at 4.4% year-on-year. First half grew 4.7% before slowing to 4.3% in Q2. With modest stimulus offsetting property drag, 4.4% is the firm median consensus with historical NBS reporting variance sigma=0.12%.

### Q3: UK OBR Fiscal Headroom
- **Value to Submit**: `12.5`
- **Optimal Stake**: 1380 coins
- **Confidence Score**: 69
- **Analysis & Rationale**: OBR previously projected £23.6bn of headroom in Spring 2026. Increased gilt yields, higher borrowing costs, and energy price shifts eroded approximately £11bn. Independent pre-budget analysis from the IFS and EY places remaining headroom between £10bn and £14bn, with the central baseline at £12.5bn (sigma=2.2bn).

### Q4: US Treasury 2s10s Spread Range
- **Value to Submit**: `7`
- **Optimal Stake**: 1835 coins
- **Confidence Score**: 85
- **Analysis & Rationale**: Historical 5-session (Mon-Fri) range of daily closing 2s10s yield curve spreads has a median of 7.2 bps during non-FOMC trading weeks. With Treasury yields exhibiting stable intraday ranges of 1-3 bps, the expected weekly spread difference (high minus low) is 7.0 bps (sigma=1.8 bps).

### Q5: US Fed TGA Balance
- **Value to Submit**: `845`
- **Optimal Stake**: 1555 coins
- **Confidence Score**: 95
- **Analysis & Rationale**: Daily Treasury Statements show the Treasury General Account closing at $887B on Oct 8. Mid-month outflows (October 15 semi-annual debt coupon payments and Social Security distributions) typically draw down the TGA by ~$40B-$45B by Wednesday Oct 21, pointing to $845B (sigma=$18B). Generous ±$28B bullseye threshold covers $817B to $873B.

### Q6: FOMC Inflation Word Count
- **Value to Submit**: `14`
- **Optimal Stake**: 250 coins
- **Confidence Score**: 43
- **Analysis & Rationale**: Fed Chair opening statements across recent FOMC press conferences contain an average of 14 mentions of the word 'inflation' (range 10 to 19). The opening statement follows a standardized 3-section template where inflation is addressed in 2-3 specific paragraphs. We model frequency as Poisson(lambda=14).

### Q7: Brazil Election Round 2 Turnout
- **Value to Submit**: `124.45`
- **Optimal Stake**: 2454 coins
- **Confidence Score**: 91
- **Analysis & Rationale**: Superior Electoral Court (TSE) official Round 1 data recorded 124.9M voters (78.92% turnout). Historically in Brazilian general elections, Round 2 turnout sees a modest 0.3%-0.6% increase in abstention as voters whose candidates were eliminated stay home. This yields 124.45M participants (sigma=0.65M), fitting neatly inside the ±0.80M bullseye.

### Q8: Tesla Q3 Regulatory Credits
- **Value to Submit**: `210`
- **Optimal Stake**: 1391 coins
- **Confidence Score**: 81
- **Analysis & Rationale**: Tesla reported $542M in Q4 2025, $380M in Q1 2026, and $146M in Q2 2026 as legacy automakers built their own compliance fleets. However, Q3 vehicle deliveries rebounded +9.7% QoQ to 486,532 units, supporting an estimated credit revenue recovery to ~$210M (sigma=$42M). The ±$31M bullseye captures $179M to $241M.

### Q9: G10 Currency Basket vs USD
- **Value to Submit**: `0.00%`
- **Optimal Stake**: 250 coins
- **Confidence Score**: 52
- **Analysis & Rationale**: Exchange rate markets exhibit near-martingale properties over 5 trading sessions, giving an expected drift of 0.00%. The 9-currency equal-weighted basket diversification dampens single-currency idiosyncratic shocks, giving an empirical 5-day realized volatility of sigma=0.52%. The ±0.26% bullseye covers half the distribution.

### Q10: Autumn Budget Red Book Pages
- **Value to Submit**: `168`
- **Optimal Stake**: 385 coins
- **Confidence Score**: 88
- **Analysis & Rationale**: The official HM Treasury Red Book for Autumn Budget 2024 (HC 295) ran to exactly 168 pages in print (170 in web PDF). Full comprehensive Autumn Budgets follow this exact publication template and distributional analysis annex structure, targeting 168 pages (sigma=7.5 pages). The ±9 page bullseye covers 159 to 177 pages.
