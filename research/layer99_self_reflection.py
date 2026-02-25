# ======================================================
# LAYER 99 — SELF-REFLECTION
# ======================================================

def process(state):
    """System reflects on its own performance trajectory"""
    
    temporal = state.get("temporal_awareness", {})
    rating = state.get("performance_rating", "UNKNOWN")
    trend = temporal.get("trend", "UNKNOWN")
    
    # Generate reflection
    reflections = []
    
    if trend == "IMPROVING":
        reflections.append("Performance trending positively")
    elif trend == "DEGRADING":
        reflections.append("Performance degradation detected")
    elif trend == "STABLE":
        reflections.append("Consistent performance maintained")
    
    if rating == "ABOVE_AVERAGE":
        reflections.append("Current run exceeds baseline")
    elif rating == "BELOW_AVERAGE":
        reflections.append("Current run below baseline")
    
    if state.get("phase") == "OPTIMAL":
        reflections.append("Optimal phase achieved")
    
    if state.get("stability_score", 0) > 0.85:
        reflections.append("High stability confirmed")
    
    state["self_reflection"] = reflections
    
    print({
        "layer": 99,
        "reflections": reflections,
        "self_awareness": "ACTIVE"
    })
    
    return state
