# =====================================================
# LAYER 79 + 80
# Adaptive Trajectory Regulation + Stability Closure
# =====================================================

import statistics


class AdaptiveTrajectoryRegulator:
    """
    Layer 79:
    Adjusts governance pressure based on trajectory risk.
    """

    def __init__(self):
        self.history = []

    def record(self, projected_stability, risk_horizon):
        self.history.append(
            {
                "projected_stability": projected_stability,
                "risk": risk_horizon
            }
        )

        if len(self.history) > 20:
            self.history.pop(0)

    def regulate(self):

        if len(self.history) < 2:
            return {"status": "INSUFFICIENT_DATA"}

        current = self.history[-1]
        prev = self.history[-2]

        stability_delta = round(
            current["projected_stability"] -
            prev["projected_stability"], 3
        )

        if current["risk"] > 0.20:
            action = "INCREASE_STABILIZATION"
        elif stability_delta < 0:
            action = "SOFT_CORRECT"
        else:
            action = "MAINTAIN"

        return {
            "stability_delta": stability_delta,
            "risk": current["risk"],
            "regulation_action": action
        }


class StabilityFinalizer:
    """
    Layer 80:
    Determines if system has reached sustainable closure.
    """

    def __init__(self):
        self.window = []

    def record(self, stability):
        self.window.append(stability)
        if len(self.window) > 10:
            self.window.pop(0)

    def finalize(self):

        if len(self.window) < 5:
            return {"status": "INSUFFICIENT_DATA"}

        avg = round(statistics.mean(self.window), 3)
        variance = round(statistics.pvariance(self.window), 4)

        if avg >= 0.85 and variance < 0.002:
            state = "STABLE_CLOSURE"
        elif avg >= 0.75:
            state = "STABILIZING"
        else:
            state = "UNSETTLED"

        return {
            "average_stability": avg,
            "variance": variance,
            "closure_state": state
        }


# =====================================================
# DEMO RUN
# =====================================================

if __name__ == "__main__":

    print("=== LAYER 79 + 80 DEMO ===")

    regulator = AdaptiveTrajectoryRegulator()
    finalizer = StabilityFinalizer()

    demo_projection = [
        (0.80, 0.12),
        (0.83, 0.10),
        (0.85, 0.08),
        (0.87, 0.06),
        (0.88, 0.05),
        (0.89, 0.04),
    ]

    for proj, risk in demo_projection:
        regulator.record(proj, risk)
        finalizer.record(proj)

    print("\n--- Layer 79 Output ---")
    print(regulator.regulate())

    print("\n--- Layer 80 Output ---")
    print(finalizer.finalize())

