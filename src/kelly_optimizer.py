"""
Constrained Portfolio Kelly Optimizer for JPMC AmplifyMe.
Maximizes expected log-wealth growth under strict portfolio constraints:
- Total bankroll = 10,000 coins (100% utilized)
- Individual stake bounds: 250 <= stake_i <= 2,500
- Integer coin allocations (via Largest Remainder Method)
"""

import math
from typing import List, Tuple
import numpy as np
from scipy.optimize import minimize

from src.config import TOTAL_ROUND_BANKROLL, MIN_STAKE_DEFAULT, MAX_STAKE_DEFAULT
from src.probability_engine import QuestionProbabilities


def optimize_portfolio_kelly(
    evaluations: List[QuestionProbabilities],
    total_bankroll: int = TOTAL_ROUND_BANKROLL,
    min_stake: int = MIN_STAKE_DEFAULT,
    max_stake: int = MAX_STAKE_DEFAULT,
) -> List[int]:
    """
    Finds the optimal integer coin allocation [s_1, ..., s_10]
    maximizing multi-asset expected log-utility subject to:
    sum(s_i) == total_bankroll and min_stake <= s_i <= max_stake.
    """
    n = len(evaluations)
    assert n == 10, f"Expected 10 questions, got {n}"
    assert n * min_stake <= total_bankroll <= n * max_stake, "Constraints are infeasible"

    # Gather parameters for each question
    p_b = np.array([e.p_bullseye for e in evaluations])
    p_p = np.array([e.p_partial for e in evaluations])
    p_m = np.array([e.p_miss for e in evaluations])
    
    r_b = np.array([e.config.bullseye_multiplier - 1.0 for e in evaluations])
    r_p = np.array([e.config.partial_multiplier - 1.0 for e in evaluations])
    r_m = np.array([-1.0 for _ in evaluations])

    w_total = float(total_bankroll)

    # Objective: Negative expected log-utility (we minimize negative utility)
    # E[log(1 + (s_i / W) * R_i)]
    def objective(s: np.ndarray) -> float:
        total_util = 0.0
        for i in range(n):
            # fraction of total bankroll
            f = s[i] / w_total
            # Payout terms
            term_b = max(1e-12, 1.0 + f * r_b[i])
            term_p = max(1e-12, 1.0 + f * r_p[i])
            term_m = max(1e-12, 1.0 + f * r_m[i])
            
            e_log = (
                p_b[i] * math.log(term_b)
                + p_p[i] * math.log(term_p)
                + p_m[i] * math.log(term_m)
            )
            total_util += e_log
        return -total_util  # minimize negative utility

    # Initial guess: distribute proportionally to positive Kelly edge
    # Edge_i = EV_i / Var_i
    evs = np.array([e.expected_net_return for e in evaluations])
    vars_ = np.array([e.return_variance for e in evaluations])
    edges = np.maximum(0.0, evs / np.maximum(1e-4, vars_))

    if edges.sum() > 0:
        base_weights = edges / edges.sum()
        s0 = min_stake + base_weights * (w_total - n * min_stake)
    else:
        s0 = np.full(n, w_total / n)

    # Clip s0 to bounds
    s0 = np.clip(s0, min_stake, max_stake)
    s0 = s0 * (w_total / s0.sum())

    # Bounds: [min_stake, max_stake] for each question
    bounds = [(float(min_stake), float(max_stake)) for _ in range(n)]

    # Constraint: sum(s_i) == total_bankroll
    constraints = [
        {"type": "eq", "fun": lambda s: np.sum(s) - w_total}
    ]

    res = minimize(
        objective,
        s0,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={"maxiter": 500, "ftol": 1e-9},
    )

    if res.success:
        s_continuous = res.x
    else:
        # Fallback to analytical edge-weighted water-filling
        s_continuous = s0

    # Ensure continuous bounds and sum
    s_continuous = np.clip(s_continuous, min_stake, max_stake)
    s_continuous = s_continuous * (w_total / s_continuous.sum())

    # Discretize to exact integers using Largest Remainder Method
    s_int = np.floor(s_continuous).astype(int)
    # Ensure min stake constraint is respected
    s_int = np.maximum(min_stake, s_int)
    
    remainder = int(total_bankroll - np.sum(s_int))

    if remainder > 0:
        fractions = s_continuous - s_int
        # Sort indices by largest fractional part, provided they haven't reached max_stake
        sorted_indices = np.argsort(-fractions)
        for idx in sorted_indices:
            if remainder <= 0:
                break
            if s_int[idx] < max_stake:
                s_int[idx] += 1
                remainder -= 1

    elif remainder < 0:
        # If floor sum exceeded (e.g. from min_stake adjustment), subtract from lowest edge above min_stake
        sorted_indices = np.argsort(edges)
        for idx in sorted_indices:
            if remainder >= 0:
                break
            can_subtract = s_int[idx] - min_stake
            sub = min(can_subtract, -remainder)
            s_int[idx] -= sub
            remainder += sub

    # Final verification
    assert np.sum(s_int) == total_bankroll, f"Sum {np.sum(s_int)} != {total_bankroll}"
    for i, stake in enumerate(s_int):
        assert min_stake <= stake <= max_stake, f"Q{i+1} stake {stake} outside bounds"

    return s_int.tolist()

