#!/usr/bin/env bash
set -euo pipefail

EVENTS="events.jsonl"
HEAD="events.head"

echo "=== FULL FIX #2 ==="
echo "events: $EVENTS"
echo "head  : $HEAD"
echo

# 1) Verify current state
echo "[1/4] pre-verify..."
if python verify_events.py; then
  echo "VERIFY OK (no fix needed)"
  exit 0
fi

echo
echo "[2/4] attempting repair via rechaining..."
# You already have rechainer; use it to rebuild canonical chain
# (Adjust args if your rechainer signature differs.)
python rechain_events.py "$EVENTS" events.fixed.jsonl "$HEAD"

echo
echo "[3/4] swap in fixed chain (backup originals)..."
cp -v "$EVENTS" "events.pre_rechain.$(date +%s).bak"
mv -v events.fixed.jsonl "$EVENTS"

echo
echo "[4/4] regenerate head from canonical chain..."
python regen_head.py --events "$EVENTS" --head "$HEAD" --strict

echo
echo "post-verify..."
python verify_events.py

echo "=== FULL FIX #2 COMPLETE ==="
