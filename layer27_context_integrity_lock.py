# ============================================================
# Layer 27 — Context Integrity Lock
# Prevents mutation/drift when system stability drops
# ============================================================

class ContextIntegrityLock:
    def __init__(self):
        self.lock_active = False

    def observe(self, coherence, echo_level):
        # activation condition
        if coherence < 0.55 or echo_level > 0.4:
            self.lock_active = True
        elif coherence > 0.75 and echo_level < 0.2:
            self.lock_active = False

        mutation_policy = "restricted" if self.lock_active else "open"

        return {
            "coherence": round(coherence, 3),
            "echo_level": round(echo_level, 3),
            "lock_active": self.lock_active,
            "mutation_policy": mutation_policy
        }


if __name__ == "__main__":
    cil = ContextIntegrityLock()

    demo = [
        (0.85, 0.0),
        (0.72, 0.1),
        (0.52, 0.5),  # lock triggers
        (0.60, 0.4),
        (0.78, 0.15), # lock releases
        (0.82, 0.05)
    ]

    print("=== LAYER 27 — CONTEXT INTEGRITY LOCK ===")

    for coherence, echo in demo:
        result = cil.observe(coherence, echo)
        print(result)

def process(state):

    state["pressure"] *= 0.9995
    state["coherence"] = min(1.0, state.get("coherence",0)+0.0002)

    print({
        "layer": "27_context_integrity_lock",
        "status": "active"
    })

    return state
