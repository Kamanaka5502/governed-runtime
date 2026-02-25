import collections

# ======================================================
# LAYER 63 — EXPLANATION PATTERN MONITOR
# Detects governance explanation bias over time
# ======================================================

class ExplanationPatternMonitor:

    def __init__(self, window=10):
        self.window = window
        self.history = []

    def record(self, explanation):
        self.history.append(explanation)

        if len(self.history) > self.window:
            self.history.pop(0)

    def analyze(self):

        if not self.history:
            return {"status": "NO_DATA"}

        causes = [e["cause"] for e in self.history]
        outcomes = [e["outcome"] for e in self.history]

        cause_count = collections.Counter(causes)
        outcome_count = collections.Counter(outcomes)

        dominant_cause = cause_count.most_common(1)[0]
        dominant_outcome = outcome_count.most_common(1)[0]

        bias_flag = False
        recommendation = "BALANCED"

        # Simple drift heuristic
        if dominant_outcome[0] == "BLOCKED" and dominant_outcome[1] >= len(self.history) * 0.7:
            bias_flag = True
            recommendation = "INCREASE_EXPLORATION_WINDOW"

        if dominant_outcome[0] == "COMMITTED" and dominant_outcome[1] >= len(self.history) * 0.9:
            bias_flag = True
            recommendation = "VERIFY_RISK_GUARDS"

        return {
            "samples": len(self.history),
            "dominant_cause": dominant_cause,
            "dominant_outcome": dominant_outcome,
            "bias_detected": bias_flag,
            "recommendation": recommendation
        }


# ======================================================
# DEMO
# ======================================================

if __name__ == "__main__":

    monitor = ExplanationPatternMonitor(window=8)

    demo_explanations = [
        {"outcome":"BLOCKED","cause":"COOLDOWN_ACTIVE"},
        {"outcome":"BLOCKED","cause":"COOLDOWN_ACTIVE"},
        {"outcome":"COMMITTED","cause":"ADJUSTMENT_COMMITTED"},
        {"outcome":"BLOCKED","cause":"COOLDOWN_ACTIVE"},
        {"outcome":"BLOCKED","cause":"COOLDOWN_ACTIVE"},
        {"outcome":"BLOCKED","cause":"COOLDOWN_ACTIVE"},
        {"outcome":"BLOCKED","cause":"COOLDOWN_ACTIVE"},
        {"outcome":"COMMITTED","cause":"ADJUSTMENT_COMMITTED"},
    ]

    print("=== LAYER 63 — EXPLANATION PATTERN MONITOR ===")

    for d in demo_explanations:
        monitor.record(d)

    print(monitor.analyze())

def process(state):

    state["pressure"] *= 0.9995
    state["coherence"] = min(1.0, state.get("coherence",0)+0.0002)

    print({
        "layer": "63_explanation_patterns",
        "status": "active"
    })

    return state
