# ============================================================
# Layer 25 — Intervention Gate
# Converts predicted state into governance intensity limits
# ============================================================

class InterventionGate:
    def __init__(self):
        self.mode = "open"

    def evaluate(self, state, trend, acceleration):
        # governance intensity logic

        if state == "fracture_risk":
            self.mode = "restricted"
            mutation_limit = "minimal"
            response_depth = "focused"
            pacing = "slow"

        elif state == "declining":
            self.mode = "guarded"
            mutation_limit = "reduced"
            response_depth = "controlled"
            pacing = "steady"

        elif state == "recovering":
            self.mode = "stabilizing"
            mutation_limit = "normal"
            response_depth = "normal"
            pacing = "steady"

        else:
            self.mode = "open"
            mutation_limit = "normal"
            response_depth = "full"
            pacing = "normal"

        return {
            "mode": self.mode,
            "trend": round(trend, 3),
            "acceleration": round(acceleration, 3),
            "mutation_limit": mutation_limit,
            "response_depth": response_depth,
            "pacing": pacing
        }


if __name__ == "__main__":
    gate = InterventionGate()

    demo = [
        {"state": "stable", "trend": 0.00, "acceleration": 0.00},
        {"state": "declining", "trend": -0.13, "acceleration": -0.09},
        {"state": "fracture_risk", "trend": -0.22, "acceleration": -0.10},
        {"state": "recovering", "trend": 0.18, "acceleration": 0.30},
        {"state": "stable", "trend": 0.05, "acceleration": 0.02},
    ]

    print("=== LAYER 25 — INTERVENTION GATE ===")

    for d in demo:
        result = gate.evaluate(
            d["state"],
            d["trend"],
            d["acceleration"]
        )
        print(result)
