from dataclasses import dataclass

@dataclass
class Signal:
    pressure: float

class PredictiveStabilizationController:
    def __init__(self):
        self.history = []
        self.margin = 1.0

    def slope(self):
        if len(self.history) < 2:
            return 0.0
        return self.history[-1] - self.history[-2]

    def acceleration(self):
        if len(self.history) < 3:
            return 0.0
        s1 = self.history[-1] - self.history[-2]
        s0 = self.history[-2] - self.history[-3]
        return s1 - s0

    def observe(self, signal):
        self.history.append(signal.pressure)

        current = signal.pressure
        trend = self.slope()
        accel = self.acceleration()

        predictive_pressure = current + (trend * 0.5) + (accel * 0.25)

        if predictive_pressure > 0.9:
            state = "anticipatory_saturation"
            pacing = 0.6
        elif predictive_pressure > 0.6:
            state = "pre_pressure"
            pacing = 0.8
        else:
            state = "stable"
            pacing = 1.0

        self.margin *= pacing
        self.margin = max(0.5, min(1.0, self.margin))

        return {
            "state": state,
            "raw": round(current,3),
            "trend": round(trend,3),
            "acceleration": round(accel,3),
            "predictive_pressure": round(predictive_pressure,3),
            "margin": round(self.margin,3),
            "pacing_modifier": pacing,
            "signals_recorded": len(self.history)
        }

    def render(self, status):
        print("\n=== LAYER 16 - PREDICTIVE STABILIZATION ===")
        for k,v in status.items():
            print(f"{k}: {v}")

if __name__ == "__main__":
    pc = PredictiveStabilizationController()

    demo = [
        Signal(0.15),
        Signal(0.3),
        Signal(0.55),
        Signal(0.82),  # rising fast → anticipatory trigger
        Signal(0.5)    # recovery
    ]

    for s in demo:
        status = pc.observe(s)
        pc.render(status)

