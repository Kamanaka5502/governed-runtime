# ============================================================
# Layer 28 — Recovery Proof Gate
# Requires sustained stability before reopening system freedom
# ============================================================

class RecoveryProofGate:
    def __init__(self, required_stable_steps=2):
        self.required_stable_steps = required_stable_steps
        self.stable_counter = 0
        self.gate_open = False

    def observe(self, coherence, lock_active):
        # recovery condition
        stable_now = (coherence > 0.75) and (not lock_active)

        if stable_now:
            self.stable_counter += 1
        else:
            self.stable_counter = 0
            self.gate_open = False

        # open only after repeated proof
        if self.stable_counter >= self.required_stable_steps:
            self.gate_open = True

        return {
            "coherence": round(coherence, 3),
            "lock_active": lock_active,
            "stable_counter": self.stable_counter,
            "gate_open": self.gate_open,
            "state": "verified_stable" if self.gate_open else "verifying"
        }


if __name__ == "__main__":
    rpg = RecoveryProofGate(required_stable_steps=2)

    demo = [
        (0.52, True),   # unstable
        (0.60, True),
        (0.78, False),  # recovery starts
        (0.81, False),  # proof achieved
        (0.84, False),  # remains open
        (0.65, False),  # instability resets
        (0.80, False),
        (0.82, False)
    ]

    print("=== LAYER 28 — RECOVERY PROOF GATE ===")

    for coherence, lock in demo:
        result = rpg.observe(coherence, lock)
        print(result)

def process(state):

    state["pressure"] *= 0.9995
    state["coherence"] = min(1.0, state.get("coherence",0)+0.0002)

    print({
        "layer": "28_recovery_proof_gate",
        "status": "active"
    })

    return state
