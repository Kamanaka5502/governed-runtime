# adaptive_stabilization_memory.py

import time
from enum import Enum


class BandwidthState(Enum):
    STABLE = "stable"
    RISING = "rising"
    HIGH = "high"
    SATURATED = "saturated"


class AdaptiveStabilizationMemory:
    """
    Layer 13.5:
    Adds hysteresis and cooldown memory to stabilization bandwidth.
    Prevents oscillation near thresholds.
    """

    def __init__(self):
        self.last_state = BandwidthState.STABLE
        self.last_transition_time = time.time()
        self.cooldown_seconds = 5
        self.saturation_penalty = 0.1
        self.dynamic_adjustment = 0.0

    def adjust_threshold(self, base_threshold: float) -> float:
        """
        After saturation, temporarily reduce allowable threshold
        to increase margin.
        """
        if self.last_state == BandwidthState.SATURATED:
            return max(0.0, base_threshold - self.saturation_penalty)
        return base_threshold

    def update_state(self, new_state: BandwidthState):
        now = time.time()

        # Prevent rapid flipping during cooldown
        if now - self.last_transition_time < self.cooldown_seconds:
            return self.last_state

        if new_state != self.last_state:
            self.last_transition_time = now
            self.last_state = new_state

        return self.last_state

    def render(self):
        print("\n=== ADAPTIVE STABILIZATION MEMORY ===")
        print(f"Current state: {self.last_state.value}")
        print(f"Cooldown remaining: "
              f"{max(0, self.cooldown_seconds - (time.time() - self.last_transition_time)):.2f}s")


# Demo
if __name__ == "__main__":
    asm = AdaptiveStabilizationMemory()

    print("Layer 13.5 — Hysteresis Demo")

    asm.update_state(BandwidthState.SATURATED)
    asm.render()

    time.sleep(2)

    # Attempt rapid state change
    asm.update_state(BandwidthState.STABLE)
    asm.render()

    time.sleep(5)

    # Now transition allowed
    asm.update_state(BandwidthState.STABLE)
    asm.render()

