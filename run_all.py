import subprocess
import sys

TESTS = [
    "governed_runtime.py",
    "cognitive_margin_layer.py",
    "raft_failover_sim.py",
]

def run_test(file):
    print(f"\n===== RUNNING: {file} =====")
    result = subprocess.run(["python", file])
    if result.returncode != 0:
        print(f"\n❌ FAILED: {file}")
        sys.exit(1)
    print(f"✅ PASSED: {file}")

if __name__ == "__main__":
    print("=== GOVERNED RUNTIME ORCHESTRATOR ===")

    for t in TESTS:
        run_test(t)

    print("\n🔥 ALL SYSTEMS VERIFIED")
