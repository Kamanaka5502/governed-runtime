#!/usr/bin/env python3
"""
DATETIME FIX PATCH
Replaces deprecated utcnow() usage with timezone-aware UTC.
"""

from datetime import datetime, UTC

def now_iso():
    # canonical governed time
    return datetime.now(UTC).isoformat()

if __name__ == "__main__":
    print("datetime_fix OK:", now_iso())
