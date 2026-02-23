# ======================================================
# LAYER FULL_CAP — EOS / GOVERNANCE CAP
# ======================================================

def process(state):

    # --- PRESERVE existing ecosystem ---
    # never replace state, only extend it
    state.update({
        "layer": "FULL_CAP",
        "status": "COMPLETE"
    })

    # --- REQUIRED INVARIANTS ---
    required = [
        "coherence",
        "pressure",
        "drift",
        "energy",
        "trust"
    ]

    missing = [k for k in required if k not in state]
    state["missing"] = missing

    # safety fallback (prevents KeyError explosions)
    state.setdefault("drift", 0.0)
    state.setdefault("energy", 1.0)
    state.setdefault("trust", 0.75)

    # --- EOS classification ---
    if state.get("pressure", 0) > 0.8:
        state["mode"] = "CRITICAL"
    elif state.get("pressure", 0) > 0.5:
        state["mode"] = "GUARD"
    else:
        state["mode"] = "STABLE"

    print({
        "layer": "FULL_CAP",
        "status": state["status"],
        "missing": state["missing"],
        "mode": state["mode"]
    })

    return state
