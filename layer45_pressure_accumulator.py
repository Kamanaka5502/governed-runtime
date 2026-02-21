# ==========================================================
# Layer 45 — Governance Pressure Accumulator
# Tracks long-term decision pressure and stabilization load
# ==========================================================

import json
import os

STATE_FILE = "governance_state.json"

class PressureAccumulator:

    def __init__(self):
        self.weights = {
            "safe": 1.0,
            "guarded": 1.0,
            "restricted": 1.0
        }
        self.pressure = 0.0
        self.history = []
        self.load()

    # ------------------------------------------------------
    # LOAD / SAVE
    # ------------------------------------------------------
    def load(self):
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r") as f:
                data = json.load(f)
                self.weights = data.get("weights", self.weights)
                self.pressure = data.get("pressure", 0.0)
                self.history = data.get("pressure_history", [])

    def save(self):
        data = {
            "weights": self.weights,
            "pressure": self.pressure,
            "pressure_history": self.history[-100:]
        }
        with open(STATE_FILE, "w") as f:
            json.dump(data, f, indent=2)

    # ------------------------------------------------------
    # UPDATE PRESSURE
    # ------------------------------------------------------
    def update(self, boundary, velocity_mode):

        delta = 0.0

        # boundary contribution
        if boundary == "restricted":
            delta += 0.25
        elif boundary == "guarded":
            delta += 0.10
        else:
            delta -= 0.05

        # velocity contribution
        if velocity_mode == "slow_verify":
            delta += 0.20
        elif velocity_mode == "deliberate":
            delta += 0.05
        else:
            delta -= 0.10

        # apply + clamp
        self.pressure += delta
        self.pressure = max(0.0, min(1.5, self.pressure))

        self.history.append(round(self.pressure, 3))

        return {
            "boundary": boundary,
            "velocity_mode": velocity_mode,
            "delta": round(delta, 3),
            "pressure": round(self.pressure, 3)
        }

    # ------------------------------------------------------
    # SIGNAL STATE
    # ------------------------------------------------------
    def signal(self):

        p = self.pressure

        if p < 0.3:
            state = "stable"
        elif p < 0.8:
            state = "elevated"
        else:
            state = "critical_load"

        return {
            "pressure": round(p, 3),
            "state": state
        }


# ==========================================================
# DEMO RUN
# ==========================================================

if __name__ == "__main__":

    pa = PressureAccumulator()

    print("=== LAYER 45 — PRESSURE ACCUMULATOR ===")

    demo = [
        ("safe", "fast_execute"),
        ("guarded", "deliberate"),
        ("restricted", "slow_verify"),
        ("guarded", "deliberate"),
        ("restricted", "slow_verify"),
    ]

    for b, v in demo:
        print(pa.update(b, v))

    print("\nSignal:", pa.signal())

    pa.save()
    print("State saved.")
