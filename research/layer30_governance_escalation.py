# ============================================================
# Layer 30 — Governance Escalation Ladder
# Converts system signals into graded governance responses
# ============================================================

class GovernanceEscalation:
    def __init__(self):
        self.level = 0  # 0=normal,1=watch,2=guard,3=lockdown

    def observe(self, coherence, pressure, lock_active, cooldown_mode):
        risk_score = 0

        # signal weighting
        if coherence < 0.75:
            risk_score += 1
        if coherence < 0.55:
            risk_score += 1

        if pressure > 0.5:
            risk_score += 1
        if pressure > 0.75:
            risk_score += 1

        if lock_active:
            risk_score += 1

        if cooldown_mode:
            risk_score += 1

        # escalation mapping
        if risk_score <= 1:
            self.level = 0
            state = "normal_flow"
        elif risk_score <= 3:
            self.level = 1
            state = "watch_mode"
        elif risk_score <= 5:
            self.level = 2
            state = "guard_mode"
        else:
            self.level = 3
            state = "lockdown"

        return {
            "coherence": coherence,
            "pressure": pressure,
            "risk_score": risk_score,
            "escalation_level": self.level,
            "state": state
        }


if __name__ == "__main__":
    ge = GovernanceEscalation()

    demo = [
        (0.88, 0.20, False, False),  # stable
        (0.72, 0.55, False, False),  # mild tension
        (0.50, 0.70, True, False),   # guarded
        (0.35, 0.90, True, True),    # lockdown
        (0.80, 0.30, False, True),   # cooldown recovery
        (0.85, 0.25, False, False)   # fully stable
    ]

    print("=== LAYER 30 — GOVERNANCE ESCALATION ===")

    for c, p, lock, cd in demo:
        result = ge.observe(c, p, lock, cd)
        print(result)

def process(state):

    state["pressure"] *= 0.9995
    state["coherence"] = min(1.0, state.get("coherence",0)+0.0002)

    print({
        "layer": "30_governance_escalation",
        "status": "active"
    })

    return state
