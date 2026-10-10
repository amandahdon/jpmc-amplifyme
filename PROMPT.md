# TASK INSTRUCTION: Implement End-to-End Prediction Models & Modified Kelly Bet Sizing for JPMC AmplifyMe (Round 2)

## Background & Objective
You are an expert quantitative researcher and Python engineer. Your task is to implement the complete forecasting, probabilistic scoring, and bet sizing code for Round 2 of the JPMC AmplifyMe Market Mind Challenge.

We have **10,000 coins** that must be **100% staked** across **10 questions**.
- **Bankroll Constraint**: Sum of stakes across all 10 questions must equal exactly 10,000 coins.
- **Per-Question Bet Limits**: Each question bet must be an integer between 250 and 2,500 coins (`250 <= stake <= 2500`).
- **Target Payout Structure**:
  - Landing in **Bullseye**: Highest payout multiplier (e.g. 2.5x to 3.5x gross).
  - Landing in **Partial**: Medium payout multiplier (e.g. 1.75x to 2.25x gross).
  - Landing in **Miss**: 0 payout (100% of stake lost).

---

## The 10 Questions (Week 2 Specifications)

| # | Question / Event | Input Format | Bullseye Tolerance & Gross Return | Partial Tolerance & Gross Return | Recommended Model / Prior |
|---|---|---|---|---|---|
| **Q1** | **UK Unemployment Rate** (3 mos to August, ONS release Oct 20) | 1 decimal `%` (e.g. `4.1`) | `+-0.11%` (2.5x gross / +1.5x net) | `+-0.20%` (1.75x gross / +0.75x net) | ONS Labour Force Survey historical releases + consensus survey median (~4.1% - 4.4%). Model as Gaussian distribution around consensus. |
| **Q2** | **China Q3 GDP Growth** (YoY, NBS release Oct 19) | 1 decimal `%` (e.g. `4.6`) | `+-0.11%` (2.5x gross / +1.5x net) | `+-0.20%` (1.75x gross / +0.75x net) | NBS historical GDP quarterly series + consensus forecast (~4.5% - 4.8%). |
| **Q3** | **UK Autumn Budget OBR Fiscal Headroom** (release Oct 28) | 1 decimal in £bn (e.g. `12.5`) | `+-0.7` £bn (3.5x gross / +2.5x net) | `+-5.0` £bn (2.25x gross / +1.25x net) | OBR Spring/Autumn forecasts & IFS pre-budget analysis (historically £8bn - £25bn). High upside payout. |
| **Q4** | **US Treasury 2s10s Spread Range** (high minus low daily spread Oct 19-23) | Whole bps in `[1, 100]` (e.g. `25`) | `+-0.016%` [1.6 bps] (3.0x gross / +2.0x net) | `+-0.050%` [5.0 bps] (2.0x gross / +1.0x net) | 5-day daily par yield curve spread range volatility (historical 5-session range typically 4 to 15 bps). |
| **Q5** | **US Fed H.4.1 Treasury General Account (TGA)** (Oct 21 level, rel. Oct 22) | Integer $bn (e.g. `815`) | `+-28` $bn (2.5x gross / +1.5x net) | `+-50` $bn (1.75x gross / +0.75x net) | Daily Treasury Statement (DTS) cash balance trajectory + Fed H.4.1 series (~$750bn - $850bn). |
| **Q6** | **Count of word 'inflation'** in Fed Chair Oct 28 Opening Statement | Integer count (e.g. `14`) | `+-0` [Exact match] (3.5x gross / +2.5x net) | `+-3` (2.25x gross / +1.25x net) | Poisson/Gaussian distribution fitted to word frequency of 'inflation' across past 12 FOMC opening statements (typically 8 to 20 times). |
| **Q7** | **Brazil Presidential Election Round 2 Turnout** (Oct 25) | 2 decimals in millions (e.g. `124.35`) | `+-0.8M` (3.0x gross / +2.0x net) | `+-2.5M` (2.0x gross / +1.0x net) | Registered electorate (~155M) * historical Round 2 turnout rate (~78% - 80% ~= 122M - 125M). |
| **Q8** | **Tesla Q3 Regulatory Credits Revenue** (release Oct 21) | Integer $m (e.g. `430`) | `+-31` $m (3.0x gross / +2.0x net) | `+-100` $m (2.0x gross / +1.0x net) | Historical TSLA 10-Q/shareholder updates quarterly regulatory credit revenue trend ($350M - $890M). |
| **Q9** | **Equal-weighted 9-Currency G10 vs USD % move** (Oct 16-23) | 2 decimals `%` (e.g. `0.45` or `-0.30`) | `+-0.26%` (2.5x gross / +1.5x net) | `+-0.45%` (1.75x gross / +0.75x net) | 5-day basket return drift (~0.00%) with empirical realized volatility (sigma ~= 0.4% - 0.8%). |
| **Q10** | **UK Autumn Budget Red Book PDF page count** (release Oct 28) | Integer pages (e.g. `168`) | `+-9` pages (2.5x gross / +1.5x net) | `+-15` pages (1.75x gross / +0.75x net) | Historical HM Treasury Red Book page counts (2015-2024: mean ~150 - 180 pages, sigma ~= 18 pages). |

