import random

def process(state):

    # ==================================================
    # A) BOUNDARY STRESS TEST
    # ==================================================
    # Push load harder but controlled
    load_factor = state.get("heavy_load", 0.05)
    stress_multiplier = 5.0

    pressure = state.get("pressure", 0.1)
    coherence = state.get("coherence", 0.8)

    pressure += load_factor * stress_multiplier
    coherence -= load_factor * 0.6

    state["boundary_stress"] = True
    state["pressure"] = pressure
    state["coherence"] = coherence

    print({
        "layer": "98A_boundary_stress",
        "stress_multiplier": stress_multiplier,
        "pressure": round(pressure, 4),
        "coherence": round(coherence, 4),
        "message": "BOUNDARY_STRESS_APPLIED"
    })

    # ==================================================
    # B) NOISE INJECTION TEST
    # ==================================================
    noise = random.uniform(-0.05, 0.05)

    pressure += noise
    coherence -= abs(noise) * 0.2

    state["noise_value"] = noise
    state["pressure"] = pressure
    state["coherence"] = coherence

    print({
        "layer": "98B_noise_injection",
        "noise": round(noise, 5),
        "pressure": round(pressure, 4),
        "coherence": round(coherence, 4),
        "message": "CONTROLLED_NOISE_APPLIED"
    })

    # ==================================================
    # C) MEMORY DRIFT FIELD  (the spicy one)
    # ==================================================
    # Tracks recent seeds instead of instant-only state

    history = state.get("micro_seed_history", [])
    micro_seed = state.get("micro_seed", 0.0)

    history.append(micro_seed)

    # keep last 10 runs only
    if len(history) > 10:
        history = history[-10:]

    drift = sum(history) / len(history) if history else 0.0

    state["micro_seed_history"] = history
    state["drift_memory"] = drift

    # subtle adaptive influence
    pressure += drift * 0.3
    coherence -= abs(drift) * 0.15

    state["pressure"] = pressure
    state["coherence"] = coherence

    print({
        "layer": "98C_memory_drift",
        "history_len": len(history),
        "drift": round(drift, 6),
        "pressure": round(pressure, 4),
        "coherence": round(coherence, 4),
        "message": "DRIFT_FIELD_ACTIVE"
    })

    return state
