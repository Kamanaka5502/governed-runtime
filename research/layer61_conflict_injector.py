# =========================================================
# LAYER 61 — CONFLICT INJECTOR
# Introduces bounded opposition between stability and drift
# =========================================================

import random

def process(state):

    # tiny bounded perturbation
    conflict_force = random.uniform(-0.02, 0.02)

    # one axis pushes pressure
    state["pressure"] += conflict_force

    # opposite axis compensates coherence
    state["coherence"] -= conflict_force * 0.6

    # clamp safety
    state["pressure"] = max(0.0, min(1.0, state["pressure"]))
    state["coherence"] = max(0.0, min(1.0, state["coherence"]))

    state["conflict_injected"] = True
    state["conflict_force"] = round(conflict_force, 4)

    print({
        "layer": 61,
        "conflict_force": round(conflict_force,4),
        "pressure": round(state["pressure"],4),
        "coherence": round(state["coherence"],4),
        "status": "ACTIVE_CONFLICT"
    })

    return state
