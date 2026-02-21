from dataclasses import dataclass
from enum import Enum


# =============================
# STATES
# =============================

class MarginState(Enum):
    STABLE = "stable"
    PRESSURED = "pressured"
    SATURATED = "saturated"


# =============================
# SIGNAL MODEL
# =============================

@dataclass
class Signal:
    directive_density: float
    correction_rate: float
    response_fragmentation: float
    interaction_speed: float


# =============================
# LAYER 15 — STABILIZATION FEEDBACK
# =============================

class StabilizationFeedbackController:

    def __init__(self):
        self.margin = 1.0
        self.history = []
        self.pacing_modifier = 1.0
        self.fragmentation_modifier = 1.0

    # -------------------------
    # PRESSURE MODEL
    # -------------------------

    def compute_pressure(self, s: Signal):
        return (
            s.directive_density * 0.35 +
            s.correction_rate * 0.25 +
            s.response_fragmentation * 0.20 +
            s.interaction_speed * 0.20
        )

    # -------------------------
    # STATE MODEL
    # -------------------------

    def determine_state(self, adjusted_pressure):

        if adjusted_pressure < 0.45:
            return MarginState.STABLE

        if adjusted_pressure < 0.85:
            return MarginState.PRESSURED

        return MarginState.SATURATED

    # -------------------------
    # MEMORY ADJUSTMENT
    # -------------------------

    def update_margin(self, state):

        if state == MarginState.STABLE:
            self.margin = min(1.0, self.margin + 0.05)

        elif state == MarginState.PRESSURED:
            self.margin = max(0.5, self.margin - 0.08)

        elif state == MarginState.SATURATED:
            self.margin = max(0.35, self.margin - 0.15)

    # -------------------------
    # FEEDBACK LOOP (NEW)
    # -------------------------

    def apply_feedback(self, state):

        if state == MarginState.STABLE:
            self.pacing_modifier = 1.0
            self.fragmentation_modifier = 1.0

        elif state == MarginState.PRESSURED:
            # subtle slowing + coherence boost
            self.pacing_modifier = 0.85
            self.fragmentation_modifier = 0.8

        elif state == MarginState.SATURATED:
            # hard stabilization feedback
            self.pacing_modifier = 0.65
            self.fragmentation_modifier = 0.6

    # -------------------------
    # OBSERVE
    # -------------------------

    def observe(self, signal: Signal):

        raw_pressure = self.compute_pressure(signal)

        adjusted_pressure = raw_pressure / self.margin

        state = self.determine_state(adjusted_pressure)

        self.update_margin(state)

        self.apply_feedback(state)

        result = {
            "state": state.value,
            "raw_pressure": round(raw_pressure, 3),
            "adjusted_pressure": round(adjusted_pressure, 3),
            "margin": round(self.margin, 3),
            "pacing_modifier": self.pacing_modifier,
            "fragmentation_modifier": self.fragmentation_modifier
        }

        self.history.append(result)

        return result

    # -------------------------
    # RENDER
    # -------------------------

    def render_status(self, result):

        print("\n=== LAYER 15 — STABILIZATION FEEDBACK LOOP ===")
        print(f"State: {result['state']}")
        print(f"Raw Pressure: {result['raw_pressure']}")
        print(f"Adjusted Pressure: {result['adjusted_pressure']}")
        print(f"Margin: {result['margin']}")
        print(f"Pacing Modifier: {result['pacing_modifier']}")
        print(f"Fragmentation Modifier: {result['fragmentation_modifier']}")
        print(f"Signals Recorded: {len(self.history)}")


# =============================
# DEMO
# =============================

if __name__ == "__main__":

    sf = StabilizationFeedbackController()

    print("Layer 15 — Stabilization Feedback Loop Demo\n")

    # normal flow
    s1 = Signal(0.2, 0.1, 0.1, 0.2)
    r = sf.observe(s1)
    sf.render_status(r)

    # moderate pressure
    s2 = Signal(0.6, 0.5, 0.3, 0.6)
    r = sf.observe(s2)
    sf.render_status(r)

    # heavy saturation
    s3 = Signal(0.9, 0.8, 0.7, 0.9)
    r = sf.observe(s3)
    sf.render_status(r)

    # recovery
    s4 = Signal(0.2, 0.1, 0.1, 0.2)
    r = sf.observe(s4)
    sf.render_status(r)
