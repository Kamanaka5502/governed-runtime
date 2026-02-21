# stabilization_bandwidth.py

import time
from dataclasses import dataclass
from enum import Enum
from typing import List


class BandwidthState(Enum):
    STABLE = "stable"
    RISING = "rising"
    HIGH = "high"
    SATURATED = "saturated"


@dataclass
class InteractionSignal:
    timestamp: int
    directive_density: float
    correction_rate: float
    response_fragmentation: float
    interaction_speed: float


class StabilizationBandwidthController:
    """
    Layer 13:
    Prevent cognitive drift under high entropy sessions.

    This layer does NOT block the user.
    It modulates pressure and introduces margin.
    """

    def __init__(self):
        self.history: List[InteractionSignal] = []
        self.state = BandwidthState.STABLE

        # Thresholds
        self.rising_threshold = 0.30
        self.high_threshold = 0.60
        self.saturation_threshold = 0.80

    # ---------- INPUT ----------

    def observe(
        self,
        directive_density: float,
        correction_rate: float,
        response_fragmentation: float,
        interaction_speed: float,
    ):

        signal = InteractionSignal(
            timestamp=time.time_ns(),
            directive_density=directive_density,
            correction_rate=correction_rate,
            response_fragmentation=response_fragmentation,
            interaction_speed=interaction_speed,
        )

        self.history.append(signal)
        self.state = self._evaluate_state(signal)

    # ---------- CORE ----------

    def _evaluate_state(self, signal: InteractionSignal) -> BandwidthState:

        load = (
            signal.directive_density * 0.30 +
            signal.correction_rate * 0.25 +
            signal.response_fragmentation * 0.25 +
            signal.interaction_speed * 0.20
        )

        if load >= self.saturation_threshold:
            return BandwidthState.SATURATED
        elif load >= self.high_threshold:
            return BandwidthState.HIGH
        elif load >= self.rising_threshold:
            return BandwidthState.RISING
        else:
            return BandwidthState.STABLE

    # ---------- OUTPUT ----------

    def stabilization_action(self) -> str:
        """
        Returns recommended stabilization behavior.
        """

        if self.state == BandwidthState.STABLE:
            return "normal_flow"

        if self.state == BandwidthState.RISING:
            return "light_structure_lock"

        if self.state == BandwidthState.HIGH:
            return "format_lock + consolidation_checkpoint"

        if self.state == BandwidthState.SATURATED:
            return "hard_checkpoint + entropy_pause"

        return "normal_flow"

    # ---------- DEBUG ----------

    def render_status(self):

        print("\n=== STABILIZATION BANDWIDTH ===")
        print(f"State: {self.state.value}")
        print(f"Recommended action: {self.stabilization_action()}")
        print(f"Signals recorded: {len(self.history)}")


# ---------------- DEMO ----------------

if __name__ == "__main__":

    sb = StabilizationBandwidthController()

    print("Layer 13 — Stabilization Bandwidth Demo\n")

    # Normal interaction
    sb.observe(
        directive_density=0.2,
        correction_rate=0.1,
        response_fragmentation=0.1,
        interaction_speed=0.2,
    )
    sb.render_status()

    # High pressure session
    sb.observe(
        directive_density=0.9,
        correction_rate=0.8,
        response_fragmentation=0.7,
        interaction_speed=0.9,
    )
    sb.render_status()

