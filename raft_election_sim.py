import time
import random


class Node:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.current_term = 0
        self.voted_for = None
        self.role = "follower"

        self.last_heartbeat = time.monotonic()
        self.election_timeout = random.uniform(0.15, 0.3)

    # ---------- Election ----------

    def start_election(self, cluster):
        self.role = "candidate"
        self.current_term += 1
        self.voted_for = self.node_id
        votes = 1

        for node in cluster:
            if node.node_id != self.node_id:
                if node.request_vote(self.current_term, self.node_id):
                    votes += 1

        if votes > len(cluster) // 2:
            self.role = "leader"
            self.last_heartbeat = time.monotonic()
            print(f"Node {self.node_id} became LEADER (term {self.current_term})")
        else:
            self.role = "follower"

    def request_vote(self, term: int, candidate_id: str):
        if term > self.current_term:
            self.current_term = term
            self.voted_for = None
            self.role = "follower"

        if term == self.current_term and self.voted_for in (None, candidate_id):
            self.voted_for = candidate_id
            return True

        return False

    # ---------- Heartbeats ----------

    def send_heartbeat(self, cluster):
        for node in cluster:
            if node.node_id != self.node_id:
                node.receive_heartbeat(self.current_term)

    def receive_heartbeat(self, term: int):
        if term >= self.current_term:
            self.current_term = term
            self.role = "follower"
            self.voted_for = None
            self.last_heartbeat = time.monotonic()

    # ---------- Tick Loop ----------

    def tick(self, cluster):
        now = time.monotonic()

        # Leader: send regular heartbeats
        if self.role == "leader":
            if now - self.last_heartbeat > 0.05:
                self.send_heartbeat(cluster)
                self.last_heartbeat = now
            return

        # Follower/Candidate: check election timeout
        if now - self.last_heartbeat > self.election_timeout:
            self.start_election(cluster)
            self.last_heartbeat = time.monotonic()

    def __repr__(self):
        return f"<Node {self.node_id} role={self.role} term={self.current_term}>"


# ---------------- SIMULATION ----------------

if __name__ == "__main__":
    print("---- RAFT ELECTION STABLE SIM ----")

    n1 = Node("A")
    n2 = Node("B")
    n3 = Node("C")

    cluster = [n1, n2, n3]

    start = time.monotonic()
    while time.monotonic() - start < 3:
        for n in cluster:
            n.tick(cluster)
        time.sleep(0.01)

    for n in cluster:
        print(n)

    leaders = [n for n in cluster if n.role == "leader"]
    assert len(leaders) == 1

    print("\n✓ Exactly one stable leader maintained")
