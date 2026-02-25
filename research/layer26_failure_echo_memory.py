# ============================================================
# Layer 26 — Failure Echo Memory
# Remembers recent fracture events and increases guard sensitivity
# ============================================================

class FailureEchoMemory:
    def __init__(self):
        self.echo_level = 0.0
        self.decay_rate = 0.1

    def observe(self, state, coherence):
        # raise echo when fracture occurs
        if state == "fracture_risk":
            self.echo_level = min(1.0, self.echo_level + 0.5)
        else:
            # gradual decay back toward calm
            self.echo_level = max(0.0, self.echo_level - self.decay_rate)

        # adaptive sensitivity influenced by echo
        guard_threshold = 0.6 + (0.2 * self.echo_level)

        mode = "normal"
        if coherence < guard_threshold:
            mode = "heightened_guard"

        return {
            "state": state,
            "coherence": round(coherence, 3),
            "echo_level": round(self.echo_level, 3),
            "guard_threshold": round(guard_threshold, 3),
            "mode": mode
        }


if __name__ == "__main__":
    fem = FailureEchoMemory()

    demo = [
        ("stable", 0.85),
        ("stable", 0.78),
        ("fracture_risk", 0.34),
        ("recovering", 0.55),
        ("recovering", 0.62),
        ("stable", 0.74),
        ("stable", 0.82),
    ]

    print("=== LAYER 26 — FAILURE ECHO MEMORY ===")

    for state, coherence in demo:
        result = fem.observe(state, coherence)
        print(result)

def process(state):

    state["pressure"] *= 0.9995
    state["coherence"] = min(1.0, state.get("coherence",0)+0.0002)

    print({
        "layer": "26_failure_echo_memory",
        "status": "active"
    })

    return state
