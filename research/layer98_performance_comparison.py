# ======================================================
# LAYER 98 — PERFORMANCE COMPARISON
# ======================================================

def process(state):
    """Compare current run to historical performance"""
    
    temporal = state.get("temporal_awareness", {})
    
    if temporal.get("total_runs", 0) < 2:
        state["performance_rating"] = "BASELINE"
        print({
            "layer": 98,
            "rating": "BASELINE",
            "reason": "Insufficient history"
        })
        return state
    
    current_stability = state.get("stability_score", 0)
    avg_stability = temporal.get("avg_stability_recent", 0)
    
    # Compare current to average
    if current_stability > avg_stability + 0.05:
        rating = "ABOVE_AVERAGE"
        delta = "+"
    elif current_stability < avg_stability - 0.05:
        rating = "BELOW_AVERAGE"
        delta = "-"
    else:
        rating = "TYPICAL"
        delta = "="
    
    state["performance_rating"] = rating
    state["performance_delta"] = round(current_stability - avg_stability, 4)
    
    print({
        "layer": 98,
        "rating": rating,
        "delta": delta,
        "current": round(current_stability, 4),
        "average": round(avg_stability, 4),
    })
    
    return state
