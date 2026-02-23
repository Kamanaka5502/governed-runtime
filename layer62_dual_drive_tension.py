# =========================================================
# LAYER 62 — DUAL DRIVE TENSION ENGINE
# Creates persistent internal conflict between stability
# and exploration forces.
# =========================================================

import random

def process(state):

    # --- baseline pulls ---
    stability_pull = (1.0 - state.get("pressure", 0.1)) * 0.01
    exploration_push = random.uniform(-0.006, 0.006)

    # --- net force ---
    tension = exploration_push - stability_pull

    # --- apply to state ---
    state["pressure"] = max(0.0, min(1.0,
                        state["pressure"] + tension))

    state["coherence"] = max(0.0, min(1.0,
                         state["coherence"] - (tension * 0.5)))

    state["dual_drive_tension"] = round(tension, 5)

    print({
        "layer": 62,
        "tension": state["dual_drive_tension"],
        "pressure": round(state["pressure"], 4),
        "coherence": round(state["coherence"], 4),
        "mode": "DUAL_DRIVE_ACTIVE"
    })

    return state
