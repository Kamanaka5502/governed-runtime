import time


class LogEntry:
    def __init__(self, term, index, command):
        self.term = term
        self.index = index
        self.command = command


class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.current_term = 0
        self.log = []
        self.commit_index = -1
        self.state_machine = {}

    def append_entry(self, term, prev_log_index, prev_log_term, entry):
        # Log matching rule
        if prev_log_index >= 0:
            if prev_log_index >= len(self.log):
                return False
            if self.log[prev_log_index].term != prev_log_term:
                return False

        # If conflicting entry exists, delete it
        if entry.index < len(self.log):
            self.log = self.log[:entry.index]

        self.log.append(entry)
        return True

    def apply_committed(self):
        while self.commit_index + 1 < len(self.log):
            self.commit_index += 1
            cmd = self.log[self.commit_index].command
            self.state_machine.update(cmd)

    def __repr__(self):
        return f"<Node {self.node_id} term={self.current_term} log_len={len(self.log)} state={self.state_machine}>"


def replicate(leader, followers, command):
    index = len(leader.log)
    entry = LogEntry(leader.current_term, index, command)

    prev_index = index - 1
    prev_term = leader.log[prev_index].term if prev_index >= 0 else -1

    leader.log.append(entry)

    acks = 1

    for f in followers:
        if f.append_entry(leader.current_term, prev_index, prev_term, entry):
            acks += 1

    if acks > (len(followers) + 1) // 2:
        leader.commit_index = index
        leader.apply_committed()
        for f in followers:
            f.commit_index = index
            f.apply_committed()


if __name__ == "__main__":
    print("---- RAFT LOG CONSISTENCY SIM ----")

    leader = Node("Leader")
    f1 = Node("F1")
    f2 = Node("F2")

    cluster = [f1, f2]

    leader.current_term = 1

    replicate(leader, cluster, {"role": "engineer"})
    replicate(leader, cluster, {"location": "kona"})

    for n in [leader, f1, f2]:
        print(n)

    assert leader.state_machine == f1.state_machine == f2.state_machine
    print("\n✓ Log consistency enforced")
