# ==========================================================
# LAYER 52 — ADAPTIVE INTELLIGENCE MEMORY
# decision outcomes reshape intelligence behavior
# ==========================================================

import statistics

# ----------------------------------------------------------
# HYSTERESIS STABILITY
# ----------------------------------------------------------

class HysteresisStability:
    def __init__(self):
        self.state = "stable"

    def evaluate(self, pressure):
        prev = self.state

        if self.state == "stable":
            if pressure > 0.8:
                self.state = "critical"
            elif pressure > 0.6:
                self.state = "rising"

        elif self.state == "rising":
            if pressure > 0.85:
                self.state = "critical"
            elif pressure < 0.4:
                self.state = "stable"

        elif self.state == "critical":
            if pressure < 0.5:
                self.state = "recovering"

        elif self.state == "recovering":
            if pressure < 0.35:
                self.state = "stable"

        return self.state


# ----------------------------------------------------------
# PRESSURE GRADIENT
# ----------------------------------------------------------

class PressureGradient:
    def __init__(self):
        self.last = None

    def update(self, pressure):
        if self.last is None:
            delta = 0.0
        else:
            delta = pressure - self.last

        self.last = pressure
        return round(delta, 3)


# ----------------------------------------------------------
# PROJECTION ENGINE
# ----------------------------------------------------------

class ProjectionEngine:
    def __init__(self):
        self.samples = []

    def project(self, pressure):
        self.samples.append(pressure)
        if len(self.samples) < 2:
            return pressure

        delta = self.samples[-1] - self.samples[-2]
        projected = pressure + delta * 2
        return round(max(0.0, min(projected, 1.0)), 3)


# ----------------------------------------------------------
# INTELLIGENCE CORE (memory influenced)
# ----------------------------------------------------------

class IntelligenceCore:
    def __init__(self):
        self.history = []
        self.explore_bias = 1.0
        self.stabilize_bias = 1.0
        self.lockdown_bias = 1.0

    def decide(self, trust, pressure, delta, projection):

        score = (
            trust * 0.45 +
            (1.0 - pressure) * 0.35 +
            (1.0 - projection) * 0.20
        )

        # apply adaptive bias
        score *= self.explore_bias

        if projection > 0.9:
            mode = "LOCKDOWN"
        elif projection > 0.65 or delta > 0.15:
            mode = "STABILIZE"
        else:
            mode = "EXPLORE"

        return {
            "trust": round(trust, 3),
            "pressure": round(pressure, 3),
            "delta": delta,
            "projection": projection,
            "intelligence_score": round(score, 3),
            "cognitive_mode": mode
        }

    # ------------------------------------------------------
    # FEEDBACK LOOP (NEW)
    # ------------------------------------------------------

    def learn(self, decision, outcome):
        """
        outcome:
            1.0 = good result
            0.0 = bad result
        """

        mode = decision["cognitive_mode"]

        adjustment = (outcome - 0.5) * 0.1

        if mode == "EXPLORE":
            self.explore_bias += adjustment
        elif mode == "STABILIZE":
            self.stabilize_bias += adjustment
        else:
            self.lockdown_bias += adjustment

        # keep sane bounds
        self.explore_bias = max(0.5, min(1.5, self.explore_bias))
        self.stabilize_bias = max(0.5, min(1.5, self.stabilize_bias))
        self.lockdown_bias = max(0.5, min(1.5, self.lockdown_bias))

        self.history.append({
            "mode": mode,
            "outcome": outcome
        })

    def bias_snapshot(self):
        return {
            "explore": round(self.explore_bias, 3),
            "stabilize": round(self.stabilize_bias, 3),
            "lockdown": round(self.lockdown_bias, 3)
        }


# ----------------------------------------------------------
# FULL STACK ORCHESTRATOR
# ----------------------------------------------------------

class IntelligenceStack:

    def __init__(self):
        self.hysteresis = HysteresisStability()
        self.gradient = PressureGradient()
        self.projection = ProjectionEngine()
        self.core = IntelligenceCore()

    def step(self, trust, pressure, outcome):

        stability = self.hysteresis.evaluate(pressure)
        delta = self.gradient.update(pressure)
        projected = self.projection.project(pressure)

        decision = self.core.decide(
            trust=trust,
            pressure=pressure,
            delta=delta,
            projection=projected
        )

        self.core.learn(decision, outcome)

        return {
            "stability_state": stability,
            **decision,
            "bias": self.core.bias_snapshot()
        }


# ----------------------------------------------------------
# DEMO RUN
# ----------------------------------------------------------

if __name__ == "__main__":

    stack = IntelligenceStack()

    print("==== GOVERNED INTELLIGENCE STACK (52) ====")

    scenarios = [
        (0.75, 0.25, 0.9),
        (0.70, 0.45, 0.8),
        (0.65, 0.62, 0.7),
        (0.60, 0.78, 0.6),
        (0.55, 0.92, 0.4),
        (0.80, 0.35, 0.95),
    ]

    for trust, pressure, outcome in scenarios:
        print(stack.step(trust, pressure, outcome))

def process(state):

    state["pressure"] *= 0.9995
    state["coherence"] = min(1.0, state.get("coherence",0)+0.0002)

    print({
        "layer": "52_adaptive_intelligence",
        "status": "active"
    })

    return state
