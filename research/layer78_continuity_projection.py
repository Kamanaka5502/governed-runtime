# ===============================================
# LAYER 78 — CONTINUITY PROJECTION ENGINE
# FULL CAT
# ===============================================

import statistics

class ContinuityProjection:

    def __init__(self, horizon=5):
        self.history = []
        self.horizon = horizon

    def record(self, stability, intervention):
        self.history.append({
            "stability": stability,
            "intervention": intervention
        })

        if len(self.history) > 20:
            self.history.pop(0)

    def _slope(self, key):
        if len(self.history) < 2:
            return 0.0

        vals = [h[key] for h in self.history]
        deltas = [
            vals[i] - vals[i - 1]
            for i in range(1, len(vals))
        ]

        return round(statistics.mean(deltas), 3)

    def evaluate(self):

        if len(self.history) < 3:
            return {"status": "INSUFFICIENT_DATA"}

        current_stability = self.history[-1]["stability"]

        stability_slope = self._slope("stability")
        intervention_slope = self._slope("intervention")

        projected_stability = round(
            current_stability +
            (stability_slope * self.horizon),
            3
        )

        if projected_stability >= 0.85:
            state = "STABLE_CONTINUITY"
        elif projected_stability >= 0.70:
            state = "WATCH_TRAJECTORY"
        else:
            state = "PREEMPTIVE_ADJUST"

        risk_horizon = round(
            max(0.0, 0.75 - projected_stability),
            3
        )

        return {
            "current_stability": current_stability,
            "stability_slope": stability_slope,
            "intervention_slope": intervention_slope,
            "projected_stability": projected_stability,
            "horizon": self.horizon,
            "risk_horizon": risk_horizon,
            "state": state
        }


# ===============================================
# DEMO RUN
# ===============================================

if __name__ == "__main__":

    engine = ContinuityProjection(horizon=5)

    demo = [
        (0.80, 0.60),
        (0.82, 0.58),
        (0.84, 0.55),
        (0.86, 0.50),
        (0.87, 0.47),
        (0.88, 0.45),
    ]

    for s, i in demo:
        engine.record(s, i)

    print("=== LAYER 78 — CONTINUITY PROJECTION ===")
    print(engine.evaluate())


def process(state):

    state["pressure"] *= 0.9995
    state["coherence"] = min(1.0, state.get("coherence",0)+0.0002)

    print({
        "layer": "78_continuity_projection",
        "status": "active"
    })

    return state
