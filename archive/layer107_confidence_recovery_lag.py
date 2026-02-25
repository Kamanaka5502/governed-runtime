# layer107_confidence_recovery_lag.py
# Measures how quickly confidence rebounds after stress

def process(state):

    coherence = state.get("coherence", 0.0)
    prev = state.get("prev_coherence", coherence)

    lag = max(prev - coherence, 0.0)

    smoothed = (state.get("confidence_lag", 0.0) * 0.8) + (lag * 0.2)

    state["confidence_lag"] = round(smoothed, 6)
    state["prev_coherence"] = coherence

    print({
        "layer": 107,
        "confidence_lag": state["confidence_lag"],
        "delta": round(lag, 6),
        "status": "RECOVERY_MONITOR"
    })

    return state
