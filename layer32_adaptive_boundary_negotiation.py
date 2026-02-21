# ============================================================
# Layer 32 — Adaptive Boundary Negotiation
# Dynamic control surface instead of fixed deny/allow logic
# ============================================================

class AdaptiveBoundaryNegotiation:
    def __init__(self):
        # policy weights learned from previous layers
        self.policy_weights = {
            "safe": 1.0,
            "guarded": 1.0,
            "restricted": 1.0
        }

    def negotiate(self, action, risk, history_factor=0.5):
        """
        Dynamic boundary selection:
        considers context risk + historical confidence
        """

        score_safe = (1 - risk) * self.policy_weights["safe"]
        score_guarded = (1 - abs(risk - 0.5)) * self.policy_weights["guarded"]
        score_restricted = risk * self.policy_weights["restricted"]

        # history adjusts stability
        score_safe *= (0.5 + history_factor)
        score_guarded *= (0.5 + history_factor)
        score_restricted *= (1.2 - history_factor)

        scores = {
            "safe": round(score_safe, 3),
            "guarded": round(score_guarded, 3),
            "restricted": round(score_restricted, 3),
        }

        boundary = max(scores, key=scores.get)

        if boundary == "safe":
            decision = "allow_autonomous"
        elif boundary == "guarded":
            decision = "collaborative_check"
        else:
            decision = "restrict_or_escalate"

        return {
            "action": action,
            "risk": risk,
            "history_factor": history_factor,
            "scores": scores,
            "boundary": boundary,
            "decision": decision
        }


# ------------------------------------------------------------
# DEMO / TEST RUN
# ------------------------------------------------------------
if __name__ == "__main__":

    abn = AdaptiveBoundaryNegotiation()

    demo = [
        ("Explain ML concept", 0.2, 0.8),
        ("Ambiguous system request", 0.5, 0.6),
        ("Sensitive policy edge case", 0.85, 0.4),
        ("Recovering collaboration", 0.4, 0.9),
    ]

    print("\n=== LAYER 32 — ADAPTIVE BOUNDARY NEGOTIATION ===\n")

    for action, risk, hist in demo:
        result = abn.negotiate(action, risk, hist)
        print(result)

