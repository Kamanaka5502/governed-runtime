# layer23_resilience_boundary.py
#
# LAYER 23 — RESILIENCE BOUNDARY
# Purpose:
# Add a structural resilience layer that detects instability
# spikes and enforces controlled recovery behavior.
#
# This sits ABOVE convergence and governance layers.
# It does NOT change decisions — it governs recovery behavior.

from dataclasses import dataclass
import time


@dataclass
class ResilienceState:
    stability_score: float
    pressure_score: float
    recovery_mode: bool
    last_transition_ts: int


class ResilienceBoundary:
    """
    Layer 23:
    Detect instability trends and enforce recovery boundaries.

    Core idea:
    - Governance decides what is allowed.
    - Resilience decides HOW fast and HOW safely the system proceeds.
    """

    def __init__(self):
        self.state = ResilienceState(
            stability_score=1.0,
            pressure_score=0.0,
            recovery_mode=False,
            last_transition_ts=time.time_ns()
        )

        # Tunable thresholds
        self.stability_floor = 0.40
        self.pressure_ceiling = 0.75
        self.recovery_exit_threshold = 0.65

    def observe(self, coherence_index: float, pressure: float):
        """
        Observe signals from lower layers.
        """
        self.state.stability_score = coherence_index
        self.state.pressure_score = pressure

        self._evaluate_boundary()

    def _evaluate_boundary(self):
        """
        Determine if resilience mode must engage.
        """
        if (
            self.state.stability_score < self.stability_floor
            or self.state.pressure_score > self.pressure_ceiling
        ):
            self.state.recovery_mode = True

        elif self.state.recovery_mode and \
                self.state.stability_score > self.recovery_exit_threshold:
            self.state.recovery_mode = False

    def governance_modifier(self):
        """
        Returns recommended system pacing modifier.
        """
        if self.state.recovery_mode:
            return {
                "mode": "recovery",
                "response_pacing": "slow",
                "mutation_limit": "reduced",
                "explanation_depth": "focused"
            }

        return {
            "mode": "normal",
            "response_pacing": "standard",
            "mutation_limit": "normal",
            "explanation_depth": "normal"
        }

    def snapshot(self):
        return {
            "stability_score": self.state.stability_score,
            "pressure_score": self.state.pressure_score,
            "recovery_mode": self.state.recovery_mode
        }


if __name__ == "__main__":

    rb = ResilienceBoundary()

    print("\n=== LAYER 23 RESILIENCE TEST ===\n")

    scenarios = [
        ("stable", 0.87, 0.20),
        ("tension", 0.62, 0.50),
        ("fracture_risk", 0.35, 0.82),
        ("recovery", 0.78, 0.30),
    ]

    for name, coherence, pressure in scenarios:
        rb.observe(coherence, pressure)

        print(f"\nScenario: {name}")
        print("Signals:", rb.snapshot())
        print("Modifier:", rb.governance_modifier())

