import json
import os
import time


class WAL:
    """
    Write-Ahead Log.
    Guarantees transitions are persisted before state mutation.
    """

    def __init__(self, path="wal.log"):
        self.path = path
        self.sequence = 0

        # Ensure file exists
        if not os.path.exists(self.path):
            open(self.path, "w").close()

        # Recover latest sequence number
        self._recover_sequence()

    def _recover_sequence(self):
        """Determine last used sequence number from WAL."""
        try:
            with open(self.path, "r") as f:
                for line in f:
                    entry = json.loads(line.strip())
                    if "seq" in entry:
                        self.sequence = max(self.sequence, entry["seq"])
        except Exception:
            # Corrupt WAL should halt higher layer
            pass

    def append(self, transition: dict) -> int:
        """
        Append transition to WAL with pending status.
        Returns sequence number.
        """
        self.sequence += 1

        entry = {
            "seq": self.sequence,
            "ts": time.monotonic_ns(),
            "status": "pending",
            "transition": transition
        }

        with open(self.path, "a") as f:
            f.write(json.dumps(entry) + "\n")
            f.flush()
            os.fsync(f.fileno())

        return self.sequence

    def mark_committed(self, seq: int):
        """
        Mark transition as committed.
        """
        entry = {
            "seq": seq,
            "ts": time.monotonic_ns(),
            "status": "committed"
        }

        with open(self.path, "a") as f:
            f.write(json.dumps(entry) + "\n")
            f.flush()
            os.fsync(f.fileno())

    def mark_failed(self, seq: int, reason: str):
        """
        Mark transition as failed.
        """
        entry = {
            "seq": seq,
            "ts": time.monotonic_ns(),
            "status": "failed",
            "reason": reason
        }

        with open(self.path, "a") as f:
            f.write(json.dumps(entry) + "\n")
            f.flush()
            os.fsync(f.fileno())

    def read_all(self):
        """
        Read all WAL entries.
        """
        entries = []
        with open(self.path, "r") as f:
            for line in f:
                if line.strip():
                    entries.append(json.loads(line.strip()))
        return entries
