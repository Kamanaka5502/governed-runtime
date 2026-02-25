# layer63_phase_inertia.py
# Adds inertia to phase switching so transitions require sustained change.

def process(state):

    current_phase = state.get("phase", "BASELINE")
    prev_phase = state.get("prev_phase", current_phase)

    pressure = state.get("pressure", 0.1)
    trend = state.get("phase_trend", 0.0)

    # initialize inertia tracking
    state.setdefault("phase_hold_counter", 0)
    state.setdefault("phase_inertia", 0.0)

    # detect phase persistence
    if current_phase == prev_phase:
        state["phase_hold_counter"] += 1
    else:
        state["phase_hold_counter"] = 0

    hold = state["phase_hold_counter"]

    # inertia increases with stability duration
    inertia = min(1.0, hold / 25.0)

    # apply mild resistance if pressure trend is weak
    if abs(trend) < 0.02:
        inertia *= 1.25

    inertia = min(1.0, inertia)

    state["phase_inertia"] = round(inertia, 4)

    # optional: lock phase if inertia high
    if inertia > 0.75:
        state["phase_locked"] = True
    else:
        state["phase_locked"] = False

    print({
        "layer": 63,
        "phase": current_phase,
        "hold": hold,
        "trend": round(trend, 4),
        "inertia": round(inertia, 4),
        "locked": state["phase_locked"]
    })

    return state
