# ==========================================================
# Layer 34 — Reflective Governance
# System analyzes its own decision trends
# ==========================================================

class ReflectiveGovernance:

    def __init__(self):
        self.history = []

    def log_decision(self, decision):
        """
        decision example:
        {
            "boundary": "safe/guarded/restricted",
            "decision": "...",
            "risk": 0.5
        }
        """
        self.history.append(decision)

    def analyze(self):
        print("\n=== REFLECTIVE GOVERNANCE ANALYSIS ===")

        if not self.history:
            print("No data.")
            return

        total = len(self.history)
        safe = sum(1 for d in self.history if d["boundary"] == "safe")
        guarded = sum(1 for d in self.history if d["boundary"] == "guarded")
        restricted = sum(1 for d in self.history if d["boundary"] == "restricted")

        avg_risk = sum(d["risk"] for d in self.history) / total

        print(f"Total decisions: {total}")
        print(f"Safe decisions: {safe}")
        print(f"Guarded decisions: {guarded}")
        print(f"Restricted decisions: {restricted}")
        print(f"Average risk: {round(avg_risk,3)}")

        # simple pattern detection
        if restricted / total > 0.4:
            print("Pattern: High restriction trend detected.")
        elif safe / total > 0.6:
            print("Pattern: High autonomy confidence.")
        else:
            print("Pattern: Balanced governance behavior.")

        # stabilization signal
        if avg_risk > 0.65:
            print("Signal: System operating under elevated pressure.")
        else:
            print("Signal: Normal operating envelope.")


# ==========================================================
# DEMO / TEST RUN
# ==========================================================

if __name__ == "__main__":

    rg = ReflectiveGovernance()

    demo_history = [
        {"boundary": "safe", "decision": "allow_autonomous", "risk": 0.2},
        {"boundary": "restricted", "decision": "restrict_or_escalate", "risk": 0.8},
        {"boundary": "guarded", "decision": "collaborative_check", "risk": 0.5},
        {"boundary": "guarded", "decision": "collaborative_check", "risk": 0.6},
        {"boundary": "safe", "decision": "allow_autonomous", "risk": 0.3},
    ]

    print("=== LAYER 34 — REFLECTIVE GOVERNANCE ===")

    for d in demo_history:
        rg.log_decision(d)

    rg.analyze()

