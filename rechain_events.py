#!/usr/bin/env python3
from __future__ import annotations

import sys
import json
from typing import Any, Dict, List
from verify_events import legacy_hash

def write_head(head_path: str, head: str) -> None:
    with open(head_path, "w", encoding="utf-8") as f:
        f.write(head + "\n")

def main() -> int:
    if len(sys.argv) != 4:
        print("Usage: python rechain_events.py <in_events.jsonl> <out_events.jsonl> <head_file>")
        return 2

    in_path, out_path, head_path = sys.argv[1], sys.argv[2], sys.argv[3]

    prev = "0" * 64
    out_lines: List[str] = []
    count = 0

    with open(in_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            rec: Dict[str, Any] = json.loads(line)
            rec.pop("prev_hash", None)

            rec["prev"] = prev
            rec["hash"] = legacy_hash(rec)

            prev = rec["hash"]
            out_lines.append(json.dumps(rec, ensure_ascii=False) + "\n")
            count += 1

    with open(out_path, "w", encoding="utf-8") as out:
        out.writelines(out_lines)

    write_head(head_path, prev)

    print("RECHAIN OK")
    print("in_records:", count)
    print("out_records:", count)
    print("head:", prev)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
