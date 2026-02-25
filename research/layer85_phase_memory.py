# =========================================================
# LAYER 85 — PHASE MEMORY
# Keeps short history of behavioral phases.
# =========================================================

def process(state):

    history = state.get("phase_history", [])
    phase = state.get("phase", "BASELINE")

    history.append(phase)
    history = history[-10:]  # keep recent memory

    state["phase_history"] = history

    print({
        "layer": 85,
        "history_len": len(history),
        "recent": history[-3:]
    })

    return state

