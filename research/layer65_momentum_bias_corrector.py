import statistics

# =====================================================
# LAYER 65 — MOMENTUM BIAS CORRECTOR
# Detects false momentum / stagnation masked as stability
# =====================================================

class MomentumBiasCorrector:

    def __init__(self, window=8):
        self.window = window
        self.history = []

    def record(self, momentum, continuity):
        entry = {
            "momentum": momentum,
            "continuity": continuity
        }

        self.history.append(entry)

        if len(self.history) > self.window:
            self.history.pop(0)

    def analyze(self):
        if len(self.history) < 3:
            return {
                "status": "INSUFFICIENT_DATA",
                "bias_detected": False,
                "recommendation": "Collect more samples"
            }

        momentum_vals = [e["momentum"] for e in self.history]
        continuity_vals = [e["continuity"] for e in self.history]

        avg_momentum = statistics.mean(momentum_vals)
        momentum_var = statistics.pvariance(momentum_vals)

        avg_continuity = statistics.mean(continuity_vals)

        bias_detected = False
        recommendation = "Healthy momentum"

        # Core insight:
        # High continuity but near-zero momentum = false stability
        if abs(avg_momentum) < 0.01 and avg_continuity > 0.8:
            bias_detected = True
            recommendation = "Momentum illusion: introduce exploration"

        # Oscillation case
        elif momentum_var > 0.02:
            bias_detected = True
            recommendation = "Momentum unstable: reduce adjustment frequency"

        return {
            "avg_momentum": round(avg_momentum, 3),
            "momentum_variance": round(momentum_var, 3),
            "avg_continuity": round(avg_continuity, 3),
            "bias_detected": bias_detected,
            "recommendation": recommendation
        }


# =====================================================
# DEMO RUN
# =====================================================

if __name__ == "__main__":

    b = MomentumBiasCorrector()

    print("=== LAYER 65 — MOMENTUM BIAS CORRECTOR ===")

    demo = [
        (0.03, 0.94),
        (0.02, 0.93),
        (0.01, 0.92),
        (0.00, 0.91),
        (0.01, 0.90),
        (0.00, 0.89),
        (0.00, 0.88),
    ]

    for m, c in demo:
        b.record(m, c)

    print(b.analyze())


def process(state):

    state["pressure"] *= 0.9995
    state["coherence"] = min(1.0, state.get("coherence",0)+0.0002)

    print({
        "layer": "65_momentum_bias_corrector",
        "status": "active"
    })

    return state
