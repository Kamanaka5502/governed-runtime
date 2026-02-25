# =========================================================
# LAYER 92 — RECOVERY PROBE
# Detects whether system naturally returns toward baseline
# =========================================================

def process(state):

    pressure = state.get("pressure", 0.0)

    recovering = pressure < 0.12

    state["recovery_probe"] = recovering

    print({
        "layer": 92,
        "recovering": recovering
    })

    return state
