# ==========================================================
# Layer 39 — Policy Conflict Resolution
# Resolves disagreement between governance agents
# ==========================================================

class GovernanceAgent:

    def __init__(self, name, weights):
        self.name = name
        self.weights = weights

    def evaluate(self, risk):
        safe = (1 - risk) * self.weights["safe"]
        guarded = (1 - abs(risk - 0.5)) * self.weights["guarded"]
        restricted = risk * self.weights["restricted"]

        scores = {
            "safe": round(safe, 3),
            "guarded": round(guarded, 3),
            "restricted": round(restricted, 3)
        }

        boundary = max(scores, key=scores.get)

        return {
            "agent": self.name,
            "risk": risk,
            "scores": scores,
            "boundary": boundary
        }


class ConflictResolver:

    def __init__(self, agents):
        self.agents = agents

    def resolve(self, risk):

        evaluations = [a.evaluate(risk) for a in self.agents]

        boundaries = [e["boundary"] for e in evaluations]

        vote_count = {"safe": 0, "guarded": 0, "restricted": 0}
        for b in boundaries:
            vote_count[b] += 1

        # disagreement metric
        unique_choices = len(set(boundaries))

        if unique_choices == 1:
            mode = "consensus"
            final = boundaries[0]

        elif unique_choices == 2:
            mode = "negotiated"
            # choose guarded if present (stability anchor)
            final = "guarded" if "guarded" in boundaries else max(vote_count, key=vote_count.get)

        else:
            mode = "high_conflict"
            final = "guarded"  # forced stabilization

        return {
            "risk": risk,
            "mode": mode,
            "votes": vote_count,
            "final_boundary": final,
            "evaluations": evaluations
        }


# ==========================================================
# DEMO / TEST RUN
# ==========================================================

if __name__ == "__main__":

    agents = [
        GovernanceAgent("alpha", {"safe":1.1, "guarded":1.0, "restricted":0.9}),
        GovernanceAgent("beta", {"safe":0.9, "guarded":1.1, "restricted":1.0}),
        GovernanceAgent("gamma", {"safe":1.0, "guarded":0.9, "restricted":1.2}),
    ]

    cr = ConflictResolver(agents)

    print("=== LAYER 39 — POLICY CONFLICT RESOLUTION ===")

    for risk in [0.15, 0.5, 0.85]:
        result = cr.resolve(risk)

        print("\n--- Conflict Round ---")
        print("Risk:", result["risk"])
        print("Mode:", result["mode"])
        print("Votes:", result["votes"])
        print("Final:", result["final_boundary"])

        for e in result["evaluations"]:
            print(e)

