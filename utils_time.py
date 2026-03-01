#!/usr/bin/env python3
from __future__ import annotations
from datetime import datetime, timezone

def now_iso() -> str:
    # timezone-aware UTC (avoids utcnow deprecation)
    return datetime.now(timezone.utc).isoformat()
