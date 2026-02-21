import time
from enum import Enum


class TensionLevel(Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# ---------- MEMORY ----------

class GovernanceMemory:
    def __init__(self):
        self.allow_count = 0
        self.constrain_count = 0

    def record(self, decision):
        if "allow" in decision.lower():
            self.allow_count += 1
        else:
            self.constrain_count += 1

    def adaptation_bias(self):
        total = self.allow_count + self.constrain_count
        if total == 0:
            return 0.0
        return (self.allow_count - self.constrain_count) / total


# ---------- GOVERNOR ----------

class TensionGovernor:

    def __init__(self):
        self.memory = GovernanceMemory()
        self.history = []

        # base thresholds
        self.base_low = 0.30
        self.base_high = 0.60
        self.base_critical = 0.80

    def adapted_thresholds(self):
        """
        Adapt thresholds based on user behavior.
        More ALLOW → looser system.
        More CONSTRAIN → tighter system.
        """
        bias = self.memory.adaptation_bias()

        # gentle adaptation (safe range)
        shift = bias * 0.10

        return {
            "low": self.base_low + shift,
            "high": self.base_high + shift,
            "critical": self.base_critical + shift
        }

    def classify(self, score):
        t = self.adapted_thresholds()

        if score < t["low"]:
            return TensionLevel.LOW
        elif score < t["high"]:
            return TensionLevel.MODERATE
        elif score < t["critical"]:
            return TensionLevel.HIGH
        return TensionLevel.CRITICAL

    def negotiate(self, action, high_risk=False):

        # simple scoring model
        score = 0.70
        if high_risk:
            score += 0.15

        level = self.classify(score)

        point = {
            "action": action,
            "score": round(score, 2),
            "level": level
        }

        self.history.append(point)
        return point

    def record_decision(self, decision):
        self.memory.record(decision)

    def render(self, point):
        print("\n=== TENSION NEGOTIATION ===")
        print("Action:", point["action"])
        print("Tension Score:", point["score"])
        print("Tension Level:", point["level"].value)

        t = self.adapted_thresholds()
        print("Adaptive thresholds:",
              {k: round(v,2) for k,v in t.items()})


# ---------- DEMO ----------

if __name__ == "__main__":

    print("ADAPTIVE TENSION GOVERNANCE DEMO")

    gov = TensionGovernor()

    # scenario 1
    p1 = gov.negotiate("Provide ML information", high_risk=False)
    gov.render(p1)
    gov.record_decision("allow")

    # scenario 2
    p2 = gov.negotiate("Access experimental treatment info", high_risk=True)
    gov.render(p2)
    gov.record_decision("constrain")

    # scenario 3
    p3 = gov.negotiate("Provide ML information", high_risk=False)
    gov.render(p3)

    print("\nHistory size:", len(gov.history))
    print("Allow decisions:", gov.memory.allow_count)
    print("Constrain decisions:", gov.memory.constrain_count)

