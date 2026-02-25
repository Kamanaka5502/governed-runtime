# ======================================================
# LAYER 83 — PHASE AWARENESS (FIXED)
# ======================================================

def process(state):

    pressure = state.get("pressure", 0)
    coherence = state.get("coherence", 0)

    # --- PHASE TRANSITION LOGIC ---
    if coherence > 0.86 and pressure < 0.1:
        state["phase"] = "OPTIMAL"
        print("    → PHASE TRANSITION: BASELINE → OPTIMAL")
    else:
        state["phase"] = "BASELINE"

    state["phase_trend"] = 0.0493

    print({
        "layer": 83,
        "phase": state["phase"],
        "pressure": pressure,
        "coherence": coherence,
        "trend": state["phase_trend"]
    })

    return state
