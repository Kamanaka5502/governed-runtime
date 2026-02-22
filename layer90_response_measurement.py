# =========================================================
# LAYER 90 — RESPONSE MEASUREMENT
# Measures how coherence reacts after disturbance
# =========================================================

def process(state):

    pressure = state.get("pressure", 0.0)
    coherence = state.get("coherence", 0.0)

    response_ratio = coherence - pressure

    state["response_ratio"] = response_ratio

    print({
        "layer": 90,
        "response_ratio": round(response_ratio, 4)
    })

    return state
