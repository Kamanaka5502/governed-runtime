# ============================================================
# LAYER 98 — CURIOSITY NUDGE
# Gentle exploratory bias for stable-but-quiet systems
# ============================================================

def process(state):

    coherence = state.get("coherence", 0.0)
    pressure = state.get("pressure", 0.0)
    emergence_state = state.get("emergence_state", "QUIET")
    phase = state.get("phase", "BASELINE")

    nudge = 0.0
    curiosity_active = False

    # --------------------------------------------------------
    # Only nudge when system is stable AND too quiet
    # --------------------------------------------------------
    if emergence_state == "QUIET" and coherence > 0.83 and pressure < 0.12:
        curiosity_active = True

        # very small exploratory perturbation
        nudge = 0.0015

        pressure += nudge
        coherence -= nudge * 0.15

    # safety bounds
    pressure = max(0.0, min(1.0, pressure))
    coherence = max(0.0, min(1.0, coherence))

    state["pressure"] = pressure
    state["coherence"] = coherence
    state["curiosity_active"] = curiosity_active
    state["curiosity_nudge"] = round(nudge, 6)

    print({
        "layer": "98_curiosity_nudge",
        "curiosity_active": curiosity_active,
        "nudge": round(nudge, 6),
        "pressure": round(pressure, 4),
        "coherence": round(coherence, 4),
        "message": "EXPLORE_ALLOWED"
    })

    return state
