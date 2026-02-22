# layer_growth_gate.py
# Adaptive Concurrency Growth Gate
# Determines when system maturity allows safe expansion.

import time
from dataclasses import dataclass


@dataclass
class GrowthMetrics:
    coherence_score: float          # 0.0 – 1.0
    intervention_rate: float        # 0.0 – 1.0 (lower is better)
    recovery_speed: float           # lower = faster recovery
    stable_duration: float          # seconds system has remained stable


class GrowthGate:
    """
    Governance-driven concurrency expansion.

    Growth is NOT manual.
    Growth is earned through sustained stability.
    """

    def __init__(self):
        # thresholds (tune later)
        self.coherence_threshold = 0.80
        self.intervention_threshold = 0.20
        self.recovery_threshold = 0.50
        self.duration_threshold = 10.0

        self.current_concurrency = 1
        self.max_concurrency = 8

    def should_expand(self, metrics: GrowthMetrics) -> bool:
        """
        Decide if concurrency expansion is safe.
        """

        stable = metrics.coherence_score >= self.coherence_threshold
        calm = metrics.intervention_rate <= self.intervention_threshold
        resilient = metrics.recovery_speed <= self.recovery_threshold
        sustained = metrics.stable_duration >= self.duration_threshold

        return stable and calm and resilient and sustained

    def maybe_expand(self, metrics: GrowthMetrics):
        """
        Expand concurrency only if governance allows it.
        """

        if self.should_expand(metrics):
            if self.current_concurrency < self.max_concurrency:
                self.current_concurrency += 1
                print(f"[GROWTH] Concurrency expanded → {self.current_concurrency}")
            else:
                print("[GROWTH] Already at max concurrency")
        else:
            print("[GROWTH] Expansion blocked — stability not sufficient")

    def maybe_contract(self, metrics: GrowthMetrics):
        """
        Rollback mechanism — protects coherence.
        """

        if metrics.coherence_score < 0.5:
            if self.current_concurrency > 1:
                self.current_concurrency -= 1
                print(f"[ROLLBACK] Concurrency reduced → {self.current_concurrency}")


if __name__ == "__main__":

    gate = GrowthGate()

    print("\n=== Adaptive Growth Gate Demo ===\n")

    # simulated stable conditions
    metrics_stable = GrowthMetrics(
        coherence_score=0.88,
        intervention_rate=0.10,
        recovery_speed=0.20,
        stable_duration=15.0
    )

    gate.maybe_expand(metrics_stable)

    # simulated instability
    metrics_unstable = GrowthMetrics(
        coherence_score=0.42,
        intervention_rate=0.60,
        recovery_speed=0.90,
        stable_duration=2.0
    )

    gate.maybe_contract(metrics_unstable)

    print(f"\nFinal concurrency level: {gate.current_concurrency}")
