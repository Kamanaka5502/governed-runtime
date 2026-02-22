# =========================================================
# LAYER 86 — STABILITY GRADIENT
# Measures slope toward or away from stability.
# =========================================================

def process(state):

    pressure = state.get("pressure", 0.0)
    coherence = state.get("coherence", 1.0)

    gradient = coherence - pressure

    state["stability_gradient"] = round(gradient, 4)

    print({
        "layer": 86,
        "gradient": round(gradient, 4)
    })

    return state

