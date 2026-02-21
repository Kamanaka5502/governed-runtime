import os
import json


class LogEntry:
    def __init__(self, term, index, command):
        self.term = term
        self.index = index
        self.command = command

    def to_dict(self):
        return {
            "term": self.term,
            "index": self.index,
            "command": self.command,
        }

    @staticmethod
    def from_dict(d):
        return LogEntry(d["term"], d["index"], d["command"])


class StateMachine:
    def __init__(self):
        self.state = {}

    def update(self, command):
        for k, v in command.items():
            self.state[k] = v

    def __repr__(self):
        return str(self.state)


class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.log_path = f"{node_id}_raft.log"
        self.current_term = 0
        self.commit_index = -1
        self.log = []
        self.state_machine = StateMachine()

        self._load_log()

    # -------------------------
    # Log Loading / Recovery
    # -------------------------
    def _load_log(self):
        if not os.path.exists(self.log_path):
            return

        with open(self.log_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry_dict = json.loads(line)
                    entry = LogEntry.from_dict(entry_dict)
                    self.log.append(entry)
                except json.JSONDecodeError:
                    print(f"[{self.node_id}] Corrupted tail detected. Truncating.")
                    break

        # Repair invariant:
        # commit_index must never exceed last_log_index
        if self.log:
            self.commit_index = len(self.log) - 1
            for entry in self.log:
                self.state_machine.update(entry.command)
        else:
            self.commit_index = -1

    # -------------------------
    # Log Append
    # -------------------------
    def append_entry(self, entry):
        # Overwrite conflicting entries
        if entry.index < len(self.log):
            self.log = self.log[:entry.index]

        self.log.append(entry)

        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry.to_dict()) + "\n")
            f.flush()
            os.fsync(f.fileno())

        return True

    # -------------------------
    # Apply Commit
    # -------------------------
    def apply_committed(self):
        if 0 <= self.commit_index < len(self.log):
            entry = self.log[self.commit_index]
            self.state_machine.update(entry.command)

    def __repr__(self):
        return (
            f"<Node {self.node_id} "
            f"term={self.current_term} "
            f"commit_index={self.commit_index} "
            f"state={self.state_machine}>"
        )


# -------------------------
# Replication
# -------------------------
def replicate(leader, followers, command):
    index = len(leader.log)
    entry = LogEntry(leader.current_term, index, command)

    # Leader appends
    leader.append_entry(entry)

    acks = 1
    for f in followers:
        if f.append_entry(entry):
            acks += 1

    # Majority rule
    if acks > (len(followers) + 1) // 2:
        leader.commit_index = index
        leader.apply_committed()

        for f in followers:
            f.commit_index = min(index, len(f.log) - 1)
            f.apply_committed()

        return True

    return False
