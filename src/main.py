"""
Main execution pipeline for JPMC AmplifyMe Round 2.
Orchestrates forecasting, probability calculations, Kelly bet optimization,
and generates human-readable submission tables and JSON output.
"""

import json
import os
from typing import List, Dict, Any

from src.config import TOTAL_ROUND_BANKROLL, MIN_STAKE_DEFAULT, MAX_STAKE_DEFAULT
from src.probability_engine import evaluate_all_questions, QuestionProbabilities
from src.kelly_optimizer import optimize_portfolio_kelly


def run_pipeline() -> Dict[str, Any]:
    print("=" * 90)
    print("      JPMC AMPLIFYME MARKET MIND CHALLENGE - ROUND 2 PIPELINE")
    print("=" * 90)

    # 1. Evaluate probabilities & EVs
    evaluations: List[QuestionProbabilities] = evaluate_all_questions()

    # 2. Optimize coin allocations using Constrained Portfolio Kelly
    optimal_stakes: List[int] = optimize_portfolio_kelly(
        evaluations,
        total_bankroll=TOTAL_ROUND_BANKROLL,
        min_stake=MIN_STAKE_DEFAULT,
        max_stake=MAX_STAKE_DEFAULT,
    )

    # 3. Assemble results
    table_rows = []
    total_expected_payout = 0.0

    print("\n" + "=" * 90)
    print(f"{'Q#':<4} | {'Question Name':<28} | {'Forecast':<9} | {'Stake':<8} | {'Conf':<5} | {'P(Bull)':<8} | {'P(Part)':<8} | {'EV':<6}")
    print("-" * 90)

    results_data = []

    for i, (eval_item, stake) in enumerate(zip(evaluations, optimal_stakes)):
        cfg = eval_item.config
        fc = eval_item.forecast
        
        # Expected gross payout from this question
        # Gross return = 1 + Net return
        expected_gross_return = 1.0 + eval_item.expected_net_return
        expected_coins = stake * expected_gross_return
        total_expected_payout += expected_coins

        row_str = (
            f"Q{cfg.id:<2} | {cfg.name:<28} | {fc.formatted_value:<9} | "
            f"{stake:>5} c | {eval_item.recommended_confidence:>3}% | "
            f"{eval_item.p_bullseye*100:>6.1f}% | {eval_item.p_partial*100:>6.1f}% | "
            f"{eval_item.expected_net_return:>+5.2f}"
        )
        print(row_str)

        results_data.append({
            "question_id": cfg.id,
            "name": cfg.name,
            "forecast_raw": fc.point_forecast,
            "forecast_formatted": fc.formatted_value,
            "stake_coins": stake,
            "confidence_slider": eval_item.recommended_confidence,
            "p_bullseye": round(eval_item.p_bullseye, 4),
            "p_partial": round(eval_item.p_partial, 4),
            "p_miss": round(eval_item.p_miss, 4),
            "expected_net_return": round(eval_item.expected_net_return, 4),
            "expected_coins_payout": round(expected_coins, 2),
            "rationale": fc.rationale,
        })

    print("-" * 90)
    total_staked = sum(optimal_stakes)
    net_expected_profit = total_expected_payout - total_staked
    roi_pct = (net_expected_profit / total_staked) * 100.0

    print(f"TOTAL COINS STAKED:       {total_staked:,} / {TOTAL_ROUND_BANKROLL:,} coins")
    print(f"TOTAL EXPECTED PAYOUT:    {total_expected_payout:,.1f} coins")
    print(f"EXPECTED NET PROFIT:      {net_expected_profit:+,.1f} coins ({roi_pct:+.1f}% ROI)")
    print("=" * 90)

    # 4. Save results to output directory
    os.makedirs("output", exist_ok=True)
    
    output_summary = {
        "round": 2,
        "total_bankroll": TOTAL_ROUND_BANKROLL,
        "total_staked": total_staked,
        "total_expected_payout": round(total_expected_payout, 2),
        "expected_net_profit": round(net_expected_profit, 2),
        "expected_roi_percent": round(roi_pct, 2),
        "questions": results_data,
    }

    with open("output/predictions_round2.json", "w") as f:
        json.dump(output_summary, f, indent=2)

    # Generate Markdown Summary
    md_content = generate_markdown_report(output_summary)
    with open("output/round2_submission_guide.md", "w") as f:
        f.write(md_content)

    print("\nSaved predictions to output/predictions_round2.json")
    print("Saved submission guide to output/round2_submission_guide.md")

    return output_summary


def generate_markdown_report(summary: Dict[str, Any]) -> str:
    lines = [
        "# JPMC AmplifyMe Market Mind Challenge - Round 2 Submission Guide",
        "",
        "## Summary Overview",
        f"- **Total Staked**: {summary['total_staked']:,} / {summary['total_bankroll']:,} coins (100% utilized)",
        f"- **Expected Total Payout**: {summary['total_expected_payout']:,} coins",
        f"- **Expected Net Profit**: {summary['expected_net_profit']:+,} coins ({summary['expected_roi_percent']:+.1f}% ROI)",
        "",
        "## Exact Values to Enter into UI",
        "",
        "| Q# | Event / Question | Forecast to Enter | Coin Stake | Confidence Slider | P(Bullseye) | P(Partial) | EV |",
        "|---|---|---|---|---|---|---|---|",
    ]

    for q in summary["questions"]:
        lines.append(
            f"| **Q{q['question_id']}** | {q['name']} | `{q['forecast_formatted']}` | "
            f"**{q['stake_coins']:,}** | {q['confidence_slider']}% | "
            f"{q['p_bullseye']*100:.1f}% | {q['p_partial']*100:.1f}% | {q['expected_net_return']:+.2f} |"
        )

    lines.extend([
        "",
        "## Model Rationales per Question",
        "",
    ])

    for q in summary["questions"]:
        lines.extend([
            f"### Q{q['question_id']}: {q['name']}",
            f"- **Value to Submit**: `{q['forecast_formatted']}`",
            f"- **Optimal Stake**: {q['stake_coins']} coins",
            f"- **Confidence Score**: {q['confidence_slider']}",
            f"- **Analysis & Rationale**: {q['rationale']}",
            "",
        ])

    return "\n".join(lines)


if __name__ == "__main__":
    run_pipeline()

