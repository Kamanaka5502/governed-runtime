def process(state):

    micro_seed = state.get("micro_seed", 0.0)
    pressure = state.get("pressure", 0.1)
    coherence = state.get("coherence", 0.8)

    # normalize influence (very small)
    adjustment = micro_seed * 0.05

    # apply tiny feedback loop
    state["phase_momentum"] = state.get("phase_momentum", 0.0) + adjustment

    # clamp to prevent chaos
    state["phase_momentum"] = max(
        -1.0,
        min(1.0, state["phase_momentum"])
    )

    print({
        "layer": 98,
        "micro_seed": round(micro_seed, 5),
        "adjustment": round(adjustment, 6),
        "phase_momentum": round(state["phase_momentum"], 4),
        "pressure": round(pressure, 4),
        "coherence": round(coherence, 4),
    })

    return state
