def process(state):

    pressure = state.get("pressure", 0.0)

    if pressure < 0.4:
        mode = "stable"
    elif pressure < 0.7:
        mode = "watch"
    else:
        mode = "boundary_lock"

    state["mode"] = mode

    print({
        "layer": 21,
        "pressure": pressure,
        "mode": mode
    })

    return state
