# ======================================================
# LAYER 01 — IRREVERSIBLE COMMIT BOUNDARY
# ======================================================

def process(state):

    if state.get("committed", False):
        # once committed, pressure cannot increase fast
        state["pressure"] *= 0.98
        state["mode"] = "LOCKED_COMMIT"
    else:
        # trigger commit if coherence high enough
        if state.get("coherence", 0) > 0.80:
            state["committed"] = True
            state["mode"] = "COMMIT_BOUNDARY"

    print({
        "layer": 1,
        "committed": state.get("committed", False),
        "mode": state.get("mode")
    })

    return state
