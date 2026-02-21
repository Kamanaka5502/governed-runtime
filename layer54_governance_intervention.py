import statistics

# ============================================
# LAYER 54 — GOVERNANCE INTERVENTION ENGINE
# ============================================

class GovernanceIntervention:

    def __init__(self, coherence_threshold=0.9):
        self.threshold = coherence_threshold
        self.last_action = "NONE"

    def evaluate(self, coherence, oscillation, dominant_mode):

        action = "NONE"

        # severe instability
        if oscillation:
            action = "FORCE_LOCKDOWN"

        # mild drift
        elif coherence < self.threshold:
            action = "BIAS_STABILIZE"

        # recovery path
        elif coherence > 0.97 and dominant_mode == "LOCKDOWN":
            action = "RELEASE_EXPLORE"

        self.last_action = action

        return {
            "coherence": round(coherence, 3),
            "oscillation": oscillation,
            "dominant_mode": dominant_mode,
            "intervention": action
        }


# ============================================
# DEMO RUN
# ============================================

if __name__ == "__main__":

    gov = GovernanceIntervention()

    print("=== LAYER 54 - GOVERNANCE INTERVENTION ===")

    scenarios = [
        (0.99, False, "STABILIZE"),
        (0.88, False, "STABILIZE"),
        (0.85, True,  "EXPLORE"),
        (0.96, False, "LOCKDOWN"),
        (0.99, False, "LOCKDOWN"),
    ]

    for c, o, m in scenarios:
        print(gov.evaluate(c, o, m))

