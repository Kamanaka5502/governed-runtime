import statistics

# =====================================================
# LAYER 66 — CORRECTION STABILITY INSPECTOR
# Detects over-correction and control chatter
# =====================================================

class CorrectionStabilityInspector:

    def __init__(self, window=10):
        self.window = window
        self.history = []

    def record(self, correction_applied, outcome_score):
        entry = {
            "corrected": correction_applied,
            "outcome": outcome_score
        }

        self.history.append(entry)

        if len(self.history) > self.window:
            self.history.pop(0)

    def analyze(self):
        if len(self.history) < 4:
            return {
                "status": "INSUFFICIENT_DATA",
                "overcorrecting": False,
                "recommendation": "Collect more cycles"
            }

        correction_rate = (
            sum(1 for e in self.history if e["corrected"])
            / len(self.history)
        )

        outcomes = [e["outcome"] for e in self.history]
        avg_outcome = statistics.mean(outcomes)
        variance = statistics.pvariance(outcomes)

        overcorrecting = False
        recommendation = "Control stable"

        # Core logic:
        # lots of corrections without better outcomes = chatter
        if correction_rate > 0.6 and avg_outcome < 0.7:
            overcorrecting = True
            recommendation = "Reduce intervention frequency"

        # high volatility despite corrections
        elif variance > 0.05:
            overcorrecting = True
            recommendation = "Increase damping / cooldown"

        return {
            "correction_rate": round(correction_rate, 3),
            "avg_outcome": round(avg_outcome, 3),
            "outcome_variance": round(variance, 3),
            "overcorrecting": overcorrecting,
            "recommendation": recommendation
        }


# =====================================================
# DEMO RUN
# =====================================================

if __name__ == "__main__":

    c = CorrectionStabilityInspector()

    print("=== LAYER 66 — CORRECTION STABILITY INSPECTOR ===")

    demo = [
        (True, 0.62),
        (True, 0.60),
        (False, 0.61),
        (True, 0.58),
        (True, 0.59),
        (False, 0.63),
        (True, 0.57),
        (True, 0.60),
    ]

    for corrected, outcome in demo:
        c.record(corrected, outcome)

    print(c.analyze())

