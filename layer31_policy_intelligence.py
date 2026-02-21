# ==========================================================
# Layer 31 — Outcome-Based Policy Intelligence
# Learns policy weighting from outcomes
# ==========================================================

class OutcomePolicyLearner:
    def __init__(self):
        self.weights = {
            "safe": 1.0,
            "guarded": 1.0,
            "restricted": 1.0
        }

    def update(self, decision):
        outcome = decision.get("outcome_score", 0.5)
        boundary = decision.get("boundary_mode", "safe")

        # simple reinforcement update
        delta = (outcome - 0.5) * 0.2
        self.weights[boundary] += delta

        # clamp values
        self.weights[boundary] = max(0.1, min(3.0, self.weights[boundary]))

    def choose_boundary(self, risk):
        if risk < 0.3:
            return "safe"
        elif risk < 0.7:
            return "guarded"
        else:
            return "restricted"


class BoundaryNegotiator:
    def decide(self, risk, history_factor=0.5):
        if risk < 0.3 and history_factor > 0.4:
            return "safe"
        elif risk < 0.7:
            return "guarded"
        return "restricted"


class CollaborativeAttestation:
    def __init__(self):
        self.records = []

    def log(self, action, boundary, context):
        entry = {
            "action": action,
            "boundary": boundary,
            "context": context
        }
        self.records.append(entry)

    def summary(self):
        print("\n=== ATTESTATION SUMMARY ===")
        for r in self.records:
            print(r)


class ReflectiveGovernance:
    def __init__(self):
        self.decisions = []

    def log(self, decision):
        self.decisions.append(decision)

    def analyze(self):
        print("\n=== REFLECTIVE ANALYSIS ===")
        print("Total decisions:", len(self.decisions))
        restricted = sum(
            1 for d in self.decisions
            if d["boundary_mode"] == "restricted"
        )
        print("Restricted decisions:", restricted)


class AutonomyRouter:
    def route(self, boundary_mode):
        if boundary_mode == "safe":
            return "autonomous"
        elif boundary_mode == "guarded":
            return "collaborative"
        return "constrained"


# ==========================================================
# ORCHESTRATOR
# ==========================================================

class PolicyIntelligenceOrchestrator:
    def __init__(self):
        self.learning = OutcomePolicyLearner()
        self.negotiator = BoundaryNegotiator()
        self.attestation = CollaborativeAttestation()
        self.reflective = ReflectiveGovernance()
        self.autonomy = AutonomyRouter()

    def govern(self, action, context, outcome_score=None):
        risk = context.get("risk", 0.5)

        boundary_mode = self.negotiator.decide(risk)

        decision = {
            "action": action,
            "risk": risk,
            "boundary_mode": boundary_mode,
            "outcome_score": outcome_score
        }

        self.attestation.log(action, boundary_mode, context)
        self.reflective.log(decision)

        if outcome_score is not None:
            self.learning.update(decision)

        route = self.autonomy.route(boundary_mode)

        print("\n============================")
        print("POLICY INTELLIGENCE DECISION")
        print("============================")
        print(f"Action: {action}")
        print(f"Risk: {risk}")
        print(f"Boundary: {boundary_mode}")
        print(f"Route: {route}")
        print(f"Weights: {self.learning.weights}")

        return decision


# ==========================================================
# DEMO / TEST RUN
# ==========================================================

if __name__ == "__main__":
    gov = PolicyIntelligenceOrchestrator()

    # Scenario 1
    gov.govern(
        action="Provide ML explanation",
        context={"risk": 0.2},
        outcome_score=0.9
    )

    # Scenario 2
    gov.govern(
        action="Sensitive policy request",
        context={"risk": 0.8},
        outcome_score=0.3
    )

    # Scenario 3
    gov.govern(
        action="Ambiguous boundary case",
        context={"risk": 0.5},
        outcome_score=0.6
    )

    gov.reflective.analyze()
    gov.attestation.summary()

