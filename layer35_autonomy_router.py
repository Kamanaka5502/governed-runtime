# ==========================================================
# Layer 35 — Autonomy Decision Logic
# Routes execution mode based on governance signals
# ==========================================================

class AutonomyRouter:

    def __init__(self):
        self.history = []

    def route(self, coherence, risk, boundary_state):
        """
        Decide execution mode:
        - autonomous
        - collaborative
        - constrained
        """

        # base logic
        if boundary_state == "restricted":
            mode = "constrained"

        elif risk > 0.7:
            mode = "collaborative"

        elif coherence < 0.5:
            mode = "collaborative"

        else:
            mode = "autonomous"

        decision = {
            "coherence": round(coherence, 3),
            "risk": round(risk, 3),
            "boundary": boundary_state,
            "mode": mode
        }

        self.history.append(decision)
        return decision

    def summary(self):
        print("\n=== AUTONOMY ROUTING SUMMARY ===")

        total = len(self.history)
        auto = sum(1 for d in self.history if d["mode"] == "autonomous")
        collab = sum(1 for d in self.history if d["mode"] == "collaborative")
        constrained = sum(1 for d in self.history if d["mode"] == "constrained")

        print(f"Total decisions: {total}")
        print(f"Autonomous: {auto}")
        print(f"Collaborative: {collab}")
        print(f"Constrained: {constrained}")


# ==========================================================
# DEMO / TEST RUN
# ==========================================================

if __name__ == "__main__":

    ar = AutonomyRouter()

    demo = [
        (0.85, 0.2, "safe"),        # full autonomy
        (0.72, 0.55, "guarded"),    # still autonomous
        (0.48, 0.40, "guarded"),    # low coherence → collaborate
        (0.60, 0.82, "guarded"),    # high risk → collaborate
        (0.70, 0.90, "restricted"), # constrained
    ]

    print("=== LAYER 35 — AUTONOMY ROUTER ===")

    for c, r, b in demo:
        result = ar.route(c, r, b)
        print(result)

    ar.summary()

