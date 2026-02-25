"""
LAYER 48 — GOVERNANCE HYSTERESIS

Purpose:
    Prevent oscillation when pressure hovers near thresholds.
    The system remembers prior state and uses different
    thresholds for escalation vs de-escalation.

Concept:
    - Escalation requires higher pressure.
    - Recovery requires lower pressure.
    - Creates stable bands between governance modes.
"""

class GovernanceHysteresis:

    def __init__(self):
        self.state = "flow"

        # Escalation thresholds
        self.flow_to_guard = 0.55
        self.guard_to_stabilize = 0.80

        # Recovery thresholds (lower — hysteresis gap)
        self.guard_to_flow = 0.40
        self.stabilize_to_guard = 0.65

    def evaluate(self, pressure):
        """
        pressure: float (0.0–1.0+)

        Returns structured governance decision.
        """

        previous_state = self.state

        # -----------------------------
        # STATE TRANSITIONS
        # -----------------------------
        if self.state == "flow":
            if pressure >= self.flow_to_guard:
                self.state = "guard"

        elif self.state == "guard":
            if pressure >= self.guard_to_stabilize:
                self.state = "stabilize"
            elif pressure <= self.guard_to_flow:
                self.state = "flow"

        elif self.state == "stabilize":
            if pressure <= self.stabilize_to_guard:
                self.state = "guard"

        transitioned = (previous_state != self.state)

        return {
            "pressure": round(pressure, 3),
            "previous_state": previous_state,
            "current_state": self.state,
            "transitioned": transitioned,
        }


# ======================================================
# DEMO / TEST RUN
# ======================================================

if __name__ == "__main__":

    gov = GovernanceHysteresis()

    print("=== LAYER 48 — GOVERNANCE HYSTERESIS ===")

    pressure_sequence = [
        0.30,  # flow
        0.50,  # still flow
        0.56,  # -> guard
        0.52,  # stays guard (no flip back)
        0.78,  # stays guard
        0.82,  # -> stabilize
        0.70,  # stays stabilize
        0.64,  # -> guard
        0.39,  # -> flow
    ]

    for p in pressure_sequence:
        result = gov.evaluate(p)
        print(result)


def process(state):

    state["pressure"] *= 0.9995
    state["coherence"] = min(1.0, state.get("coherence",0)+0.0002)

    print({
        "layer": "48_governance_hysteresis",
        "status": "active"
    })

    return state
