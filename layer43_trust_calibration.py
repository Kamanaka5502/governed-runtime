# ==========================================================
# Layer 43 — Trust Calibration Engine
# Converts policy memory into governance confidence
# ==========================================================

import json
import os

STATE_FILE = "governance_state.json"

class TrustCalibrationEngine:

    def __init__(self):
        self.weights = {
            "safe": 1.0,
            "guarded": 1.0,
            "restricted": 1.0
        }
        self.load()

    # ------------------------------------------------------
    # LOAD MEMORY
    # ------------------------------------------------------
    def load(self):
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r") as f:
                data = json.load(f)
                self.weights = data.get("weights", self.weights)

    # ------------------------------------------------------
    # NORMALIZE WEIGHTS
    # ------------------------------------------------------
    def normalized(self):
        total = sum(self.weights.values())
        return {
            k: round(v / total, 3)
            for k, v in self.weights.items()
        }

    # ------------------------------------------------------
    # TRUST SCORE
    # ------------------------------------------------------
    def trust_score(self):
        norm = self.normalized()

        # higher "safe" increases trust
        # high "restricted" lowers autonomy confidence
        score = (
            norm["safe"] * 1.0 +
            norm["guarded"] * 0.6 +
            norm["restricted"] * 0.2
        )

        return round(score, 3), norm

    # ------------------------------------------------------
    # ROUTING DECISION
    # ------------------------------------------------------
    def route(self):
        score, norm = self.trust_score()

        if score > 0.65:
            mode = "autonomous"
        elif score > 0.45:
            mode = "collaborative"
        else:
            mode = "constrained"

        return {
            "trust_score": score,
            "normalized_weights": norm,
            "recommended_mode": mode
        }


# ==========================================================
# DEMO RUN
# ==========================================================

if __name__ == "__main__":

    tc = TrustCalibrationEngine()

    print("=== LAYER 43 — TRUST CALIBRATION ===")
    result = tc.route()

    print("Trust score:", result["trust_score"])
    print("Normalized:", result["normalized_weights"])
    print("Recommended mode:", result["recommended_mode"])
