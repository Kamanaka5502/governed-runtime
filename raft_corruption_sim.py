import os
from raft_persistent import Node, replicate

LOGS = ["A_raft.log", "B_raft.log", "C_raft.log"]

def corrupt_last_line(path):
    """Simulate crash by truncating last 10 bytes of file."""
    with open(path, "rb+") as f:
        f.seek(0, os.SEEK_END)
        size = f.tell()
        if size > 10:
            f.truncate(size - 10)

if __name__ == "__main__":
    print("---- RAFT CORRUPTION SIM ----")

    # Clean old logs
    for f in LOGS:
        if os.path.exists(f):
            os.remove(f)

    # Build initial cluster
    A = Node("A")
    B = Node("B")
    C = Node("C")

    cluster = [B, C]
    A.current_term = 1

    # Initial replication
    replicate(A, cluster, {"role": "engineer"})
    replicate(A, cluster, {"location": "kona"})

    print("\nCluster before corruption:")
    print(A)
    print(B)
    print(C)

    # Corrupt B's log tail
    print("\nCorrupting B log tail...")
    corrupt_last_line("B_raft.log")

    # Restart nodes (simulate crash + recovery)
    print("\nRestarting cluster...")
    A2 = Node("A")
    B2 = Node("B")
    C2 = Node("C")

    print(A2)
    print(B2)
    print(C2)

    # Re-heal via leader replication
    print("\nRe-replicating to heal follower...")
    replicate(A2, [B2, C2], {"location": "kona"})

    print("\nCluster after healing:")
    print(A2)
    print(B2)
    print(C2)

    assert A2.state_machine == B2.state_machine == C2.state_machine

    print("\n✓ Tail corruption healed via leader replication")
    EOF
