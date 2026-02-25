"""
LAYER 46 — ADAPTIVE STABILITY GATE
Purpose:
    Convert trust + pressure + velocity into a system-wide stability state.
"""

class AdaptiveStabilityGate:

    def __init__(self):
        self.state = "flow"

    def evaluate(self, trust, pressure, velocity_mode):
        """
        Inputs:
            trust   : float (0.0–1.0)
            pressure: float (0.0–1.0+)
            velocity_mode: fast_execute | deliberate | slow_verify
        """

        # --- CRITICAL STABILIZATION ---
        if pressure >= 0.8:
            self.state = "stabilize"

        # --- LOW TRUST GUARD ---
        elif trust <= 0.45:
            self.state = "guard"

        # --- HIGH SPEED UNDER LOAD ---
        elif velocity_mode == "fast_execute" and pressure > 0.5:
            self.state = "guard"

        # --- NORMAL FLOW ---
        else:
            self.state = "flow"

        return {
            "trust": round(trust, 3),
            "pressure": round(pressure, 3),
            "velocity_mode": velocity_mode,
            "stability_state": self.state
        }


# ======================================================
# DEMO / TEST RUN
# ======================================================

if __name__ == "__main__":

    gate = AdaptiveStabilityGate()

    print("=== LAYER 46 — ADAPTIVE STABILITY GATE ===")

    tests = [
        (0.72, 0.20, "fast_execute"),
        (0.63, 0.55, "fast_execute"),
        (0.40, 0.35, "deliberate"),
        (0.60, 0.85, "slow_verify"),
    ]

    for t, p, v in tests:
        result = gate.evaluate(t, p, v)
        print(result)

def process(state):

    state["pressure"] *= 0.9995
    state["coherence"] = min(1.0, state.get("coherence",0)+0.0002)

    print({
        "layer": "46_adaptive_stability_gate",
        "status": "active"
    })

    return state
