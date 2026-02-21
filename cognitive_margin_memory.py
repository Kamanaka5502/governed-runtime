from dataclasses import dataclass, field
from enum import Enum
from typing import List


# =========================
# STATES
# =========================

class BandwidthState(Enum):
    STABLE = "stable"
    PRESSURED = "pressured"
    SATURATED = "saturated"


# =========================
# SIGNAL MODEL
# =========================

@dataclass
class Signal:
    directive_density: float
    correction_rate: float
    response_fragmentation: float
    interaction_speed: float

    def intensity(self) -> float:
        # weighted pressure score
        return (
            self.directive_density * 0.30 +
            self.correction_rate * 0.25 +
            self.response_fragmentation * 0.20 +
            self.interaction_speed * 0.25
        )


# =========================
# COGNITIVE MARGIN MEMORY
# =========================

@dataclass
class CognitiveMarginController:

    margin: float = 1.0              # 1.0 = full capacity
    decay_rate: float = 0.15         # how fast overload shrinks margin
    recovery_rate: float = 0.05      # slow recovery during calm flow

    history: List[Signal] = field(default_factory=list)
    state: BandwidthState = BandwidthState.STABLE

    # ---------- CORE ----------

    def observe(self, signal: Signal):

        pressure = signal.intensity()
        adjusted_pressure = pressure / max(self.margin, 0.05)

        # STATE TRANSITIONS
        if adjusted_pressure < 0.35:
            self.state = BandwidthState.STABLE
            self.margin = min(1.0, self.margin + self.recovery_rate)

        elif adjusted_pressure < 0.75:
            self.state = BandwidthState.PRESSURED
            self.margin = max(0.2, self.margin - (self.decay_rate * 0.4))

        else:
            self.state = BandwidthState.SATURATED
            self.margin = max(0.2, self.margin - self.decay_rate)

        self.history.append(signal)

        return adjusted_pressure

    # ---------- ACTION LOGIC ----------

    def recommended_action(self):

        if self.state == BandwidthState.STABLE:
            return "normal_flow"

        if self.state == BandwidthState.PRESSURED:
            return "soft_checkpoint + pacing_adjust"

        return "hard_checkpoint + entropy_pause"

    # ---------- DEBUG RENDER ----------

    def render_status(self, adjusted_pressure):

        print("\n=== COGNITIVE MARGIN MEMORY ===")
        print(f"State: {self.state.value}")
        print(f"Adjusted Pressure: {round(adjusted_pressure,3)}")
        print(f"Current Margin: {round(self.margin,3)}")
        print(f"Recommended action: {self.recommended_action()}")
        print(f"Signals recorded: {len(self.history)}")


# =========================
# DEMO RUN
# =========================

if __name__ == "__main__":

    print("Layer 14 — Cognitive Margin Memory Demo\n")

    cm = CognitiveMarginController()

    # calm interaction
    s1 = Signal(
        directive_density=0.2,
        correction_rate=0.1,
        response_fragmentation=0.1,
        interaction_speed=0.2,
    )
    p = cm.observe(s1)
    cm.render_status(p)

    # moderate pressure
    s2 = Signal(
        directive_density=0.6,
        correction_rate=0.5,
        response_fragmentation=0.4,
        interaction_speed=0.6,
    )
    p = cm.observe(s2)
    cm.render_status(p)

    # sustained overload
    s3 = Signal(
        directive_density=0.9,
        correction_rate=0.8,
        response_fragmentation=0.7,
        interaction_speed=0.9,
    )
    p = cm.observe(s3)
    cm.render_status(p)

    # second overload hits harder because margin reduced
    s4 = Signal(
        directive_density=0.9,
        correction_rate=0.8,
        response_fragmentation=0.7,
        interaction_speed=0.9,
    )
    p = cm.observe(s4)
    cm.render_status(p)

    # recovery phase
    s5 = Signal(
        directive_density=0.2,
        correction_rate=0.1,
        response_fragmentation=0.1,
        interaction_speed=0.2,
    )
    p = cm.observe(s5)
    cm.render_status(p)

