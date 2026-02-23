# ======================================================
# LAYER 05 — COMMIT INTEGRITY UNDER DISTURBANCE
# ======================================================

def process(state):

    committed = state.get("committed", False)

    disturbance = state.get("disturbance", 0.25)

    if committed:
        original_pressure = state.get("pressure", 0.0)

        simulated_pressure = original_pressure + disturbance

        # irreversible boundary behavior
        state["pressure"] = min(original_pressure, simulated_pressure) * 0.98

        rollback_attempt = True
        rollback_result = "REJECTED"

        state["mode"] = "LOCKED_COMMIT"

    else:
        rollback_attempt = False
        rollback_result = "NOT_COMMITTED"

    state["commit_integrity"] = rollback_result

    print({
        "layer": 5,
        "rollback_attempt": rollback_attempt,
        "result": rollback_result,
        "mode": state.get("mode")
    })

    return state
