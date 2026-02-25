def process(state):

    pressure = state.get("pressure", 0.0)

    if pressure > 0.8:
        mode = "CRITICAL"
    elif pressure > 0.5:
        mode = "GUARD"
    else:
        mode = "STABLE"

    state["mode"] = mode

    print({
        "layer": 21,
        "pressure": pressure,
        "mode": mode
    })

    return state
