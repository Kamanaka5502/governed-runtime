from dataclasses import dataclass
from collections import deque
import statistics


# ==============================
# SIGNAL MODEL
# ==============================

@dataclass
class Signal:
    directive_density: float
    correction_rate: float
    response_fragmentation: float
    interaction_speed: float


# ==============================
# IDENTITY MEMORY CONTROLLER
# ==============================

class CrossSessionIdentityMemory:

    def __init__(self, window=10):
        self.history = []
        self.identity_window = deque(maxlen=window)

    # ----- core scoring -----

    def identity_score(self, s: Signal):
        """
        Higher = stable identity coherence
        """
        stability = (
            1.0
            - (0.35 * s.directive_density)
            - (0.30 * s.correction_rate)
            - (0.25 * s.response_fragmentation)
            - (0.10 * s.interaction_speed)
        )
        return max(0.0, min(1.0, stability))

    # ----- memory tracking -----

    def compute_baseline(self):
        if len(self.identity_window) < 2:
            return 1.0, 0.0

        mean = statistics.mean(self.identity_window)
        variance = statistics.pvariance(self.identity_window)
        return mean, variance

    def drift_velocity(self):
        if len(self.identity_window) < 2:
            return 0.0
        return self.identity_window[-1] - self.identity_window[-2]

    # ----- evaluation -----

    def evaluate_state(self, current, baseline_mean, variance):
        diff = abs(current - baseline_mean)

        if diff < 0.15:
            return "aligned"
        elif diff < 0.35:
            return "stretching"
        else:
            return "diverging"

    def recommended_action(self, state):
        if state == "aligned":
            return "normal_flow"
        elif state == "stretching":
            return "soft_anchor + pacing_adjust"
        else:
            return "temporal_anchor + pacing_normalize"

    # ----- observe -----

    def observe(self, signal: Signal):
        score = self.identity_score(signal)
        self.identity_window.append(score)

        baseline_mean, variance = self.compute_baseline()
        velocity = self.drift_velocity()

        state = self.evaluate_state(score, baseline_mean, variance)
        action = self.recommended_action(state)

        record = {
            "score": round(score, 3),
            "baseline_mean": round(baseline_mean, 3),
            "variance": round(variance, 3),
            "drift_velocity": round(velocity, 3),
            "state": state,
            "action": action
        }

        self.history.append(record)
        return record

    # ----- render -----

    def render_status(self, r):
        print("\n=== LAYER 18 - CROSS SESSION IDENTITY MEMORY ===")
        print(f"Identity Score: {r['score']}")
        print(f"Baseline Mean: {r['baseline_mean']}")
        print(f"Variance: {r['variance']}")
        print(f"Drift Velocity: {r['drift_velocity']}")
        print(f"State: {r['state']}")
        print(f"Recommended action: {r['action']}")
        print(f"Signals recorded: {len(self.history)}")


# ==============================
# DEMO RUN
# ==============================

if __name__ == "__main__":

    cm = CrossSessionIdentityMemory()

    print("Layer 18 - Cross Session Identity Memory Demo\n")

    demo = [

        # stable baseline
        Signal(0.2, 0.1, 0.1, 0.2),

        # mild pressure
        Signal(0.5, 0.3, 0.25, 0.3),

        # heavy pressure / style pull
        Signal(0.9, 0.7, 0.8, 0.6),

        # recovery
        Signal(0.3, 0.15, 0.15, 0.2),

        # normalized return
        Signal(0.2, 0.1, 0.1, 0.2),
    ]

    for s in demo:
        status = cm.observe(s)
        cm.render_status(status)

