from cassandra.cluster import Cluster, Session
from cassandra.policies import RoundRobinPolicy


def create_session(
    contact_points: list[str] | None = None,
    keyspace: str = "task_manager",
) -> Session:
    cluster = Cluster(
        contact_points=contact_points or ["127.0.0.1"],
        load_balancing_policy=RoundRobinPolicy(),
    )
    session = cluster.connect()
    session.set_keyspace(keyspace)
    return session
