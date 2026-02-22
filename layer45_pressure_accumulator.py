def process(state):

    velocity = state.get("velocity", 0.0)
    pressure = state.get("pressure", 0.0)

    # velocity increases pressure
    pressure += abs(velocity) * 0.5

    # clamp
    pressure = max(0.0, min(1.0, pressure))

    state["pressure"] = pressure

    print({
        "layer": 45,
        "velocity": velocity,
        "pressure": pressure
    })

    return state
