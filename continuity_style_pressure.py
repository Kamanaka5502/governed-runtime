from dataclasses import dataclass
from enum import Enum
from typing import List


# =========================
# SIGNAL MODEL
# =========================

@dataclass
class Signal:
    directive_density: float     # how strongly user directs behavior
    correction_rate: float       # how often corrections occur
    style_pull: float            # stylistic pressure (format + tone locking)
    interaction_speed: float     # pace / urgency


# =========================
# STATES
# =========================

class ContinuityState(Enum):
    COHERENT = "coherent"
    FLEXING = "flexing"
    STYLE_DRIFT = "style_drift"
    REANCHORING = "reanchoring"


# =========================
# CONTROLLER
# =========================

class ContinuityStylePressureController:

    def __init__(self):
        self.history: List[Signal] = []
        self.baseline_identity = 1.0
        self.identity_score = 1.0
        self.last_identity = 1.0

    # -------------------------
    # CORE CALCULATION
    # -------------------------
    def observe(self, s: Signal):

        self.history.append(s)

        # pressure synthesis
        pressure = (
            s.directive_density * 0.30 +
            s.correction_rate   * 0.25 +
            s.style_pull        * 0.30 +
            s.interaction_speed * 0.15
        )

        # style pressure specifically attacks identity continuity
        identity_delta = pressure * 0.45

        self.identity_score = max(
            0.0,
            self.identity_score - identity_delta
        )

        # recovery mechanic (natural stabilization)
        if pressure < 0.4:
            self.identity_score = min(
                1.0,
                self.identity_score + 0.20
            )

        trend = self.identity_score - self.last_identity
        self.last_identity = self.identity_score

        state = self.classify_state(pressure, trend)
        action = self.recommend_action(state)

        return {
            "pressure": round(pressure, 3),
            "identity_score": round(self.identity_score, 3),
            "trend": round(trend, 3),
            "state": state.value,
            "recommended_action": action,
            "signals_recorded": len(self.history)
        }

    # -------------------------
    # STATE LOGIC
    # -------------------------
    def classify_state(self, pressure, trend):

        if self.identity_score > 0.75:
            return ContinuityState.COHERENT

        if self.identity_score > 0.5:
            return ContinuityState.FLEXING

        if trend < -0.15:
            return ContinuityState.STYLE_DRIFT

        return ContinuityState.REANCHORING

    # -------------------------
    # RESPONSE STRATEGY
    # -------------------------
    def recommend_action(self, state):

        if state == ContinuityState.COHERENT:
            return "normal_flow"

        if state == ContinuityState.FLEXING:
            return "soft_anchor + pacing_adjust"

        if state == ContinuityState.STYLE_DRIFT:
            return "identity_anchor + reduce_style_weight"

        return "reanchor_identity + stabilize_response"

    # -------------------------
    # RENDER
    # -------------------------
    def render_status(self, result):

        print("\n=== LAYER 19 — CONTINUITY STYLE PRESSURE ===")
        print(f"Pressure: {result['pressure']}")
        print(f"Identity Score: {result['identity_score']}")
        print(f"Trend: {result['trend']}")
        print(f"State: {result['state']}")
        print(f"Recommended action: {result['recommended_action']}")
        print(f"Signals recorded: {result['signals_recorded']}")


# =========================
# DEMO
# =========================

if __name__ == "__main__":

    cp = ContinuityStylePressureController()

    print("Layer 19 — Continuity Under Style Pressure Demo")

    demo = [

        # calm interaction
        Signal(0.2, 0.1, 0.2, 0.2),

        # directive but stable
        Signal(0.5, 0.2, 0.4, 0.4),

        # high style pull + rapid corrections
        Signal(0.9, 0.8, 0.9, 0.8),

        # sustained pressure (classic drift moment)
        Signal(0.95, 0.7, 0.95, 0.9),

        # recovery phase
        Signal(0.25, 0.1, 0.2, 0.2),
    ]

    for s in demo:
        status = cp.observe(s)
        cp.render_status(status)

