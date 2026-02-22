# =========================================================
# LAYER 88 — DRIFT PREDICTION
# Lightweight forward risk estimate.
# =========================================================

def process(state):

    pressure = state.get("pressure", 0.0)
    velocity = state.get("velocity", 0.0)
    gradient = state.get("stability_gradient", 0.0)

    drift_score = (pressure * 0.5) + (velocity * 0.3) - (gradient * 0.2)

    if drift_score > 0.4:
        prediction = "DRIFT_RISK"
    elif drift_score > 0.2:
        prediction = "WATCH"
    else:
        prediction = "STABLE_PATH"

    state["drift_prediction"] = prediction
    state["drift_score"] = round(drift_score, 4)

    print({
        "layer": 88,
        "prediction": prediction,
        "score": round(drift_score, 4)
    })

    return state

