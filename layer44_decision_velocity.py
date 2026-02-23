# ==========================================================
# Layer 44 — Decision Velocity Controller
# Governs decision speed based on trust + risk
# ==========================================================

import json
import os

STATE_FILE = "governance_state.json"

class DecisionVelocityController:

    def __init__(self):
        self.weights = {
            "safe": 1.0,
            "guarded": 1.0,
            "restricted": 1.0
        }
        self.load()

    # ------------------------------------------------------
    # LOAD STATE
    # ------------------------------------------------------
    def load(self):
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r") as f:
                data = json.load(f)
                self.weights = data.get("weights", self.weights)

    # ------------------------------------------------------
    # TRUST SCORE (same logic as Layer 43)
    # ------------------------------------------------------
    def trust_score(self):
        total = sum(self.weights.values())
        norm = {k: v / total for k, v in self.weights.items()}

        score = (
            norm["safe"] * 1.0 +
            norm["guarded"] * 0.6 +
            norm["restricted"] * 0.2
        )

        return round(score, 3)

    # ------------------------------------------------------
    # VELOCITY MODEL
    # ------------------------------------------------------
    def velocity(self, risk):

        trust = self.trust_score()

        # velocity equation
        # trust speeds up
        # risk slows down
        speed = trust * (1.0 - risk)

        if speed > 0.6:
            mode = "fast_execute"
        elif speed > 0.3:
            mode = "deliberate"
        else:
            mode = "slow_verify"

        return {
            "risk": risk,
            "trust": trust,
            "velocity": round(speed, 3),
            "mode": mode
        }


# ==========================================================
# DEMO RUN
# ==========================================================

if __name__ == "__main__":

    vc = DecisionVelocityController()

    print("=== LAYER 44 — DECISION VELOCITY ===")

    for r in [0.2, 0.5, 0.8]:
        result = vc.velocity(r)
        print(result)

def process(state):

    state["pressure"] *= 0.9995
    state["coherence"] = min(1.0, state.get("coherence",0)+0.0002)

    print({
        "layer": "44_decision_velocity",
        "status": "active"
    })

    return state
