# layer108_noise_taper.py
# Reduces noise influence when stability is strong

def process(state):

    noise = state.get("noise_value", 0.0)
    stability = state.get("stability_score", 0.0)

    taper = max(0.2, 1.0 - stability)

    adjusted = noise * taper

    state["tapered_noise"] = round(adjusted, 6)

    print({
        "layer": 108,
        "noise": round(noise, 6),
        "taper": round(taper, 4),
        "tapered_noise": state["tapered_noise"],
        "status": "NOISE_TAPERED"
    })

    return state
