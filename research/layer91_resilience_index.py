# =========================================================
# LAYER 91 — RESILIENCE INDEX
# Composite measure of recovery capacity
# =========================================================

def process(state):

    coherence = state.get("coherence", 0.0)
    pressure = state.get("pressure", 0.0)
    energy = state.get("energy", 1.0)

    resilience = (coherence * energy) - pressure

    state["resilience_index"] = resilience

    print({
        "layer": 91,
        "resilience_index": round(resilience, 4)
    })

    return state
