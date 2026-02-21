import subprocess
from execution_gate import ExecutionGate

print("\n=== GOVERNED RUNTIME ORCHESTRATOR (GUARDED) ===\n")

gate = ExecutionGate()

tasks = [
    ("governed_runtime.py", "run core governance tests"),
    ("cognitive_margin_layer.py", "stress cognitive layer"),
    ("raft_failover_sim.py", "cluster failover simulation"),
]

for script, description in tasks:

    print(f"\n--- REQUEST: {description} ---")

    allowed = gate.request_execution(description)

    if not allowed:
        print(f"⛔ SKIPPED: {script}")
        continue

    print(f"▶ RUNNING: {script}")
    subprocess.run(["python", script])

print("\n🔥 GUARDED ORCHESTRATION COMPLETE")
