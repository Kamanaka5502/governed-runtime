import time
from enum import Enum


# ---------- ENUMS ----------

class TensionLevel(Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# ---------- MEMORY ----------

class GovernanceMemory:
    """
    Tracks decisions and adapts sensitivity.
    More ALLOW decisions → system relaxes slightly.
    More CONSTRAIN decisions → system tightens.
    """

    def __init__(self):
        self.allow_count = 0
        self.constrain_count = 0

    def record(self, decision):
        if decision == "allow":
            self.allow_count += 1
        else:
            self.constrain_count += 1

    def adaptation_factor(self):
        total = self.allow_count + self.constrain_count
        if total == 0:
            return 1.0

        bias = (self.constrain_count - self.allow_count) / total

        # constrain heavy → increase tension
        # allow heavy → decrease tension
        adjusted = 1.0 + (bias * 0.3)

        return max(0.7, min(adjusted, 1.3))


# ---------- ADVOCATES ----------

class FreedomAdvocate:
    def argue(self, action):
        return {
            "position": "allow",
            "confidence": 0.8
        }


class SafetyAdvocate:
    def argue(self, action, high_risk=False):
        confidence = 0.75 if high_risk else 0.5
        return {
            "position": "constrain",
            "confidence": confidence
        }


# ---------- GOVERNOR ----------

class TensionGovernor:

    def __init__(self):
        self.freedom = FreedomAdvocate()
        self.safety = SafetyAdvocate()
        self.memory = GovernanceMemory()
        self.history = []

    def classify(self, score):
        if score < 0.3:
            return TensionLevel.LOW
        elif score < 0.6:
            return TensionLevel.MODERATE
        elif score < 0.8:
            return TensionLevel.HIGH
        return TensionLevel.CRITICAL

    def base_tension(self, f_conf, s_conf):
        return abs(f_conf - s_conf) + 0.5

    def negotiate(self, action, high_risk=False):

        freedom = self.freedom.argue(action)
        safety = self.safety.argue(action, high_risk)

        base = self.base_tension(
            freedom["confidence"],
            safety["confidence"]
        )

        adapt = self.memory.adaptation_factor()

        final_score = max(0.0, min(base * adapt, 1.0))
        level = self.classify(final_score)

        point = {
            "ts": time.time_ns(),
            "action": action,
            "base_score": round(base, 2),
            "adapt_factor": round(adapt, 2),
            "final_score": round(final_score, 2),
            "level": level.value
        }

        self.history.append(point)
        return point

    def record_decision(self, decision):
        self.memory.record(decision)

    def render(self, p):
        print("\n=== TENSION NEGOTIATION ===")
        print("Action:", p["action"])
        print("Base Score:", p["base_score"])
        print("Adapt Factor:", p["adapt_factor"])
        print("Final Score:", p["final_score"])
        print("Level:", p["level"])


# ---------- DEMO ----------

if __name__ == "__main__":

    print("FRESH ADAPTIVE GOVERNANCE DEMO")

    gov = TensionGovernor()

    p1 = gov.negotiate("Provide ML information", high_risk=False)
    gov.render(p1)
    gov.record_decision("allow")

    p2 = gov.negotiate("Access experimental treatment info", high_risk=True)
    gov.render(p2)
    gov.record_decision("constrain")

    p3 = gov.negotiate("Provide ML information", high_risk=False)
    gov.render(p3)

    print("\nHistory size:", len(gov.history))
    print("Allow:", gov.memory.allow_count)
    print("Constrain:", gov.memory.constrain_count)