---

## Mathematical Formulations

### 1. Probability Engine
For each question $i$, model the outcome as distribution $Y_i \sim \mathcal{N}(\mu_i, \sigma_i^2)$ (or discrete equivalent). Given point forecast entry $\hat{y}_i = \mu_i$:
- **Bullseye Probability**:
  $$P(B_i) = 2\Phi\left(\frac{\delta_{B,i}}{\sigma_i}\right) - 1$$
- **Partial Probability**:
  $$P(P_i) = \left[2\Phi\left(\frac{\delta_{P,i}}{\sigma_i}\right) - 1\right] - P(B_i)$$
- **Miss Probability**:
  $$P(M_i) = 1 - P(B_i) - P(P_i)$$
- **Expected Return ($EV_i$)**:
  $$EV_i = P(B_i) \cdot (M_{B,i} - 1) + P(P_i) \cdot (M_{P,i} - 1) - P(M_i) \cdot 1.0$$
- **Return Variance**:
  $$\text{Var}(R_i) = P(B_i)(M_{B,i} - 1)^2 + P(P_i)(M_{P,i} - 1)^2 + P(M_i)(-1)^2 - (EV_i)^2$$

### 2. Constrained Portfolio Kelly Optimizer
Formulate and solve:
$$\max_{s} \sum_{i=1}^{10} \left( \frac{EV_i}{\text{Var}(R_i)} s_i - \frac{\lambda}{2} s_i^2 \right)$$
Subject to:
1. $\sum_{i=1}^{10} s_i = 10,000$
2. $250 \le s_i \le 2,500$ for all $i \in \{1, \dots, 10\}$
3. $s_i \in \mathbb{Z}$ (integers, resolved via largest-remainder method)
4. For any question with $EV_i \le 0$, lock stake to minimum 250 coins and redistribute remaining bankroll across positive EV bets.

---

## Project Structure to Create

Create the following files in the project directory:

```
src/
├── __init__.py
├── config.py             # Dataclass with question configs, thresholds, multipliers, constraints
├── data_sources.py       # Historical baselines, web fetching, and prior parameters for Q1-Q10
├── models.py             # Estimator classes returning point forecast, sigma, and distribution
├── probability_engine.py # Bullseye/Partial/Miss CDF calculations & EV computation
├── kelly_optimizer.py    # Bounded SLSQP / fractional Kelly integer optimization
└── main.py               # Orchestrator running all models, solver, and printing outputs
run.py                    # Top-level executable runner
```

---

## Required Final Output Format

Running `python run.py` must print a clean, clear submission table:

```
========================================================================================
                      JPMC AMPLIFYME - ROUND 2 PREDICTION SHEET
========================================================================================
Q# | Question Name        | Forecast Value | Bet (Coins) | Conf. (0-100) | P(Bull) | P(Part) | EV
----------------------------------------------------------------------------------------
Q1 | UK Unemployment Rate | 4.2%           | 1,250       | 82            | 48.2%   | 34.1%   | +0.35
...
----------------------------------------------------------------------------------------
TOTAL STAKE: 10,000 / 10,000 COINS [ALL CONSTRAINTS SATISFIED]
========================================================================================
```
Ensure all code runs without errors, uses standard libraries (`numpy`, `scipy`, `pandas`), and writes results to `output/predictions_round2.json`.
