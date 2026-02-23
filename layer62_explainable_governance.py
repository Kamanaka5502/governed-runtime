class ExplanationEngine:

    def explain(self, step, decision):

        allowed = decision["allowed"]
        reason = decision["reason"]

        if allowed:
            outcome = "COMMITTED"
            risk = "LOW"
            alternative = "NONE"
        else:
            outcome = "BLOCKED"

            if reason == "COOLDOWN_ACTIVE":
                risk = "THRESHOLD_DRIFT"
                alternative = "WAIT_NEXT_WINDOW"
            else:
                risk = "UNKNOWN"
                alternative = "MANUAL_REVIEW"

        return {
            "step": step,
            "outcome": outcome,
            "cause": reason,
            "risk_if_overridden": risk,
            "alternative_path": alternative,
            "explainability_score": 1.0
        }


# =====================
# DEMO
# =====================

if __name__ == "__main__":

    engine = ExplanationEngine()

    demo = [
        {"allowed": False, "reason": "COOLDOWN_ACTIVE"},
        {"allowed": True, "reason": "ADJUSTMENT_COMMITTED"},
        {"allowed": False, "reason": "COOLDOWN_ACTIVE"},
    ]

    print("=== LAYER 62 — EXPLAINABLE GOVERNANCE ===")

    for i, d in enumerate(demo, start=1):
        print(engine.explain(i, d))

def process(state):

    state["pressure"] *= 0.9995
    state["coherence"] = min(1.0, state.get("coherence",0)+0.0002)

    print({
        "layer": "62_explainable_governance",
        "status": "active"
    })

    return state
