# ======================================================
# LAYER 94 — STABILITY SCORING
# ======================================================

def process(state):
    """Calculate overall stability score BEFORE temporal layers"""
    
    # Calculate composite stability score
    stability_score = (
        state.get("coherence", 0) * 0.4 +
        (1.0 - state.get("pressure", 0)) * 0.3 +
        state.get("stability_gradient", 0.5) * 0.3
    )
    
    state["stability_score"] = round(stability_score, 4)
    
    print({
        "layer": 94,
        "stability_score": state["stability_score"],
        "calculated": True,
    })
    
    return state
