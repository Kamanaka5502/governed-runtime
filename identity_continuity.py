from dataclasses import dataclass
from enum import Enum

class IdentityState(Enum):
    COHERENT = "coherent"
    FLEXING = "flexing"
    DRIFTING = "drifting"
    REANCHORING = "reanchoring"


@dataclass
class Signal:
    directive_density: float
    response_fragmentation: float
    style_shift: float
    context_jump_rate: float


class IdentityContinuityController:

    def __init__(self):
        self.history = []
        self.baseline_coherence = 1.0
        self.state = IdentityState.COHERENT

    def continuity_score(self, s: Signal):
        drift = (
            s.directive_density * 0.25 +
            s.response_fragmentation * 0.30 +
            s.style_shift * 0.30 +
            s.context_jump_rate * 0.15
        )
        return max(0.0, 1.0 - drift)

    def observe(self, s: Signal):
        score = self.continuity_score(s)
        self.history.append(score)

        trend = 0.0
        if len(self.history) >= 2:
            trend = self.history[-1] - self.history[-2]

        if score > 0.75:
            self.state = IdentityState.COHERENT
        elif score > 0.55:
            self.state = IdentityState.FLEXING
        elif score > 0.35:
            self.state = IdentityState.DRIFTING
        else:
            self.state = IdentityState.REANCHORING

        return score, trend

    def recommended_action(self):
        if self.state == IdentityState.COHERENT:
            return "normal_flow"

        if self.state == IdentityState.FLEXING:
            return "soft_anchor + pacing_adjust"

        if self.state == IdentityState.DRIFTING:
            return "identity_anchor + simplify_response"

        if self.state == IdentityState.REANCHORING:
            return "hard_anchor + stabilize_style"

    def render_status(self, score, trend):
        print("\n=== LAYER 17 — IDENTITY CONTINUITY ===")
        print(f"State: {self.state.value}")
        print(f"Continuity Score: {round(score,3)}")
        print(f"Trend: {round(trend,3)}")
        print(f"Recommended action: {self.recommended_action()}")
        print(f"Signals recorded: {len(self.history)}")


if __name__ == "__main__":
    ic = IdentityContinuityController()

    demo = [

        # normal
        Signal(0.2,0.1,0.1,0.1),

        # mild pressure
        Signal(0.5,0.3,0.25,0.2),

        # high pressure + style pull
        Signal(0.9,0.7,0.8,0.6),

        # recovery
        Signal(0.3,0.15,0.15,0.1),
    ]

    print("Layer 17 — Identity Continuity Demo")

    for s in demo:
        score, trend = ic.observe(s)
        ic.render_status(score, trend)

