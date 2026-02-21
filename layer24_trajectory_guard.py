# ============================================================
# Layer 24 — Trajectory Guard
# Predictive governance based on coherence trend
# ============================================================

class TrajectoryGuard:
    def __init__(self):
        self.history = []
        self.state = "stable"

    def observe(self, coherence):
        # keep short rolling memory
        self.history.append(coherence)
        if len(self.history) > 6:
            self.history.pop(0)

        trend = 0.0
        acceleration = 0.0

        # compute simple trend (velocity)
        if len(self.history) >= 2:
            trend = self.history[-1] - self.history[-2]

        # compute acceleration (change of trend)
        if len(self.history) >= 3:
            prev_trend = self.history[-2] - self.history[-3]
            acceleration = trend - prev_trend

        # predictive state logic
        if coherence < 0.4:
            self.state = "fracture_risk"
            action = "hard_recovery"

        elif trend < -0.12 or acceleration < -0.08:
            self.state = "declining"
            action = "preemptive_guard"

        elif trend > 0.08:
            self.state = "recovering"
            action = "stabilize_and_monitor"

        else:
            self.state = "stable"
            action = "normal_flow"

        return {
            "coherence": round(coherence, 3),
            "trend": round(trend, 3),
            "acceleration": round(acceleration, 3),
            "state": self.state,
            "action": action,
            "history": [round(x, 3) for x in self.history]
        }


if __name__ == "__main__":
    tg = TrajectoryGuard()

    demo = [
        0.87,   # stable
        0.82,   # slight decline
        0.70,   # accelerating down
        0.58,   # predictive guard should trigger
        0.36,   # fracture risk
        0.55,   # recovery
        0.79    # stabilized
    ]

    print("=== LAYER 24 — TRAJECTORY GUARD ===")

    for c in demo:
        result = tg.observe(c)
        print(result)
