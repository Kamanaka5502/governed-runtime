<<<<<<< HEAD
import os
import json
import random
import time

STATE_FILE = "runtime_state.json"

# ===============================
# LOAD / SAVE STATE
# ===============================
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {
        "run_count": 0,
        "values": {
            "WATCH": 0.0,
            "PREEMPT": 0.0,
            "RECOVER": 0.0,
            "ANTICIPATE": 0.0
        },
        "learning_rate": 0.1
    }

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

state = load_state()
state["run_count"] += 1

VALUES = state["values"]
LEARNING_RATE = state["learning_rate"]

print("\n=== SIMPLE AI RUNTIME — INTELLIGENCE LAYER START ===\n")
print("RUN COUNT :", state["run_count"])
print("VALUES    :", VALUES)
print("LEARNING  :", LEARNING_RATE)

# ===============================
# GOALS (competing pressures)
# ===============================
GOALS = {
    "stability": 1.0,
    "efficiency": 0.8,
    "exploration": 0.4
}

# ===============================
# ENVIRONMENT DETECTION
# ===============================
def detect_environment(pressure, velocity):
    if pressure > 0.22:
        return "chaotic"
    elif abs(velocity) > 0.06:
        return "volatile"
    return "calm"

# ===============================
# FUTURE SIMULATION
# ===============================
def simulate_future(pressure, velocity, action):
    p = pressure
    v = velocity

    for _ in range(5):
        if action == "PREEMPT":
            p += v * 0.5
        elif action == "RECOVER":
            p -= abs(v) * 0.3
        elif action == "ANTICIPATE":
            p += v * 0.2
        else:  # WATCH
            p += v * 0.1

    return p

# ===============================
# ACTION CHOICE
# ===============================
def choose_action(pressure, velocity):
    actions = ["WATCH", "PREEMPT", "RECOVER", "ANTICIPATE"]
    env = detect_environment(pressure, velocity)

    best_action = None
    best_score = -999

    for action in actions:
        future_p = simulate_future(pressure, velocity, action)

        stability_reward = -abs(future_p - 0.15) * GOALS["stability"]
        efficiency_reward = -abs(velocity) * GOALS["efficiency"]

        exploration_bonus = 0
        if action == "ANTICIPATE":
            exploration_bonus = GOALS["exploration"]

        learned_value = VALUES[action]

        score = (
            stability_reward
            + efficiency_reward
            + exploration_bonus
            + learned_value
        )

        if env == "chaotic" and action == "RECOVER":
            score += 0.2
        if env == "calm" and action == "WATCH":
            score += 0.1

        if score > best_score:
            best_score = score
            best_action = action

    return best_action, env

# ===============================
# MAIN LOOP
# ===============================
pressure = 0.05
velocity = 0.0
avg_vel = 0.0
stability = 0.90

MAX_CYCLES = 200

for cycle in range(1, MAX_CYCLES + 1):

    # environmental drift
    velocity += random.uniform(-0.08, 0.08)
    pressure += velocity * 0.2
    pressure = max(0.0, min(0.5, pressure))

    avg_vel = (avg_vel * 0.9) + (velocity * 0.1)

    action, env = choose_action(pressure, velocity)

    # action effects
    if action == "RECOVER":
        pressure *= 0.9
        stability -= 0.01
    elif action == "PREEMPT":
        pressure += 0.02
        stability -= 0.003
    elif action == "ANTICIPATE":
        pressure += 0.01
        stability -= 0.001
    else:
        stability += 0.004

    stability = max(0.6, min(1.0, stability))

    # reward system
    reward = -abs(pressure - 0.15)

    VALUES[action] += LEARNING_RATE * reward

    # adaptive learning rate (meta learning)
    if reward < -0.15:
        LEARNING_RATE *= 0.98
    else:
        LEARNING_RATE *= 1.005

    LEARNING_RATE = max(0.01, min(0.2, LEARNING_RATE))

    confidence = max(0.7, min(1.0, stability))

    print("=" * 50)
    print(f"CYCLE      : {cycle}")
    print(f"MODE       : {action} ({env})")
    print(f"CONFIDENCE : {confidence:.3f}")
    print(f"VELOCITY   : {velocity:.4f}")
    print(f"AVG_VEL    : {avg_vel:.4f}")
    print(f"PRESSURE   : {pressure:.4f}")
    print(f"STABILITY  : {stability:.4f}")
    print(f"LEARNING   : {LEARNING_RATE:.4f}")
    print(f"VALUES     : {VALUES}")

    time.sleep(0.03)

# save state
state["values"] = VALUES
state["learning_rate"] = LEARNING_RATE
save_state(state)

print("\n=== STATE SAVED ===")
print("=== EOS ===")

=======
#!/usr/bin/env python3

import random
import json
import os
from collections import deque

# =====================================================
# SIMPLE AI RUNTIME — EMERGENT INTELLIGENCE CORE
# =====================================================

STATE_FILE = "runtime_state.json"

CYCLES = 80
TARGET_P = 0.15

ACTIONS = ["WATCH", "PREEMPT", "RECOVER", "ANTICIPATE"]

