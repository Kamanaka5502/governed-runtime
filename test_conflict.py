import os
from atomic_state import CanonicalState, VersionConflict

# Clean WAL
if os.path.exists("wal.log"):
    os.remove("wal.log")

# Two runtimes sharing same WAL
runtime_a = CanonicalState("wal.log")
runtime_b = CanonicalState("wal.log")

print("Initial versions:")
print("A:", runtime_a.version)
print("B:", runtime_b.version)

# Both think version is 0

print("\nA committing...")
runtime_a.transition({"role": "engineer"}, expected_version=0)

print("A version:", runtime_a.version)
print("B still thinks version:", runtime_b.version)

print("\nB attempting conflicting commit...")

try:
    runtime_b.transition({"location": "kona"}, expected_version=0)
    print("❌ ERROR: Conflict was NOT detected")
except VersionConflict as e:
    print("✓ Conflict detected cleanly:")
    print(e)

print("\nFinal state A:", runtime_a.data, runtime_a.version)
print("Final state B:", runtime_b.data, runtime_b.version)
