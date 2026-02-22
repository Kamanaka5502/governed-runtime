def process(state):

    pressure = state.get("pressure", 0.0)
    coherence = state.get("coherence", 1.0)

    risk = (pressure * 0.7) + ((1 - coherence) * 0.3)

    if risk > 0.7:
        classification = "UNSTABLE"
    elif risk > 0.4:
        classification = "STRAIN"
    else:
        classification = "STABLE"

    state["instability_risk"] = round(risk, 4)
    state["instability_classification"] = classification

    print({
        "layer": 71,
        "risk": round(risk, 4),
        "classification": classification,
        "pressure": pressure
    })

    return state
