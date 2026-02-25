# ======================================================
# LAYER 58 — GOVERNANCE CONFLICT ENGINE
# Introduces competing governance pressures
# ======================================================

def process(state):

    pressure = state.get("pressure", 0.0)
    coherence = state.get("coherence", 0.0)
    trust = state.get("trust", 0.5)

    # --- competing forces ---
    safety_force = 1.0 - pressure
    performance_force = coherence + state.get("velocity", 0.0)
    operator_force = trust

    # normalized tension model
    tension = abs(safety_force - performance_force)

    # --- conflict detection ---
    conflict = tension > 0.25

    if conflict:

        # arbitration logic
        if operator_force >= 0.7:
            resolution = "OPERATOR_PRIORITY"
            state["pressure"] *= 0.98
            state["coherence"] *= 1.001

        elif safety_force > performance_force:
            resolution = "SAFETY_DOMINANT"
            state["pressure"] *= 0.95
            state["velocity"] *= 0.8

        else:
            resolution = "PERFORMANCE_DOMINANT"
            state["velocity"] = state.get("velocity", 0.0) + 0.05
            state["pressure"] *= 1.02

    else:
        resolution = "NO_CONFLICT"

    state["governance_conflict"] = conflict
    state["conflict_tension"] = round(tension, 4)
    state["conflict_resolution"] = resolution

    print({
        "layer": 58,
        "conflict": conflict,
        "tension": round(tension,4),
        "resolution": resolution
    })

    return state
