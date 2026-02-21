# layer50_pressure_projection.py
# Layer 50 — Pressure Projection + Delta Tracking
#
# Purpose:
# Track pressure change over time and project future trend.
# This gives governance foresight instead of only reacting.

from dataclasses import dataclass
from typing import List
import statistics


@dataclass
class PressureSample:
    timestamp: int
    pressure: float


class PressureProjection:
    def __init__(self):
        self.samples: List[PressureSample] = []

    def add_sample(self, timestamp: int, pressure: float):
        self.samples.append(PressureSample(timestamp, pressure))

    def delta(self):
        """Return latest pressure change."""
        if len(self.samples) < 2:
            return 0.0
        return self.samples[-1].pressure - self.samples[-2].pressure

    def velocity(self):
        """Average pressure change over all samples."""
        if len(self.samples) < 2:
            return 0.0

        deltas = []
        for i in range(1, len(self.samples)):
            deltas.append(
                self.samples[i].pressure - self.samples[i - 1].pressure
            )

        return statistics.mean(deltas)

    def projected_pressure(self, steps=3):
        """
        Simple linear projection.
        Not magic — deterministic trend extension.
        """
        v = self.velocity()
        current = self.samples[-1].pressure if self.samples else 0.0
        return current + (v * steps)

    def state(self):
        d = self.delta()

        if d > 0.15:
            return "RISING"
        elif d < -0.15:
            return "FALLING"
        else:
            return "STABLE"


def demo():
    p = PressureProjection()

    # Simulated pressure timeline
    p.add_sample(1, 0.20)
    p.add_sample(2, 0.35)
    p.add_sample(3, 0.48)
    p.add_sample(4, 0.63)
    p.add_sample(5, 0.70)

    print("\n=== LAYER 50: PRESSURE PROJECTION ===")
    print(f"Latest Delta: {p.delta():.2f}")
    print(f"Average Velocity: {p.velocity():.2f}")
    print(f"Projected Pressure (+3): {p.projected_pressure():.2f}")
    print(f"State: {p.state()}")


if __name__ == "__main__":
    demo()
