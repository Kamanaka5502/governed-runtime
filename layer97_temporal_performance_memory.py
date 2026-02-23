# ======================================================
# LAYER 97 — TEMPORAL PERFORMANCE MEMORY
# ======================================================

import os
import json
from datetime import datetime

def process(state):
    """Track performance over time and detect trends"""
    
    history_file = "performance_history.json"
    
    # Load existing history
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history = json.load(f)
    else:
        history = {"runs": []}
    
    # Current run metrics (NOW stability_score exists)
    current_run = {
        "timestamp": datetime.now().isoformat(),
        "pressure": state.get("pressure", 0),
        "coherence": state.get("coherence", 0),
        "stability_score": state.get("stability_score", 0),  # ← Now calculated!
        "phase": state.get("phase", "UNKNOWN"),
        "resilience_index": state.get("resilience_index", 0),
    }
    
    # Add to history
    history["runs"].append(current_run)
    
    # Keep last 100 runs
    if len(history["runs"]) > 100:
        history["runs"] = history["runs"][-100:]
    
    # Calculate trends (if we have history)
    if len(history["runs"]) >= 2:
        recent = history["runs"][-10:]  # Last 10 runs
        
        avg_pressure = sum(r["pressure"] for r in recent) / len(recent)
        avg_coherence = sum(r["coherence"] for r in recent) / len(recent)
        avg_stability = sum(r["stability_score"] for r in recent) / len(recent)
        
        # Compare to previous average
        if len(history["runs"]) >= 20:
            previous = history["runs"][-20:-10]
            prev_stability = sum(r["stability_score"] for r in previous) / len(previous)
            
            trend = avg_stability - prev_stability
            
            if trend > 0.05:
                trend_direction = "IMPROVING"
            elif trend < -0.05:
                trend_direction = "DEGRADING"
            else:
                trend_direction = "STABLE"
        else:
            trend_direction = "INSUFFICIENT_DATA"
        
        state["temporal_awareness"] = {
            "total_runs": len(history["runs"]),
            "avg_pressure_recent": round(avg_pressure, 4),
            "avg_coherence_recent": round(avg_coherence, 4),
            "avg_stability_recent": round(avg_stability, 4),
            "trend": trend_direction,
        }
    else:
        state["temporal_awareness"] = {
            "total_runs": len(history["runs"]),
            "trend": "FIRST_RUN",
        }
    
    # Save updated history
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=2)
    
    print({
        "layer": 97,
        "total_runs": len(history["runs"]),
        "trend": state["temporal_awareness"].get("trend", "UNKNOWN"),
        "avg_stability": state["temporal_awareness"].get("avg_stability_recent", 0),
    })
    
    return state
