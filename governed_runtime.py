import time
import json
import uuid
from datetime import datetime

MEMORY_FILE = "canonical_memory.json"
EVENT_FILE = "events.jsonl"

def stamp_event(event_type, actor, payload=None):
    event = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "actor": actor,
        "payload": payload or {}
    }
    with open(EVENT_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")
    return event

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def commit_memory(key, value, session_id):
    memory = load_memory()

    # Rule 2: No silent contradiction
    if key in memory and memory[key] != value:
        stamp_event("conflict_detected", session_id, {
            "key": key,
            "existing": memory[key],
            "new": value
        })
        print(f"CONFLICT: '{key}' already set to '{memory[key]}'")
        return False

    memory[key] = value
    save_memory(memory)

    stamp_event("memory_commit", session_id, {
        "key": key,
        "value": value
    })
    return True

def inspect_memory():
    memory = load_memory()
    print(json.dumps(memory, indent=2))

def delete_memory(key):
    memory = load_memory()
    if key in memory:
        del memory[key]
        save_memory(memory)
        print(f"Deleted '{key}'")
    else:
        print("Key not found.")

def mock_llm_call(prompt):
    # Replace this with real API call later
    stamp_event("llm_call", "system", {"prompt": prompt})
    return f"Mock response to: {prompt}"

def process(user_input, session_id):
    stamp_event("request_received", session_id, {"input": user_input})

    response = mock_llm_call(user_input)

    stamp_event("response_generated", session_id, {"response": response})

    return response

if __name__ == "__main__":
    session = "user_" + str(uuid.uuid4())[:8]
    print("Governed Runtime CLI")
    print("Type 'inspect', 'delete <key>', or anything else to send to LLM.")
    while True:
        user_input = input("> ")

        if user_input == "inspect":
            inspect_memory()
            continue

        if user_input.startswith("delete "):
            _, key = user_input.split(" ", 1)
            delete_memory(key)
            continue

        if user_input.startswith("remember "):
            _, pair = user_input.split(" ", 1)
            key, value = pair.split("=", 1)
            commit_memory(key.strip(), value.strip(), session)
            continue

        response = process(user_input, session)
        print(response)
