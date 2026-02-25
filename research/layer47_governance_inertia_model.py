"""
LAYER 47 — GOVERNANCE INERTIA MODEL

Purpose:
    Prevent rapid oscillation between governance states.
    Adds inertia so the system doesn't flip modes too easily.

Concept:
    Decisions carry momentum.
    Strong previous state resists abrupt change unless pressure builds.
"""

class GovernanceInertiaModel:

    def __init__(self):
        self.current_state = "flow"
        self.inertia_strength = 0.6   # resistance to change (0–1)

    def evaluate(self, proposed_state, pressure):
        """
        Inputs:
            proposed_state : flow | guard | stabilize
            pressure       : float (0.0–1.0+)

        Logic:
            - Small pressure changes respect inertia.
            - High pressure overrides inertia.
        """

        # Map state priority
        priority = {
            "flow": 1,
            "guard": 2,
            "stabilize": 3
        }

        current_priority = priority[self.current_state]
        proposed_priority = priority[proposed_state]

        # Difference in governance intensity
        delta = proposed_priority - current_priority

        # Inertia threshold scales with pressure
        threshold = self.inertia_strength * (1 - pressure)

        # Decide whether transition occurs
        if abs(delta) > threshold:
            self.current_state = proposed_state
            transitioned = True
        else:
            transitioned = False

        return {
            "pressure": round(pressure, 3),
            "proposed_state": proposed_state,
            "final_state": self.current_state,
            "transitioned": transitioned,
            "inertia_threshold": round(threshold, 3)
        }


# ======================================================
# DEMO / TEST RUN
# ======================================================

if __name__ == "__main__":

    model = GovernanceInertiaModel()

    print("=== LAYER 47 — GOVERNANCE INERTIA MODEL ===")

    tests = [
        ("guard", 0.20),
        ("stabilize", 0.30),
        ("stabilize", 0.90),
        ("flow", 0.10),
        ("flow", 0.95),
    ]

    for state, pressure in tests:
        result = model.evaluate(state, pressure)
        print(result)


def process(state):

    state["pressure"] *= 0.9995
    state["coherence"] = min(1.0, state.get("coherence",0)+0.0002)

    print({
        "layer": "47_governance_inertia_model",
        "status": "active"
    })

    return state
