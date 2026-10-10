"""Unit tests for AmplifyMe prediction & optimization pipeline."""

import unittest
from src.config import QUESTIONS_CONFIG, TOTAL_ROUND_BANKROLL, MIN_STAKE_DEFAULT, MAX_STAKE_DEFAULT
from src.models import get_all_forecasts
from src.probability_engine import evaluate_all_questions
from src.kelly_optimizer import optimize_portfolio_kelly


class TestPipeline(unittest.TestCase):
    def test_questions_config(self):
        self.assertEqual(len(QUESTIONS_CONFIG), 10)
        for q in QUESTIONS_CONFIG:
            self.assertGreaterEqual(q.partial_tolerance, q.bullseye_tolerance)
            self.assertGreater(q.bullseye_multiplier, q.partial_multiplier)
            self.assertGreater(q.partial_multiplier, 1.0)

    def test_forecasts_exist_for_all(self):
        forecasts = get_all_forecasts()
        self.assertEqual(len(forecasts), 10)
        for qid in range(1, 11):
            self.assertIn(qid, forecasts)
            self.assertIsNotNone(forecasts[qid].point_forecast)
            self.assertGreater(forecasts[qid].std_err, 0)

    def test_probability_distribution_integrity(self):
        evaluations = evaluate_all_questions()
        self.assertEqual(len(evaluations), 10)
        for item in evaluations:
            total_p = item.p_bullseye + item.p_partial + item.p_miss
            self.assertAlmostEqual(total_p, 1.0, places=4)
            self.assertGreaterEqual(item.p_bullseye, 0.0)
            self.assertGreaterEqual(item.p_partial, 0.0)
            self.assertGreaterEqual(item.p_miss, 0.0)
            self.assertTrue(0 <= item.recommended_confidence <= 100)

    def test_kelly_optimizer_constraints(self):
        evaluations = evaluate_all_questions()
        stakes = optimize_portfolio_kelly(
            evaluations,
            total_bankroll=TOTAL_ROUND_BANKROLL,
            min_stake=MIN_STAKE_DEFAULT,
            max_stake=MAX_STAKE_DEFAULT,
        )
        self.assertEqual(len(stakes), 10)
        self.assertEqual(sum(stakes), TOTAL_ROUND_BANKROLL)
        for s in stakes:
            self.assertIsInstance(s, int)
            self.assertGreaterEqual(s, MIN_STAKE_DEFAULT)
            self.assertLessEqual(s, MAX_STAKE_DEFAULT)


if __name__ == "__main__":
    unittest.main()

