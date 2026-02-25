def process(state):
    """
    LAYER 59 — ATTRACTOR RUPTURE TEST
    Controlled instability injection to test recovery behavior.
    """

    import random

    # ---- CONTROLLED DISTURBANCE ----
    # small shock that pushes pressure + coherence in opposite directions
    shock = random.uniform(-0.05, 0.05)

    state["pressure"] = max(
        0.0,
        state.get("pressure", 0.0) + shock
    )

    state["coherence"] = max(
        0.0,
        state.get("coherence", 0.0) - (shock * 0.6)
    )

    # ---- TRACK EVENT ----
    state["rupture_event"] = True
    state["rupture_magnitude"] = round(shock, 4)

    print({
        "layer": 59,
        "rupture": True,
        "shock": round(shock, 4),
        "pressure": round(state["pressure"], 4),
        "coherence": round(state["coherence"], 4),
    })

    return state
