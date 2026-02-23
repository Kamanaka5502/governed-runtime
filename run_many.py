#!/usr/bin/env python3

import subprocess
import json
from datetime import datetime, timezone

SUMMARY_FILE = "runtime_summary.jsonl"
TOTAL_RUNS = 1000


def run_runtime():
    """Execute governed runtime and return parsed final state if possible."""
    result = subprocess.run(
        ["python", "runtime_state_core.py"],
        capture_output=True,
        text=True
    )

    output = result.stdout

    state = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "success": result.returncode == 0,
        "raw_return_code": result.returncode,
    }

    # Optional parsing — grabs stability if present
    for line in output.splitlines():
        if "stability_score:" in line:
            try:
                state["stability_score"] = float(
                    line.split("stability_score:")[1].strip()
                )
            except Exception:
                pass
        elif "phase:" in line:
            try:
                state["phase"] = line.split("phase:")[1].strip()
            except Exception:
                pass
        elif "pressure:" in line:
            try:
                state["pressure"] = float(
                    line.split("pressure:")[1].strip()
                )
            except Exception:
                pass
        elif "coherence:" in line:
            try:
                state["coherence"] = float(
                    line.split("coherence:")[1].strip()
                )
            except Exception:
                pass

    return state


def main():
    print("=== FULL CAT LOOP START ===")

    with open(SUMMARY_FILE, "a") as f:
        for i in range(1, TOTAL_RUNS + 1):
            print(f"\n=== RUN {i}/{TOTAL_RUNS} ===")

            state = run_runtime()

            f.write(json.dumps(state) + "\n")
            f.flush()

            print(f"Logged run {i}")

    print("\n=== LOOP COMPLETE ===")


if __name__ == "__main__":
    main()

