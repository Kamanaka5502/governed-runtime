#!/data/data/com.termux/files/usr/bin/bash

echo "========================================"
echo "   GOVERNED RUNTIME — FULL CAT x10"
echo "========================================"

# ---------- RUN 1 : BASELINE ----------
unset NOISE_SCALE DRIFT_TEST CURIOSITY_FORCE HEAVY_MODE RESONANCE_TEST BOUNDARY_STRESS FINAL_SNAPSHOT
python runtime_state_core.py

# ---------- RUN 2 : GENTLE NOISE ----------
export NOISE_SCALE=0.01
python runtime_state_core.py

# ---------- RUN 3 : MEMORY DRIFT ----------
unset NOISE_SCALE
export DRIFT_TEST=1
python runtime_state_core.py

# ---------- RUN 4 : CURIOSITY PASS ----------
unset DRIFT_TEST
export CURIOSITY_FORCE=1
python runtime_state_core.py

# ---------- RUN 5 : CONTROLLED HEAVY ----------
unset CURIOSITY_FORCE
export HEAVY_MODE=1
python runtime_state_core.py

# ---------- RUN 6 : RECOVERY RESET ----------
unset HEAVY_MODE
python runtime_state_core.py

# ---------- RUN 7 : RESONANCE CHECK ----------
export RESONANCE_TEST=1
python runtime_state_core.py

# ---------- RUN 8 : BOUNDARY STRESS ----------
unset RESONANCE_TEST
export BOUNDARY_STRESS=2
python runtime_state_core.py

# ---------- RUN 9 : LONG STABILITY ----------
unset BOUNDARY_STRESS
python runtime_state_core.py

# ---------- RUN 10 : FINAL SNAPSHOT ----------
export FINAL_SNAPSHOT=1
python runtime_state_core.py

# ---------- CLEAN EXIT ----------
unset FINAL_SNAPSHOT

echo "========================================"
echo "FULL CAT x10 COMPLETE"
echo "========================================"
