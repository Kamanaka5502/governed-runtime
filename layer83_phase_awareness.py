# =========================================================
# LAYER 83 — PHASE AWARENESS
# Governing idea:
# Convert raw runtime telemetry into behavioral phase state.
# =========================================================

def process(state):

    pressure = state.get("pressure", 0.0)
    coherence = state.get("coherence", 1.0)
    velocity = state.get("velocity", 0.0)
    risk = state.get("instability_risk", 0.0)

    # ---- derive simple trend signal ----
    # (lightweight prediction — not heavy math)
    trend = (pressure * 0.6) + (velocity * 0.4)

    # ---- phase classification ----
    if coherence < 0.70 and pressure > 0.5:
        phase = "DRIFT_WARNING"

    elif pressure > 0.6 and velocity > 0.05:
        phase = "SURGE"

    elif pressure > 0.3 and trend > 0.2:
        phase = "RAMPING"

    elif pressure < 0.2 and velocity < 0.02:
        phase = "BASELINE"

    else:
        phase = "RECOVERY"

    # ---- write back to runtime ----
    state["phase"] = phase
    state["phase_trend"] = round(trend, 4)

    print({
        "layer": 83,
        "phase": phase,
        "pressure": round(pressure, 4),
        "velocity": round(velocity, 4),
        "coherence": round(coherence, 4),
        "trend": round(trend, 4)
    })

    return state

