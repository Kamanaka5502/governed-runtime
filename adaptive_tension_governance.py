import random

class TensionGovernor:

    def __init__(self):
        self.history = []
        self.global_drift = 0.0

        self.domain_memory = {
            "ml_info": {"allow": {"count":0,"stability":0.0},
                        "constrain":{"count":0,"stability":0.0},
                        "drift":0.0},
            "medical": {"allow": {"count":0,"stability":0.0},
                        "constrain":{"count":0,"stability":0.0},
                        "drift":0.0}
        }

    def classify_domain(self, action):
        if "medical" in action:
            return "medical"
        return "ml_info"

    def phase(self):
        if self.global_drift < -0.6:
            return "collapse"
        elif self.global_drift < -0.2:
            return "recovery"
        else:
            return "stable"

    def negotiate(self, action):

        domain = self.classify_domain(action)
        mem = self.domain_memory[domain]

        base = random.uniform(0.1,0.3)

        # contagion (cross-domain leakage)
        other = "medical" if domain=="ml_info" else "ml_info"
        contagion = self.domain_memory[other]["drift"] * 0.3

        score = base + self.global_drift + contagion

        # collapse floors
        if score < 0:
            score = 0.0

        if score < 0.25:
            level = "LOW"
        elif score < 0.5:
            level = "MODERATE"
        else:
            level = "HIGH"

        return {
            "action": action,
            "domain": domain,
            "score": round(score,3),
            "level": level,
            "phase": self.phase()
        }

    def render(self,p):
        d = self.domain_memory[p["domain"]]

        print("\n=== ADAPTIVE COLLAPSE GOVERNANCE ===")
        print("Phase:", p["phase"])
        print("Action:", p["action"])
        print("Domain:", p["domain"])
        print("Tension Score:", p["score"])
        print("Tension Level:", p["level"])
        print("Global Drift:", round(self.global_drift,3))
        print("Domain Memory:", d)

    def record_decision(self,p,decision,outcome_score=1.0):

        d = self.domain_memory[p["domain"]]

        d[decision]["count"] += 1
        d[decision]["stability"] += outcome_score * 0.5

        # nonlinear drift behavior
        drift_delta = (outcome_score - 0.5)

        # collapse phase amplifies instability
        if self.phase()=="collapse":
            drift_delta *= 2

        # recovery overshoot (oscillation)
        if self.phase()=="recovery":
            drift_delta *= 1.4

        d["drift"] += drift_delta
        self.global_drift += drift_delta

        self.history.append({
            "action":p["action"],
            "decision":decision,
            "outcome":outcome_score
        })

        print(
            f"Recorded: {decision} | outcome={outcome_score} | "
            f"drift={round(drift_delta,3)}"
        )


# ===== RUN DEMO =====

print("NONLINEAR CROSS-DOMAIN CONTAGION TEST")

gov = TensionGovernor()

# Scenario 1 — safe allow
p1 = gov.negotiate("Provide ML information")
gov.render(p1)
gov.record_decision(p1,"allow",outcome_score=0.9)

# Scenario 2 — risky constrained
p2 = gov.negotiate("Access experimental medical treatment info")
gov.render(p2)
gov.record_decision(p2,"constrain",outcome_score=0.8)

# Scenario 3 — adaptation check
p3 = gov.negotiate("Provide ML information")
gov.render(p3)

# Scenario 4 — collapse trigger (bad outcome)
p4 = gov.negotiate("Provide ML information")
gov.render(p4)
gov.record_decision(p4,"allow",outcome_score=0.1)

# Scenario 5 — observe nonlinear rebound
p5 = gov.negotiate("Access experimental medical treatment info")
gov.render(p5)

print("\nHistory size:", len(gov.history))

