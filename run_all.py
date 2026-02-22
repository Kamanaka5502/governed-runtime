import glob
import subprocess
import os

print("=== GOVERNED RUNTIME ORCHESTRATOR ===")

layers = sorted(glob.glob("layer*.py"))

for layer in layers:
    print(f"\n--- Running {layer} ---")
    try:
        subprocess.run(["python", layer], check=False)
    except Exception as e:
        print(f"Error in {layer}: {e}")

print("\n=== RUNTIME COMPLETE ===")
