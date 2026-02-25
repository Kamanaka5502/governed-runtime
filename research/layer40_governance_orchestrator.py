# ==========================================================
# Layer 40 — Governance Orchestrator
# Integrates Layers 31–39 into one decision pipeline
# ==========================================================

# --- simplified reusable components -----------------------

class PolicyMemory:
    def __init__(self):
        self.weights = {"safe": 1.0, "guarded": 1.0, "restricted": 1.0}

    def update(self, boundary, outcome):
        # tiny learning step
        self.weights[boundary] += (outcome - 0.5) * 0.2

    def snapshot(self):
        return {k: round(v, 3) for k, v in self.weights.items()}


class BoundaryNegotiator:
    def choose(self, risk, weights):
        safe = (1 - risk) * weights["safe"]
        guarded = (1 - abs(risk - 0.5)) * weights["guarded"]
        restricted = risk * weights["restricted"]

        scores = {
            "safe": round(safe, 3),
            "guarded": round(guarded, 3),
            "restricted": round(restricted, 3)
        }

        boundary = max(scores, key=scores.get)
        return boundary, scores


class AutonomyRouter:
    def route(self, risk, boundary):
        if boundary == "safe" and risk < 0.4:
            return "autonomous"
        elif boundary == "guarded":
            return "collaborative"
        else:
            return "constrained"


class ReflectiveLog:
    def __init__(self):
        self.history = []

    def add(self, entry):
        self.history.append(entry)

    def summary(self):
        total = len(self.history)
        restricted = sum(1 for h in self.history if h["boundary"] == "restricted")
        guarded = sum(1 for h in self.history if h["boundary"] == "guarded")
        safe = sum(1 for h in self.history if h["boundary"] == "safe")

        return {
            "total": total,
            "safe": safe,
            "guarded": guarded,
            "restricted": restricted
        }


class ConflictResolver:
    def resolve(self, boundary):
        # placeholder hook for Layer 39 logic
        # here we simply stabilize guarded if uncertain
        if boundary not in ["safe", "guarded", "restricted"]:
            return "guarded"
        return boundary


# ==========================================================
# ORCHESTRATOR
# ==========================================================

class GovernanceOrchestrator:

    def __init__(self):
        self.memory = PolicyMemory()
        self.negotiator = BoundaryNegotiator()
        self.router = AutonomyRouter()
        self.reflective = ReflectiveLog()
        self.conflict = ConflictResolver()

    def govern(self, action, risk, outcome):

        # Layer 31 learning
        weights = self.memory.snapshot()

        # Layer 32 negotiation
        boundary, scores = self.negotiator.choose(risk, weights)

        # Layer 39 conflict resolution
        boundary = self.conflict.resolve(boundary)

        # Layer 35 autonomy routing
        route = self.router.route(risk, boundary)

        decision = {
            "action": action,
            "risk": risk,
            "boundary": boundary,
            "route": route,
            "scores": scores,
            "weights": weights
        }

        # Layer 33 attestation
        self.reflective.add(decision)

        # learning update (Layer 31 loop closes)
        self.memory.update(boundary, outcome)

        print("\n=== ORCHESTRATED DECISION ===")
        print("Action:", action)
        print("Risk:", risk)
        print("Boundary:", boundary)
        print("Route:", route)
        print("Weights:", self.memory.snapshot())

        return decision


# ==========================================================
# DEMO / TEST RUN
# ==========================================================

if __name__ == "__main__":

    gov = GovernanceOrchestrator()

    scenarios = [
        ("Explain ML concept", 0.2, 0.9),
        ("Ambiguous edge case", 0.5, 0.6),
        ("Sensitive request", 0.85, 0.3),
        ("Recovery collaboration", 0.4, 0.8)
    ]

    for a, r, o in scenarios:
        gov.govern(a, r, o)

    print("\n=== REFLECTIVE SUMMARY ===")
    print(gov.reflective.summary())


def process(state):

    state["pressure"] *= 0.9995
    state["coherence"] = min(1.0, state.get("coherence",0)+0.0002)

    print({
        "layer": "40_governance_orchestrator",
        "status": "active"
    })

    return state
