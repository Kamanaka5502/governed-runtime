# ======================================================
# LAYER 03 — ADMISSIBILITY RULES
# ======================================================

def process(state):

    pressure = state.get("pressure", 0)
    coherence = state.get("coherence", 0)

    admissible = (
        pressure < 0.8 and
        coherence > 0.3
    )

    state["admissible"] = admissible

    if not admissible:
        state["mode"] = "REJECT_INPUT"

    print({
        "layer": 3,
        "admissible": admissible,
        "pressure": round(pressure, 4),
        "coherence": round(coherence, 4)
    })

    return state
