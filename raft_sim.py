class LogEntry:
    def __init__(self, term: int, index: int, command: dict):
        self.term = term
        self.index = index
        self.command = command


class Node:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.current_term = 0
        self.log = []
        self.commit_index = -1
        self.state_machine = {}

    def append_entry(self, entry: LogEntry):
        if entry.index != len(self.log):
            return False
        self.log.append(entry)
        return True

    def apply_committed(self):
        if self.commit_index >= 0:
            entry = self.log[self.commit_index]
            self.state_machine.update(entry.command)

    def __repr__(self):
        return f"<Node {self.node_id} term={self.current_term} commit_index={self.commit_index} state={self.state_machine}>"


def replicate(leader: Node, cluster: list, command: dict):
    index = len(leader.log)
    entry = LogEntry(leader.current_term, index, command)

    # Leader appends to itself
    leader.log.append(entry)

    # Send to followers
    acks = 1
    for node in cluster:
        if node is not leader:
            if node.append_entry(entry):
                acks += 1

    # Majority commit
    if acks > len(cluster) // 2:
        leader.commit_index = index
        leader.apply_committed()

        for node in cluster:
            node.commit_index = index
            node.apply_committed()

        return True

    return False


if __name__ == "__main__":
    print("---- RAFT SIMULATION ----")

    n1 = Node("A")
    n2 = Node("B")
    n3 = Node("C")

    cluster = [n1, n2, n3]

    leader = n1
    leader.current_term = 1

    print("\nReplicating command: role=engineer")
    replicate(leader, cluster, {"role": "engineer"})

    print(n1)
    print(n2)
    print(n3)

    assert n1.state_machine == n2.state_machine == n3.state_machine
    assert n1.state_machine == {"role": "engineer"}

    print("\n✓ Cluster converged with actual state replication")

