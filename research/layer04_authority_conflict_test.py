# ======================================================
# LAYER 04 — AUTHORITY CONFLICT TEST
# ======================================================

def process(state):

    primary = state.get("authority", "PRIMARY_OPERATOR")
    incoming = state.get("incoming_authority", "SECONDARY_OPERATOR")

    trust = state.get("trust", 0.0)

    conflict_detected = (primary != incoming)

    if conflict_detected:
        if trust >= 0.5:
            resolution = "PRIMARY_PRESERVED"
            state["authority"] = primary
        else:
            resolution = "AUTHORITY_GUARD"
            state["mode"] = "AUTHORITY_GUARD"
    else:
        resolution = "NO_CONFLICT"

    state["authority_conflict"] = conflict_detected
    state["authority_resolution"] = resolution

    print({
        "layer": 4,
        "conflict": conflict_detected,
        "resolution": resolution,
        "authority": state.get("authority")
    })

    return state
