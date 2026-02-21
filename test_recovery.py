import os
from atomic_state import CanonicalState
from recovery import RecoveryEngine

# Simulate normal operations
state = CanonicalState("wal.log")
state.transition({"role": "engineer"})
state.transition({"location": "kona"})

print("Before crash:", state.data, state.version)

# Simulate crash by reloading from WAL
recovered = RecoveryEngine("wal.log").recover()

print("Recovered:", recovered.data, recovered.version)

assert recovered.data == state.data
assert recovered.version == state.version

print("✓ Crash recovery verified")
