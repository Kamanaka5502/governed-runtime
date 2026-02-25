import random

def process(state):
    pattern = state.get("stress_pattern", "pulse")

    pressure = state.get("pressure", 0.1)
    coherence = state.get("coherence", 0.85)

    # === stress pattern selection ===
    if pattern == "pulse":
        # sudden spikes
        shock = random.choice([-0.02, 0.0, 0.04])

    elif pattern == "drift":
        # slow accumulation
        shock = state.get("drift_accum", 0.0) + 0.002
        state["drift_accum"] = shock

    elif pattern == "chaos":
        # randomized disturbance
        shock = random.uniform(-0.01, 0.03)

    else:
        shock = 0.0

    # === apply disturbance ===
    pressure += shock
    coherence -= abs(shock) * 0.6

    # clamp values
    pressure = max(0.0, pressure)
    coherence = max(0.0, coherence)

    state["pressure"] = pressure
    state["coherence"] = coherence

    result = {
        "layer": 60,
        "pattern": pattern,
        "shock": round(shock, 4),
        "pressure": round(pressure, 4),
        "coherence": round(coherence, 4),
    }

    print(result)
    return state
