from dataclasses import dataclass

@dataclass
class MetaState:
    low_threshold: float = 0.30
    high_threshold: float = 0.70
    last_adjustment_step: int = 0

class MetaLimitsGuard:

    def __init__(self):
        self.state = MetaState()
        self.max_drift_per_cycle = 0.05
        self.cooldown_steps = 2
        self.step_counter = 0

    def clamp(self, value, lo, hi):
        return max(lo, min(value, hi))

    def allow_adjustment(self):
        return (
            self.step_counter - self.state.last_adjustment_step
            >= self.cooldown_steps
        )

    def apply_adjustment(self, proposed_low, proposed_high):

        self.step_counter += 1

        allowed = self.allow_adjustment()
        reason = "COOLDOWN_ACTIVE"

        if allowed:
            delta_low = proposed_low - self.state.low_threshold
            delta_high = proposed_high - self.state.high_threshold

            # drift limiting (non-runaway guarantee)
            delta_low = self.clamp(
                delta_low, -self.max_drift_per_cycle, self.max_drift_per_cycle
            )
            delta_high = self.clamp(
                delta_high, -self.max_drift_per_cycle, self.max_drift_per_cycle
            )

            self.state.low_threshold += delta_low
            self.state.high_threshold += delta_high
            self.state.last_adjustment_step = self.step_counter

            reason = "ADJUSTMENT_COMMITTED"

        return {
            "step": self.step_counter,
            "allowed": allowed,
            "reason": reason,
            "low_threshold": round(self.state.low_threshold, 3),
            "high_threshold": round(self.state.high_threshold, 3),
        }


# ==============================
# DEMO RUN
# ==============================
if __name__ == "__main__":

    guard = MetaLimitsGuard()

    print("=== LAYER 61 — META LIMITS GUARD ===")

    proposals = [
        (0.35, 0.75),  # allowed
        (0.45, 0.85),  # blocked (cooldown)
        (0.50, 0.90),  # allowed (drift limited)
        (0.20, 0.60),  # blocked (cooldown)
        (0.25, 0.65),  # allowed
    ]

    for low, high in proposals:
        print(guard.apply_adjustment(low, high))

def process(state):

    state["pressure"] *= 0.9995
    state["coherence"] = min(1.0, state.get("coherence",0)+0.0002)

    print({
        "layer": "61_meta_limits",
        "status": "active"
    })

    return state
