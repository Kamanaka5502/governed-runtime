# ============================================================
# LAYER 98 — TRANSITION ACCEPTANCE
# "Change is allowed. Stability may evolve."
# ============================================================

def process(state):

    micro_seed = state.get("micro_seed", 0.0)
    pressure = state.get("pressure", 0.0)
    coherence = state.get("coherence", 0.0)
    emergence_state = state.get("emergence_state", "QUIET")

    # --------------------------------------------------------
    # TRANSITION PERMISSION
    # If emergence is active, reduce normalization pressure
    # slightly so the system can explore safe change.
    # --------------------------------------------------------

    transition_window = False
    adjustment = 0.0

    if emergence_state in ["SURGE", "ACTIVE"]:
        transition_window = True

        # gentle release of stabilizer tension
        adjustment = micro_seed * 0.08

        pressure += adjustment
        coherence -= abs(adjustment) * 0.2

    # keep safety bounds
    pressure = max(0.0, min(1.0, pressure))
    coherence = max(0.0, min(1.0, coherence))

    state["pressure"] = pressure
    state["coherence"] = coherence
    state["transition_window"] = transition_window
    state["transition_adjustment"] = round(adjustment, 6)

    print({
        "layer": "98_transition_acceptance",
        "transition_window": transition_window,
        "adjustment": round(adjustment, 6),
        "pressure": round(pressure, 4),
        "coherence": round(coherence, 4),
        "message": "CHANGE_ACCEPTED"
    })

    return state
