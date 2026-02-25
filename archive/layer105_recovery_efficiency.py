# layer105_recovery_efficiency.py
# Measures recovery quality instead of just stability

def process(state):

    confidence = state.get("confidence", state.get("coherence", 0.0))
    debt = state.get("adaptation_debt", state.get("debt", 0.0))
    prev_conf = state.get("prev_confidence", confidence)
    prev_debt = state.get("prev_debt", debt)

    conf_gain = confidence - prev_conf
    debt_reduction = max(prev_debt - debt, 0.0001)

    efficiency = conf_gain / debt_reduction

    state["recovery_efficiency"] = round(efficiency, 6)
    state["prev_confidence"] = confidence
    state["prev_debt"] = debt

    print({
        "layer": 105,
        "recovery_efficiency": state["recovery_efficiency"],
        "conf_gain": round(conf_gain, 6),
        "debt_reduction": round(debt_reduction, 6),
        "status": "MEASURED"
    })

    return state
