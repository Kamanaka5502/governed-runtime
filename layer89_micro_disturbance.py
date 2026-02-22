# =========================================================
# LAYER 89 — MICRO DISTURBANCE INJECTOR
# Controlled turbulence to test stability response
# =========================================================

def process(state):

    pressure = state.get("pressure", 0.0)

    # tiny synthetic perturbation
    disturbance = 0.01

    pressure += disturbance

    state["pressure"] = pressure
    state["micro_disturbance"] = disturbance

    print({
        "layer": 89,
        "disturbance": disturbance,
        "pressure": round(pressure, 4)
    })

    return state
