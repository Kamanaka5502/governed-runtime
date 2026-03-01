#!/usr/bin/env python3

import json
from datetime import datetime, UTC

EVENTS_FILE = "events.json"

def now_iso():
    return datetime.now(UTC).isoformat()

event = {
    "ts": now_iso(),
    "type": "SYSTEM_PATCH",
    "patch": "datetime_utc_upgrade",
    "reason": "remove_deprecated_utcnow",
    "status": "applied"
}

with open(EVENTS_FILE, "a", encoding="utf-8") as f:
    f.write(json.dumps(event, sort_keys=True) + "\n")

print("PATCH EVENT APPENDED")
