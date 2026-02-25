# =========================================================
# LAYER 84 — PHASE MOMENTUM
# Tracks how fast phase state is changing.
# =========================================================

def process(state):

    prev_phase = state.get("prev_phase", "BASELINE")
    phase = state.get("phase", "BASELINE")

    momentum = 0.0
    if prev_phase != phase:
        momentum = 1.0
    else:
        momentum = max(0.0, state.get("phase_momentum", 0.0) * 0.9)

    state["phase_momentum"] = momentum
    state["prev_phase"] = phase

    print({
        "layer": 84,
        "phase": phase,
        "momentum": round(momentum, 4)
    })

    return state

