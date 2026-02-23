# ======================================================
# LAYER 02 — AUTHORITY SOURCE
# ======================================================

def process(state):

    if "authority" not in state:
        state["authority"] = "PRIMARY_OPERATOR"

    # trust alignment check
    if state.get("trust", 0) < 0.5:
        state["mode"] = "AUTHORITY_GUARD"

    print({
        "layer": 2,
        "authority": state["authority"],
        "trust": round(state.get("trust", 0), 4)
    })

    return state
