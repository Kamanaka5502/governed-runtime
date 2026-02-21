import copy
from wal import WAL


class VersionConflict(Exception):
    pass


class CanonicalState:
    """
    Canonical state with WAL-backed atomic transitions.
    Disk (WAL) is the authority.
    """

    def __init__(self, wal_path="wal.log"):
        self.data = {}
        self.version = 0
        self.wal = WAL(wal_path)

    def snapshot(self):
        return copy.deepcopy(self.data)

    def apply_transition(self, event: dict):
        """
        Deterministic, idempotent transition.
        """
        new_data = self.snapshot()

        # Simple idempotent key-value merge
        for k, v in event.items():
            new_data[k] = v

        return new_data

    def _current_committed_version(self):
        """
        Count committed transitions in WAL.
        Disk truth.
        """
        entries = self.wal.read_all()
        committed = 0
        for e in entries:
            if e.get("status") == "committed":
                committed += 1
        return committed

    def transition(self, event: dict, expected_version: int) -> bool:
        """
        Atomic transition with strict version assertion.
        """

        # --- Sync with WAL ---
        canonical_version = self._current_committed_version()

        if canonical_version != self.version:
            raise VersionConflict(
                f"Local version {self.version} out of sync with WAL version {canonical_version}"
            )

        if expected_version != canonical_version:
            raise VersionConflict(
                f"Version mismatch: expected {expected_version}, actual {canonical_version}"
            )

        # --- Step 1: Write pending ---
        seq = self.wal.append({
            "event": event,
            "version_before": self.version
        })

        # --- Step 2: Apply ---
        try:
            new_data = self.apply_transition(event)
        except Exception as e:
            self.wal.mark_failed(seq, str(e))
            return False

        # --- Step 3: Commit ---
        self.data = new_data
        self.version += 1
        self.wal.mark_committed(seq)

        return True
