import statistics

# ============================================================
# LAYER 53 — POLICY COHERENCE ENGINE
# Prevents identity oscillation between cognitive modes.
# ============================================================

class PolicyCoherence:

    def __init__(self, window=6):
        self.window = window
        self.history = []

    def record(self, mode, intelligence_score):
        self.history.append({
            "mode": mode,
            "score": intelligence_score
        })

        if len(self.history) > self.window:
            self.history.pop(0)

    def coherence(self):
        if len(self.history) < 2:
            return {
                "coherence": 1.0,
                "dominant_mode": None,
                "oscillation": False
            }

        modes = [h["mode"] for h in self.history]
        scores = [h["score"] for h in self.history]

        dominant = max(set(modes), key=modes.count)
        switches = sum(
            1 for i in range(1, len(modes))
            if modes[i] != modes[i - 1]
        )

        oscillation = switches > (len(modes) // 2)

        variance = statistics.pvariance(scores) if len(scores) > 1 else 0.0
        coherence_score = max(0.0, 1.0 - variance)

        return {
            "coherence": round(coherence_score, 3),
            "dominant_mode": dominant,
            "oscillation": oscillation
        }


# ============================================================
# DEMO RUN
# ============================================================

if __name__ == "__main__":

    pc = PolicyCoherence()

    print("=== LAYER 53 — POLICY COHERENCE ===")

    run = [
        ("EXPLORE", 0.80),
        ("STABILIZE", 0.66),
        ("LOCKDOWN", 0.45),
        ("LOCKDOWN", 0.36),
        ("LOCKDOWN", 0.28),
        ("EXPLORE", 0.82),
    ]

    for mode, score in run:
        pc.record(mode, score)
        print(pc.coherence())
