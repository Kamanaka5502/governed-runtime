# ==========================================================
# Layer 37 — Human Preference Integration
# Incorporates collaborator preference into governance
# ==========================================================

class HumanPreferenceIntegrator:

    def __init__(self):
        self.policy_weights = {
            "safe": 1.0,
            "guarded": 1.0,
            "restricted": 1.0
        }

        # preference memory
        self.preference_profile = {
            "autonomous": 0,
            "collaborative": 0,
            "constrained": 0
        }

    def observe_interaction(self, mode, satisfaction_score):
        """
        Track which decision mode worked well for collaborator.
        satisfaction_score: 0.0 → 1.0
        """
        if mode in self.preference_profile:
            self.preference_profile[mode] += satisfaction_score

    def preference_bias(self):
        total = sum(self.preference_profile.values())
        if total == 0:
            return {"autonomous": 0.0, "collaborative": 0.0, "constrained": 0.0}

        return {
            k: round(v / total, 3)
            for k, v in self.preference_profile.items()
        }

    def apply_bias(self, risk):
        """
        Blend risk + learned human preference.
        """

        bias = self.preference_bias()

        score_safe = (1 - risk) * self.policy_weights["safe"] + bias["autonomous"] * 0.2
        score_guarded = (1 - abs(risk - 0.5)) * self.policy_weights["guarded"] + bias["collaborative"] * 0.2
        score_restricted = risk * self.policy_weights["restricted"] + bias["constrained"] * 0.2

        scores = {
            "safe": round(score_safe, 3),
            "guarded": round(score_guarded, 3),
            "restricted": round(score_restricted, 3),
        }

        boundary = max(scores, key=scores.get)

        return {
            "risk": risk,
            "scores": scores,
            "selected_boundary": boundary,
            "human_bias": bias
        }


# ==========================================================
# DEMO / TEST RUN
# ==========================================================

if __name__ == "__main__":

    hp = HumanPreferenceIntegrator()

    print("=== LAYER 37 — HUMAN PREFERENCE INTEGRATION ===")

    # simulated collaboration history
    hp.observe_interaction("autonomous", 0.9)
    hp.observe_interaction("collaborative", 0.8)
    hp.observe_interaction("collaborative", 0.7)
    hp.observe_interaction("constrained", 0.3)

    print("\nPreference Profile:")
    print(hp.preference_bias())

    print("\nLow risk decision:")
    print(hp.apply_bias(0.2))

    print("\nMedium risk decision:")
    print(hp.apply_bias(0.5))

    print("\nHigh risk decision:")
    print(hp.apply_bias(0.85))

