# =========================================================
# LAYER 87 — RECOVERY INTENT
# Detects if system is naturally moving toward recovery.
# =========================================================

def process(state):

    gradient = state.get("stability_gradient", 0.0)
    momentum = state.get("phase_momentum", 0.0)

    intent = "NEUTRAL"

    if gradient > 0.6 and momentum < 0.3:
        intent = "RECOVERING"
    elif gradient < 0.2:
        intent = "UNSTABLE_TENDENCY"

    state["recovery_intent"] = intent

    print({
        "layer": 87,
        "intent": intent
    })

    return state

