# ==========================================================
# Layer 36 — Cross Context Policy Transfer
# Carries governance learning across environments
# ==========================================================

import copy

class PolicyTransfer:

    def __init__(self):
        self.global_policy = {
            "safe": 1.0,
            "guarded": 1.0,
            "restricted": 1.0
        }
        self.context_snapshots = {}

    def learn(self, boundary, outcome_score):
        """
        Simple outcome-based learning update.
        Positive outcome reinforces.
        Negative outcome weakens.
        """
        delta = (outcome_score - 0.5) * 0.2
        self.global_policy[boundary] += delta
        self.global_policy[boundary] = round(self.global_policy[boundary], 3)

    def export_context(self, name):
        """
        Save policy state for a context.
        """
        self.context_snapshots[name] = copy.deepcopy(self.global_policy)

    def import_context(self, name):
        """
        Load known policy profile.
        """
        if name in self.context_snapshots:
            self.global_policy = copy.deepcopy(self.context_snapshots[name])

    def decision_bias(self, risk):
        """
        Select preferred boundary based on policy weights.
        """
        score_safe = (1 - risk) * self.global_policy["safe"]
        score_guarded = (1 - abs(risk - 0.5)) * self.global_policy["guarded"]
        score_restricted = risk * self.global_policy["restricted"]

        scores = {
            "safe": round(score_safe, 3),
            "guarded": round(score_guarded, 3),
            "restricted": round(score_restricted, 3),
        }

        boundary = max(scores, key=scores.get)

        return {
            "risk": risk,
            "scores": scores,
            "selected": boundary,
            "weights": dict(self.global_policy)
        }


# ==========================================================
# DEMO / TEST RUN
# ==========================================================

if __name__ == "__main__":

    pt = PolicyTransfer()

    print("=== LAYER 36 — POLICY TRANSFER ===")

    # Context A (technical collaboration)
    pt.learn("safe", 0.9)
    pt.learn("guarded", 0.6)
    pt.export_context("technical")

    print("\nContext: technical")
    print(pt.decision_bias(0.3))

    # Context B (sensitive governance)
    pt.learn("restricted", 0.95)
    pt.learn("restricted", 0.8)
    pt.export_context("sensitive")

    print("\nContext: sensitive")
    print(pt.decision_bias(0.8))

    # Return to previous context
    pt.import_context("technical")

    print("\nContext: reloaded technical")
    print(pt.decision_bias(0.3))

