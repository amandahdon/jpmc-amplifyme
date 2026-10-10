"""
Configuration definitions for JPMC AmplifyMe Market Mind Challenge (Round 2).
Specifies the exact constraints, question thresholds, and payout multipliers.
"""

from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class QuestionConfig:
    id: int
    name: str
    description: str
    unit: str
    format_spec: str
    formatter: Callable[[float], str]
    bullseye_tolerance: float  # Half-width of bullseye interval
    bullseye_multiplier: float  # Gross multiplier (e.g. 2.5 means +1.5 net profit)
    partial_tolerance: float   # Half-width of partial interval
    partial_multiplier: float   # Gross multiplier (e.g. 1.75 means +0.75 net profit)
    min_stake: int = 250
    max_stake: int = 2500


TOTAL_ROUND_BANKROLL = 10000
MIN_STAKE_DEFAULT = 250
MAX_STAKE_DEFAULT = 2500

QUESTIONS_CONFIG = [
    QuestionConfig(
        id=1,
        name="UK Unemployment Rate",
        description="Official UK unemployment rate for three months to August (ONS rel. Oct 20)",
        unit="%",
        format_spec="one decimal place (e.g. 4.7%)",
        formatter=lambda x: f"{x:.1f}%",
        bullseye_tolerance=0.11,
        bullseye_multiplier=2.50,
        partial_tolerance=0.20,
        partial_multiplier=1.75,
    ),
    QuestionConfig(
        id=2,
        name="China Q3 GDP Growth",
        description="Official year-on-year GDP growth rate for Q3 2026 (NBS rel. Oct 19)",
        unit="%",
        format_spec="one decimal place (e.g. 0.8%)",
        formatter=lambda x: f"{x:.1f}%",
        bullseye_tolerance=0.11,
        bullseye_multiplier=2.50,
        partial_tolerance=0.20,
        partial_multiplier=1.75,
    ),
    QuestionConfig(
        id=3,
        name="UK OBR Fiscal Headroom",
        description="OBR reported headroom against fiscal mandate in target year (£bn, rel. Oct 28)",
        unit="£ billions",
        format_spec="one decimal place (e.g. 12.5)",
        formatter=lambda x: f"{x:.1f}",
        bullseye_tolerance=0.70,
        bullseye_multiplier=3.50,
        partial_tolerance=5.00,
        partial_multiplier=2.25,
    ),
    QuestionConfig(
        id=4,
        name="US Treasury 2s10s Spread Range",
        description="Difference between widest and narrowest daily 2s10s spread (Oct 19-23) in bps",
        unit="bps",
        format_spec="whole number between 1 and 100 (e.g. 25)",
        formatter=lambda x: f"{int(round(x))}",
        # Payout specifies ±0.016% (1.6 bps) and ±0.050% (5.0 bps)
        bullseye_tolerance=1.60,
        bullseye_multiplier=3.00,
        partial_tolerance=5.00,
        partial_multiplier=2.00,
    ),
    QuestionConfig(
        id=5,
        name="US Fed TGA Balance",
        description="Treasury General Account balance as of Wed Oct 21 in H.4.1 ($bn, rel. Oct 22)",
        unit="$ billions",
        format_spec="nearest billion (e.g. 815)",
        formatter=lambda x: f"{int(round(x))}",
        bullseye_tolerance=28.0,
        bullseye_multiplier=2.50,
        partial_tolerance=50.0,
        partial_multiplier=1.75,
    ),
    QuestionConfig(
        id=6,
        name="FOMC Inflation Word Count",
        description="Count of word 'inflation' in Fed Chair opening statement (rel. Oct 28)",
        unit="occurrences",
        format_spec="whole number (e.g. 14)",
        formatter=lambda x: f"{int(round(x))}",
        bullseye_tolerance=0.0,   # Exact match required
        bullseye_multiplier=3.50,
        partial_tolerance=3.0,
        partial_multiplier=2.25,
    ),
    QuestionConfig(
        id=7,
        name="Brazil Election Round 2 Turnout",
        description="Total votes cast in presidential second round (millions, rel. Oct 25)",
        unit="millions",
        format_spec="millions to two decimal places (e.g. 124.35)",
        formatter=lambda x: f"{x:.2f}",
        bullseye_tolerance=0.80,
        bullseye_multiplier=3.00,
        partial_tolerance=2.50,
        partial_multiplier=2.00,
    ),
    QuestionConfig(
        id=8,
        name="Tesla Q3 Regulatory Credits",
        description="Tesla Q3 2026 automotive regulatory credits revenue ($m, rel. Oct 21)",
        unit="$ millions",
        format_spec="whole number in $ millions (e.g. 430)",
        formatter=lambda x: f"{int(round(x))}",
        bullseye_tolerance=31.0,
        bullseye_multiplier=3.00,
        partial_tolerance=100.0,
        partial_multiplier=2.00,
    ),
    QuestionConfig(
        id=9,
        name="G10 Currency Basket vs USD",
        description="Equal-weighted 9-currency G10 basket % move vs USD (5pm Oct 16 to Oct 23)",
        unit="%",
        format_spec="two decimal places (e.g. 0.45 or -0.30)",
        formatter=lambda x: f"{x:+.2f}%" if x != 0 else "0.00%",
        bullseye_tolerance=0.26,
        bullseye_multiplier=2.50,
        partial_tolerance=0.45,
        partial_multiplier=1.75,
    ),
    QuestionConfig(
        id=10,
        name="Autumn Budget Red Book Pages",
        description="Total page count of HM Treasury Autumn Budget 2026 Red Book PDF (rel. Oct 28)",
        unit="pages",
        format_spec="whole number of pages (e.g. 168)",
        formatter=lambda x: f"{int(round(x))}",
        bullseye_tolerance=9.0,
        bullseye_multiplier=2.50,
        partial_tolerance=15.0,
        partial_multiplier=1.75,
    ),
]

