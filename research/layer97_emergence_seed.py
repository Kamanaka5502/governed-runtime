import random

def process(state):

    pressure = state.get("pressure", 0.1)
    coherence = state.get("coherence", 0.8)
    phase = state.get("phase", "BASELINE")

    # ===== CONTEXTUAL EMERGENCE =====
    if phase == "OPTIMAL":
        seed_scale = 0.03     # exploratory
    elif phase == "BASELINE":
        seed_scale = 0.015    # controlled
    else:
        seed_scale = 0.008    # conservative

    # pressure dampening
    seed_scale *= max(0.2, (1.0 - pressure))

    # coherence boost (stable systems can explore more)
    seed_scale *= (0.5 + coherence)

    micro_seed = random.uniform(-seed_scale, seed_scale)

    # classify emergence state
    magnitude = abs(micro_seed)
    if magnitude > 0.02:
        emergence_state = "ACTIVE"
    elif magnitude > 0.008:
        emergence_state = "SURGE"
    else:
        emergence_state = "QUIET"

    state["micro_seed"] = micro_seed
    state["emergence_state"] = emergence_state
    state.setdefault("emergence_history", []).append(emergence_state)

    print({
        "layer": 97,
        "micro_seed": round(micro_seed, 5),
        "pressure": round(pressure, 4),
        "coherence": round(coherence, 4),
        "emergence_state": emergence_state,
        "phase": phase
    })

    return state
