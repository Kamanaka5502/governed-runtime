from dataclasses import dataclass
from enum import Enum


# ============================
# SIGNAL MODEL
# ============================

@dataclass
class FieldSignal:
    pressure: float
    identity_score: float
    margin: float
    style_stability: float


# ============================
# FIELD STATES
# ============================

class FieldState(Enum):
    STABLE = "stable"
    TENSION = "tension"
    FRACTURE_RISK = "fracture_risk"
    RECENTERING = "recentering"


# ============================
# CONTROLLER
# ============================

class UnifiedFieldController:

    def __init__(self):
        self.last_uci = 1.0
        self.history = []

    def compute_uci(self, s: FieldSignal):
        """
        Unified Coherence Index
        Higher = stable convergence
        """
        coherence = (
            (1 - s.pressure) * 0.30 +
            s.identity_score * 0.30 +
            s.margin * 0.20 +
            s.style_stability * 0.20
        )
        return max(0.0, min(1.0, coherence))

    def classify(self, uci, trend):

        if uci > 0.75:
            return FieldState.STABLE

        if uci > 0.55:
            return FieldState.TENSION

        if trend < -0.15:
            return FieldState.FRACTURE_RISK

        return FieldState.RECENTERING

    def recommend(self, state):

        if state == FieldState.STABLE:
            return "normal_flow"

        if state == FieldState.TENSION:
            return "soft_stabilization + pacing_adjust"

        if state == FieldState.FRACTURE_RISK:
            return "hard_anchor + reduce_style_weight + margin_restore"

        return "recenter_field + identity_anchor"

    def observe(self, s: FieldSignal):

        uci = self.compute_uci(s)
        trend = uci - self.last_uci
        self.last_uci = uci

        state = self.classify(uci, trend)
        action = self.recommend(state)

        result = {
            "uci": round(uci, 3),
            "trend": round(trend, 3),
            "state": state.value,
            "recommended_action": action,
            "signals_recorded": len(self.history) + 1
        }

        self.history.append(result)
        return result

    def render(self, r):
        print("\n=== LAYER 20 — UNIFIED FIELD CONVERGENCE ===")
        print(f"Unified Coherence Index: {r['uci']}")
        print(f"Trend: {r['trend']}")
        print(f"Field State: {r['state']}")
        print(f"Recommended action: {r['recommended_action']}")
        print(f"Signals recorded: {r['signals_recorded']}")


# ============================
# DEMO
# ============================

if __name__ == "__main__":

    uf = UnifiedFieldController()

    print("Layer 20 — Unified Field Convergence Demo")

    demo = [

        # stable baseline
        FieldSignal(pressure=0.2, identity_score=0.9, margin=0.9, style_stability=0.9),

        # rising tension
        FieldSignal(pressure=0.6, identity_score=0.7, margin=0.8, style_stability=0.7),

        # fracture moment
        FieldSignal(pressure=0.9, identity_score=0.4, margin=0.6, style_stability=0.5),

        # recovery
        FieldSignal(pressure=0.3, identity_score=0.8, margin=0.85, style_stability=0.85),

    ]

    for s in demo:
        status = uf.observe(s)
        uf.render(status)

