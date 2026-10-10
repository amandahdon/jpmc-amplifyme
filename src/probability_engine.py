"""
Probability and Expected Value calculation engine.
Calculates P(Bullseye), P(Partial), P(Miss), Expected Return (EV), and Return Variance.
Uses pure-Python math functions (erf, Poisson PMF) for maximum portability and zero latency.
"""

import math
from dataclasses import dataclass
from typing import Dict, List

from src.config import QuestionConfig, QUESTIONS_CONFIG
from src.models import ForecastResult, get_all_forecasts


@dataclass
class QuestionProbabilities:
    config: QuestionConfig
    forecast: ForecastResult
    p_bullseye: float
    p_partial: float
    p_miss: float
    expected_net_return: float  # EV per coin staked
    return_variance: float      # Variance of return per coin staked
    sharpe_ratio: float         # EV / std_dev
    recommended_confidence: int # 0 to 100 slider value


def normal_cdf(z: float) -> float:
    """Standard normal cumulative distribution function Phi(z)."""
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def poisson_pmf(k: int, lam: float) -> float:
    """Poisson probability mass function P(X = k) for parameter lam."""
    if k < 0:
        return 0.0
    return math.exp(-lam + k * math.log(lam) - math.lgamma(k + 1.0))


def compute_question_probabilities(
    config: QuestionConfig, forecast: ForecastResult
) -> QuestionProbabilities:
    """
    Computes exact probabilities of Bullseye, Partial, and Miss,
    along with EV and risk metrics.
    """
    if forecast.dist_type == "poisson":
        lam = forecast.point_forecast
        center_k = int(round(lam))
        
        # Bullseye is exact match (tolerance 0)
        p_bullseye = poisson_pmf(center_k, lam)
        
        # Partial is within tolerance (e.g. +- 3) excluding exact match
        p_partial = 0.0
        tol = int(config.partial_tolerance)
        for offset in range(-tol, tol + 1):
            if offset != 0:
                p_partial += poisson_pmf(center_k + offset, lam)
                
        p_miss = max(0.0, 1.0 - p_bullseye - p_partial)
    else:
        sigma = forecast.std_err
        
        # Bullseye: [ -delta_B, +delta_B ]
        if config.bullseye_tolerance > 0:
            z_b = config.bullseye_tolerance / sigma
            p_bullseye = max(0.0, 2.0 * normal_cdf(z_b) - 1.0)
        else:
            p_bullseye = 0.0
            
        # Total payout range (Bullseye + Partial): [ -delta_P, +delta_P ]
        z_p = config.partial_tolerance / sigma
        p_total_win = max(0.0, 2.0 * normal_cdf(z_p) - 1.0)
        
        p_partial = max(0.0, p_total_win - p_bullseye)
        p_miss = max(0.0, 1.0 - p_bullseye - p_partial)

    # Net returns per unit staked
    net_bullseye = config.bullseye_multiplier - 1.0
    net_partial = config.partial_multiplier - 1.0
    net_miss = -1.0

    ev = (
        p_bullseye * net_bullseye
        + p_partial * net_partial
        + p_miss * net_miss
    )

    e_r2 = (
        p_bullseye * (net_bullseye ** 2)
        + p_partial * (net_partial ** 2)
        + p_miss * (net_miss ** 2)
    )
    variance = max(1e-6, e_r2 - (ev ** 2))
    std_dev = math.sqrt(variance)
    sharpe = ev / std_dev if std_dev > 0 else 0.0

    # Calibrated confidence slider score: weighted chance of success
    # Bullseye counts 100%, Partial counts 60%
    raw_confidence = (p_bullseye * 100.0) + (p_partial * 60.0)
    recommended_confidence = int(round(min(98.0, max(25.0, raw_confidence))))

    return QuestionProbabilities(
        config=config,
        forecast=forecast,
        p_bullseye=p_bullseye,
        p_partial=p_partial,
        p_miss=p_miss,
        expected_net_return=ev,
        return_variance=variance,
        sharpe_ratio=sharpe,
        recommended_confidence=recommended_confidence,
    )


def evaluate_all_questions() -> List[QuestionProbabilities]:
    """Evaluates probabilities and metrics for all 10 questions."""
    forecasts = get_all_forecasts()
    results = []
    for cfg in QUESTIONS_CONFIG:
        fc = forecasts[cfg.id]
        results.append(compute_question_probabilities(cfg, fc))
    return results

