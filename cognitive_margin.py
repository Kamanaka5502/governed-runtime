# cognitive_margin.py
#
# Layer 13: Cognitive Margin Governance
#
# Detects operator saturation and protects interaction integrity.

import time
from dataclasses import dataclass
from typing import List


@dataclass
class MarginEvent:
    ts: int
    action: str
    pressure_score: float
    checkpoint_created: bool


class CognitiveMarginGovernor:
    """
    Monitors interaction entropy and detects saturation.

    This layer DOES NOT control AI behavior.
    It governs interaction pacing.
    """

    def __init__(self):
        self.history: List[MarginEvent] = []
        self.pressure = 0.0

        # thresholds
        self.warn_threshold = 0.60
        self.saturation_threshold = 0.80
        self.reset_decay = 0.10

    def record_action(self, action: str):
        """
        Record a new interaction event.
        Pressure increases with rapid activity.
        """

        now = time.time_ns()

        # decay pressure slightly (recovery over time)
        self.pressure = max(0.0, self.pressure - self.reset_decay)

        # increase pressure
        self.pressure += 0.25
        self.pressure = min(self.pressure, 1.0)

        checkpoint = False

        # automatic checkpoint near saturation
        if self.pressure >= self.saturation_threshold:
            checkpoint = True

        event = MarginEvent(
            ts=now,
            action=action,
            pressure_score=self.pressure,
            checkpoint_created=checkpoint,
        )

        self.history.append(event)

        return event

    def status(self) -> str:
        """Return current cognitive margin state."""
        if self.pressure < self.warn_threshold:
            return "stable"
        elif self.pressure < self.saturation_threshold:
            return "warning"
        else:
            return "saturated"

    def render(self):
        print("\n=== COGNITIVE MARGIN STATUS ===")
        print(f"Pressure: {self.pressure:.2f}")
        print(f"State: {self.status()}")
        print(f"Events: {len(self.history)}")

        if self.status() == "warning":
            print("⚠️  Margin narrowing. Consider checkpointing.")
        elif self.status() == "saturated":
            print("🛑 Saturation detected. Pause recommended.")

        print("===============================\n")


if __name__ == "__main__":

    gov = CognitiveMarginGovernor()

    print("Layer 13 — Cognitive Margin Demo\n")

    actions = [
        "state_transition",
        "commit",
        "commit",
        "verification",
        "rewrite",
        "rewrite",
        "rewrite",
    ]

    for a in actions:
        evt = gov.record_action(a)
        print(
            f"{a} | pressure={evt.pressure_score:.2f} "
            f"| checkpoint={evt.checkpoint_created}"
        )

    gov.render()
