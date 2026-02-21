# ============================================================
# GOVERNED INTELLIGENCE STACK
# Layers 48–51 Unified
# ============================================================

import statistics

# ============================================================
# LAYER 48 — HYSTERESIS STABILITY
# ============================================================

class HysteresisStability:

    def __init__(self):
        self.last_state = "stable"

    def evaluate(self, pressure):

        if self.last_state == "stable":
            if pressure > 0.70:
                self.last_state = "rising"

        elif self.last_state == "rising":
            if pressure > 0.85:
                self.last_state = "critical"
            elif pressure < 0.50:
                self.last_state = "stable"

        elif self.last_state == "critical":
            if pressure < 0.60:
                self.last_state = "recovering"

        elif self.last_state == "recovering":
            if pressure < 0.40:
                self.last_state = "stable"

        return self.last_state


# ============================================================
# LAYER 49 — PRESSURE GRADIENT
# ============================================================

class PressureGradient:

    def __init__(self):
        self.history = []

    def update(self, pressure):

        self.history.append(pressure)

        if len(self.history) < 2:
            return 0.0

        delta = self.history[-1] - self.history[-2]
        return round(delta, 3)


# ============================================================
# LAYER 50 — PROJECTION ENGINE
# ============================================================

class ProjectionEngine:

    def __init__(self):
        self.history = []

    def project(self, pressure):

        self.history.append(pressure)

        if len(self.history) < 3:
            return pressure

        slope = statistics.mean([
            self.history[-1] - self.history[-2],
            self.history[-2] - self.history[-3]
        ])

        projected = pressure + slope
        return round(max(0.0, min(projected, 1.0)), 3)


# ============================================================
# LAYER 51 — INTELLIGENCE CORE
# ============================================================

class IntelligenceCore:

    def __init__(self):
        self.history = []

    def synthesize(self, trust, pressure, delta, projection):

        intelligence_score = (
            trust * 0.4 +
            (1 - pressure) * 0.3 +
            (1 - abs(delta)) * 0.2 +
            (1 - projection) * 0.1
        )

        return round(intelligence_score, 3)

    def choose_mode(self, trust, pressure, delta):

        if pressure > 0.85:
            return "LOCKDOWN"

        if delta > 0.15:
            return "STABILIZE"

        if trust > 0.7 and pressure < 0.4:
            return "EXPLORE"

        return "ADAPT"

    def decide(self, trust, pressure, delta, projection):

        score = self.synthesize(trust, pressure, delta, projection)
        mode = self.choose_mode(trust, pressure, delta)

        decision = {
            "trust": round(trust, 3),
            "pressure": round(pressure, 3),
            "delta": round(delta, 3),
            "projection": round(projection, 3),
            "intelligence_score": score,
            "cognitive_mode": mode
        }

        self.history.append(decision)
        return decision


# ============================================================
# FULL STACK ORCHESTRATOR
# ============================================================

class IntelligenceStack:

    def __init__(self):
        self.hysteresis = HysteresisStability()
        self.gradient = PressureGradient()
        self.projection = ProjectionEngine()
        self.core = IntelligenceCore()

    def step(self, trust, pressure):

        state = self.hysteresis.evaluate(pressure)
        delta = self.gradient.update(pressure)
        projected = self.projection.project(pressure)

        decision = self.core.decide(
            trust=trust,
            pressure=pressure,
            delta=delta,
            projection=projected
        )

        return {
            "stability_state": state,
            **decision
        }


# ============================================================
# DEMO RUN
# ============================================================

if __name__ == "__main__":

    stack = IntelligenceStack()

    print("=== GOVERNED INTELLIGENCE STACK (48–51) ===")

    scenarios = [
        (0.75, 0.25),
        (0.70, 0.45),
        (0.65, 0.62),
        (0.60, 0.78),
        (0.55, 0.92),
        (0.80, 0.35),
    ]

    for trust, pressure in scenarios:
        print(stack.step(trust, pressure))

