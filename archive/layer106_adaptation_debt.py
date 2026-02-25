# layer106_adaptation_debt.py
# Tracks unresolved adaptation pressure

def process(state):

    pressure = state.get("pressure", 0.0)
    coherence = state.get("coherence", 0.0)

    debt = max(pressure - coherence, 0.0)

    prev = state.get("adaptation_debt", 0.0)
    debt = (prev * 0.7) + (debt * 0.3)

    state["adaptation_debt"] = round(debt, 6)

    print({
        "layer": 106,
        "adaptation_debt": state["adaptation_debt"],
        "pressure": round(pressure, 4),
        "coherence": round(coherence, 4),
        "status": "TRACKING"
    })

    return state
