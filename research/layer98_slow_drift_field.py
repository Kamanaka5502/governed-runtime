# ============================================================
# LAYER 98 — SLOW DRIFT FIELD
# "Momentum through tiny change."
# ============================================================

import random

def process(state):

    pressure = state.get("pressure", 0.0)
    coherence = state.get("coherence", 0.0)

    # --------------------------------------------------------
    # MICRO DRIFT
    # extremely small environmental shift each run
    # --------------------------------------------------------

    drift = random.uniform(-0.002, 0.002)

    pressure += drift * 0.6
    coherence -= abs(drift) * 0.15

    # safety bounds
    pressure = max(0.0, min(1.0, pressure))
    coherence = max(0.0, min(1.0, coherence))

    state["pressure"] = pressure
    state["coherence"] = coherence
    state["slow_drift"] = round(drift, 6)

    print({
        "layer": "98_slow_drift_field",
        "drift": round(drift, 6),
        "pressure": round(pressure, 4),
        "coherence": round(coherence, 4),
        "message": "MICRO_ADAPTATION_ACTIVE"
    })

    return state