# -----------------------------------------------------
# LOAD MEMORY
# -----------------------------------------------------
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        memory = json.load(f)
else:
    memory = {}

memory.setdefault("run_count", 0)
memory.setdefault("action_value", {a: 0.0 for a in ACTIONS})

memory["run_count"] += 1
values = memory["action_value"]

# -----------------------------------------------------
# INITIAL STATE
# -----------------------------------------------------
state = {
    "pressure": 0.03,
    "stability": 0.90,
    "confidence": 1.0,
    "velocity": 0.0,
    "frustration": 0.0
}

vel_history = deque(maxlen=5)
prev_pressure = state["pressure"]

print("\n=== SIMPLE AI RUNTIME — EMERGENT INTELLIGENCE START ===\n")
print(f"RUN COUNT : {memory['run_count']}")
print(f"VALUES    : {values}\n")

# -----------------------------------------------------
# MAIN LOOP
# -----------------------------------------------------
for cycle in range(1, CYCLES + 1):

    # -------------------------------------------------
    # ENVIRONMENT INPUT
    # -------------------------------------------------
    shock = random.uniform(-0.05, 0.09)

    # mild attractor toward target
    drift = (TARGET_P - state["pressure"]) * 0.07

    state["pressure"] += shock + drift
    state["pressure"] = max(0.0, state["pressure"])

    # -------------------------------------------------
    # VELOCITY
    # -------------------------------------------------
    state["velocity"] = state["pressure"] - prev_pressure
    prev_pressure = state["pressure"]

    vel_history.append(state["velocity"])
    avg_vel = sum(vel_history) / len(vel_history)

    future_pressure = state["pressure"] + (avg_vel * 5)

    # -------------------------------------------------
    # PREDICTION ERROR (proto-world-model)
    # -------------------------------------------------
    prediction = state["pressure"] + avg_vel
    error = abs(prediction - future_pressure)

    # -------------------------------------------------
    # EXPLORATION CONTROL (frustration physics)
    # -------------------------------------------------
    if state["frustration"] > 0.4:
        explore_rate = 0.6
    else:
        explore_rate = 0.1

    if random.random() < explore_rate:
        action = random.choice(ACTIONS)
        reason = "explore"
    else:
        action = max(values, key=values.get)
        reason = "learned_policy"

    state["mode"] = action

    # -------------------------------------------------
    # GOVERNANCE ACTIONS
    # -------------------------------------------------
    if action == "RECOVER":
        state["pressure"] *= 0.75
        state["stability"] -= 0.01

    elif action == "PREEMPT":
        state["pressure"] *= 0.85
        state["stability"] -= 0.003

    elif action == "ANTICIPATE":
        state["stability"] -= 0.0015

    else:  # WATCH
        state["stability"] += 0.004

    # clamps
    state["stability"] = max(0.0, min(1.0, state["stability"]))

    # -------------------------------------------------
    # REWARD SYSTEM
    # -------------------------------------------------
    reward = 0.0

    error_term = abs(state["pressure"] - TARGET_P)

    if error_term < 0.05:
        reward += 1.0

    if state["stability"] > 0.92:
        reward += 0.5

    if state["pressure"] > 0.28:
        reward -= 1.0

    # prediction accuracy reward
    reward += max(0, 0.2 - error)

    # -------------------------------------------------
    # FRUSTRATION UPDATE
    # -------------------------------------------------
    if reward < 0:
        state["frustration"] += 0.05
    else:
        state["frustration"] *= 0.95

    state["frustration"] = min(1.0, state["frustration"])

    # -------------------------------------------------
    # UPDATE LEARNED VALUE
    # -------------------------------------------------
    values[action] += 0.1 * (reward - values[action])

    # slow decay (forces adaptation)
    for k in values:
        values[k] *= 0.999

    # -------------------------------------------------
    # CONFIDENCE DYNAMICS
    # -------------------------------------------------
    if abs(state["velocity"]) > 0.07:
        state["confidence"] -= 0.01
    else:
        state["confidence"] += 0.002

    state["confidence"] = max(0.85, min(1.0, state["confidence"]))

    # -------------------------------------------------
    # DISPLAY
    # -------------------------------------------------
    print("==================================================")
    print(f"CYCLE      : {cycle}")
    print(f"MODE       : {action} ({reason})")
    print(f"CONFIDENCE : {state['confidence']:.3f}")
    print(f"VELOCITY   : {state['velocity']:.4f}")
    print(f"AVG_VEL    : {avg_vel:.4f}")
    print(f"PRESSURE   : {state['pressure']:.4f}")
    print(f"FUTURE_P   : {future_pressure:.4f}")
    print(f"ERROR      : {error:.4f}")
    print(f"FRUSTRATE  : {state['frustration']:.3f}")
    print(f"STABILITY  : {state['stability']:.4f}")
    print(f"VALUES     : {values}")

# -----------------------------------------------------
# SAVE MEMORY
# -----------------------------------------------------
memory["action_value"] = values

with open(STATE_FILE, "w") as f:
    json.dump(memory, f, indent=2)

print("\n=== STATE SAVED ===")
print("=== EOS ===")
>>>>>>> 8b8fd77 (Add trend detector + saferoom promotion flow + governance drift tracking)
