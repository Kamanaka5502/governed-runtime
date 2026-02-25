import csv
import os
from datetime import datetime

LOG_FILE = "runtime_runs.csv"

FIELDS = [
    "timestamp",
    "stability_score",
    "coherence",
    "pressure",
    "instability_risk",
    "micro_seed",
    "phase",
    "mode"
]

def log_run(state):
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "timestamp": datetime.utcnow().isoformat(),
            "stability_score": state.get("stability_score"),
            "coherence": state.get("coherence"),
            "pressure": state.get("pressure"),
            "instability_risk": state.get("instability_risk"),
            "micro_seed": state.get("micro_seed"),
            "phase": state.get("phase"),
            "mode": state.get("mode"),
        })

    print("[LOGGER] Run appended to", LOG_FILE)
