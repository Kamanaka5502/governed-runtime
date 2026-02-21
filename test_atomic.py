from atomic_state import CanonicalState

# Fresh state
state = CanonicalState("wal.log")

print("Initial:", state.data, state.version)

state.transition({"role": "engineer"})
print("After 1:", state.data, state.version)

state.transition({"location": "kona"})
print("After 2:", state.data, state.version)
