# =========================================================
# GOVERNED RUNTIME LAYER — MARGINALIZED PROCESS
# =========================================================

MARGIN = 0.10   # global marginal influence (10%)

def process(state):

    # --- safe defaults ---
    pressure = state.get("pressure", 0.0)
    coherence = state.get("coherence", 0.0)
    energy = state.get("energy", 1.0)

    # --- tiny marginal adjustments ---
    pressure_delta = -0.002 * MARGIN
    coherence_delta = 0.001 * MARGIN
    energy_delta = -0.0005 * MARGIN

    pressure = max(0.0, pressure + pressure_delta)
    coherence = min(1.0, coherence + coherence_delta)
    energy = max(0.0, min(1.0, energy + energy_delta))

    # --- write back ---
    state["pressure"] = pressure
    state["coherence"] = coherence
    state["energy"] = energy

    print({
        "layer": __name__,
        "margin": MARGIN,
        "pressure": round(pressure, 4),
        "coherence": round(coherence, 4)
    })

    return state
