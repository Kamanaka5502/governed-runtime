#!/usr/bin/env python3

"""
Layer 60 — Meta Governance Core

Purpose:
    Governs the governance system itself.

This layer analyzes historical governance performance
and adjusts internal thresholds dynamically.

Key Idea:
    Governance becomes adaptive instead of static.
"""

import time
from dataclasses import dataclass
from typing import List


@dataclass
class GovernanceSnapshot:
    timestamp: float
    tension_score: float
    stabilization_used: bool
    outcome_score: float


class MetaGovernanceCore:

    def __init__(self):
        self.history: List[GovernanceSnapshot] = []

        # Initial governance thresholds
        self.low_threshold = 0.30
        self.high_threshold = 0.70

    def record_snapshot(
        self,
        tension_score: float,
        stabilization_used: bool,
        outcome_score: float,
    ):
        snap = GovernanceSnapshot(
            timestamp=time.time(),
            tension_score=tension_score,
            stabilization_used=stabilization_used,
            outcome_score=outcome_score,
        )
        self.history.append(snap)

    def evaluate(self):
        if not self.history:
            print("No governance history available.")
            return

        avg_tension = sum(s.tension_score for s in self.history) / len(self.history)
        avg_outcome = sum(s.outcome_score for s in self.history) / len(self.history)

        stabilization_rate = (
            sum(1 for s in self.history if s.stabilization_used)
            / len(self.history)
        )

        print("\n=== META GOVERNANCE EVALUATION ===")
        print(f"Average tension: {avg_tension:.2f}")
        print(f"Average outcome: {avg_outcome:.2f}")
        print(f"Stabilization usage: {stabilization_rate:.2f}")

        self._tune_thresholds(avg_tension, avg_outcome, stabilization_rate)

    def _tune_thresholds(
        self,
        avg_tension: float,
        avg_outcome: float,
        stabilization_rate: float,
    ):
        """
        Self-tuning logic:
        - Too much stabilization → thresholds too sensitive
        - Poor outcomes under high tension → thresholds too loose
        """

        if stabilization_rate > 0.70:
            self.low_threshold += 0.05
            self.high_threshold += 0.05
            action = "Raised thresholds (too sensitive)."

        elif avg_tension > 0.65 and avg_outcome < 0.50:
            self.low_threshold -= 0.05
            self.high_threshold -= 0.05
            action = "Lowered thresholds (too permissive)."

        else:
            action = "Thresholds stable."

        # Clamp values
        self.low_threshold = max(0.05, min(self.low_threshold, 0.90))
        self.high_threshold = max(self.low_threshold + 0.05,
                                  min(self.high_threshold, 0.95))

        print("\n=== META GOVERNANCE ADJUSTMENT ===")
        print(action)
        print(f"New LOW threshold: {self.low_threshold:.2f}")
        print(f"New HIGH threshold: {self.high_threshold:.2f}")


def demo():

    core = MetaGovernanceCore()

    # Simulated governance history
    core.record_snapshot(0.40, False, 0.80)
    core.record_snapshot(0.68, True, 0.55)
    core.record_snapshot(0.75, True, 0.45)
    core.record_snapshot(0.52, False, 0.72)
    core.record_snapshot(0.80, True, 0.40)

    core.evaluate()


if __name__ == "__main__":
    demo()

