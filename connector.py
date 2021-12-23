from gqlalchemy import Memgraph


class Connector:
    """manages connection to Memgraph database"""
    def __init__(self, address="127.0.0.1", port=7687):
        self.memgraph = Memgraph(address, port)

    def execute(self, query):
        self.memgraph.execute(query)
        self.memgraph.get_indexes()

    def execute_and_fetch(self, query):
        return self.memgraph.execute_and_fetch(query)
