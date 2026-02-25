# ======================================================
# LAYER 100 — ADAPTIVE POLICY SHIFT
# ======================================================

def process(state):

    rating = state.get("performance_rating", "UNKNOWN")
    phase = state.get("phase", "BASELINE")
    pressure = state.get("pressure", 0.0)

    adjustment = 0.0
    shift = "NONE"

    # --- adaptation rules ---
    if rating == "ABOVE_AVERAGE":
        adjustment = -0.005
        shift = "STABILITY_REINFORCEMENT"

    elif rating == "BELOW_AVERAGE":
        adjustment = 0.008
        shift = "RECOVERY_ADAPTATION"

    elif phase == "OPTIMAL":
        adjustment = -0.002
        shift = "OPTIMAL_HOLD"

    # apply safely
    pressure = max(0.0, pressure + adjustment)

    state["pressure"] = pressure
    state["policy_shift"] = shift
    state["policy_adjustment"] = adjustment

    print({
        "layer": 100,
        "policy_shift": shift,
        "adjustment": adjustment,
        "pressure": round(pressure, 4)
    })

    return state
