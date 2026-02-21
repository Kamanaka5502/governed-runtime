import statistics

# =====================================================
# LAYER 64 — MOMENTUM CONTINUITY ENGINE
# Tracks directional coherence across governance cycles
# =====================================================

class MomentumContinuity:

    def __init__(self, window=8):
        self.window = window
        self.history = []

    def record(self, intelligence_score, coherence, committed):
        entry = {
            "intelligence_score": intelligence_score,
            "coherence": coherence,
            "committed": committed
        }

        self.history.append(entry)

        if len(self.history) > self.window:
            self.history.pop(0)

    def momentum_vector(self):
        if len(self.history) < 2:
            return 0.0

        deltas = []

        for i in range(1, len(self.history)):
            prev = self.history[i - 1]["intelligence_score"]
            cur = self.history[i]["intelligence_score"]
            deltas.append(cur - prev)

        return round(statistics.mean(deltas), 3)

    def continuity_score(self):
        if not self.history:
            return 0.0

        coherence_avg = statistics.mean(
            e["coherence"] for e in self.history
        )

        commit_ratio = (
            sum(1 for e in self.history if e["committed"])
            / len(self.history)
        )

        score = (coherence_avg * 0.6) + (commit_ratio * 0.4)
        return round(score, 3)

    def status(self):
        momentum = self.momentum_vector()
        continuity = self.continuity_score()

        if momentum > 0.05 and continuity > 0.7:
            state = "FORWARD_STABLE"
        elif momentum < -0.05:
            state = "DRIFTING"
        else:
            state = "STABLE"

        return {
            "momentum": momentum,
            "continuity": continuity,
            "state": state
        }


# =====================================================
# DEMO RUN
# =====================================================

if __name__ == "__main__":

    m = MomentumContinuity()

    print("=== LAYER 64 — MOMENTUM CONTINUITY ===")

    demo = [
        (0.72, 0.90, True),
        (0.75, 0.92, True),
        (0.78, 0.88, True),
        (0.81, 0.87, True),
        (0.83, 0.91, True),
        (0.84, 0.89, False),
        (0.86, 0.93, True),
    ]

    for i, d in enumerate(demo, start=1):
        m.record(*d)
        print(f"step {i} ->", m.status())

