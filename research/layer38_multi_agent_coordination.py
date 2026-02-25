# ==========================================================
# Layer 38 — Multi-Agent Policy Coordination
# Multiple governance agents coordinate decisions
# ==========================================================

class GovernanceAgent:

    def __init__(self, name, weights=None):
        self.name = name
        self.weights = weights or {
            "safe": 1.0,
            "guarded": 1.0,
            "restricted": 1.0
        }

    def evaluate(self, risk):
        score_safe = (1 - risk) * self.weights["safe"]
        score_guarded = (1 - abs(risk - 0.5)) * self.weights["guarded"]
        score_restricted = risk * self.weights["restricted"]

        scores = {
            "safe": round(score_safe, 3),
            "guarded": round(score_guarded, 3),
            "restricted": round(score_restricted, 3),
        }

        boundary = max(scores, key=scores.get)

        return {
            "agent": self.name,
            "risk": risk,
            "scores": scores,
            "boundary": boundary
        }


class MultiAgentCoordinator:

    def __init__(self, agents):
        self.agents = agents

    def coordinate(self, risk):

        evaluations = [a.evaluate(risk) for a in self.agents]

        # voting
        vote_count = {"safe": 0, "guarded": 0, "restricted": 0}
        for e in evaluations:
            vote_count[e["boundary"]] += 1

        # majority wins; tie -> guarded (neutral stability)
        selected = max(vote_count, key=vote_count.get)

        if list(vote_count.values()).count(vote_count[selected]) > 1:
            selected = "guarded"

        return {
            "risk": risk,
            "evaluations": evaluations,
            "votes": vote_count,
            "selected_boundary": selected
        }


# ==========================================================
# DEMO / TEST RUN
# ==========================================================

if __name__ == "__main__":

    a1 = GovernanceAgent("agent_alpha", {
        "safe": 1.1,
        "guarded": 1.0,
        "restricted": 0.9
    })

    a2 = GovernanceAgent("agent_beta", {
        "safe": 0.9,
        "guarded": 1.1,
        "restricted": 1.0
    })

    a3 = GovernanceAgent("agent_gamma", {
        "safe": 1.0,
        "guarded": 0.9,
        "restricted": 1.2
    })

    mac = MultiAgentCoordinator([a1, a2, a3])

    print("=== LAYER 38 — MULTI-AGENT COORDINATION ===")

    for risk in [0.2, 0.5, 0.85]:
        result = mac.coordinate(risk)

        print("\n--- Coordination Round ---")
        print("Risk:", result["risk"])
        print("Votes:", result["votes"])
        print("Selected:", result["selected_boundary"])

        for e in result["evaluations"]:
            print(e)


def process(state):

    state["pressure"] *= 0.9995
    state["coherence"] = min(1.0, state.get("coherence",0)+0.0002)

    print({
        "layer": "38_multi_agent_coordination",
        "status": "active"
    })

    return state
