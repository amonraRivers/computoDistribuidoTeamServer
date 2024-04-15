""" A pool of connections """

from threading import Condition

from socket_connection import SocketConnection


class ConnectionPool:
    """Connection Pool"""

    def __init__(self, connections: list[SocketConnection]):
        """Constructor"""
        self.reply_condition: Condition | None = None
        self.connections = connections

    def get_connections(self):
        """Get connections"""
        return self.connections

    def add_connection(self, connection: SocketConnection):
        """Add connection"""
        self.connections.append(connection)

    def remove_connection(self, connection: SocketConnection):
        """Remove connection"""
        try:
            self.connections.remove(connection)
        except ValueError:
            pass

    def set_reply_condition(self, condition: Condition):
        """Set reply condition"""
        self.reply_condition = condition

    def send_to_all(self, message):
        """Send message to all connections"""
        for connection in self.connections:
            connection.send_to_out_queue(message)

    def send_to(self, message, connection_id: int):
        """Send message to a connection"""
        #print("Sending to", connection_id)
        conns = list(filter(lambda x: x.node_id == connection_id, self.connections))
        #print(len(conns), "conns")
        if len(conns) > 0:
            #print(conns[0].node_id)
            pass

        for conn in conns:
            conn.send_to_out_queue(message)

    def remove_duplicate_connections(self):
        """Remove duplicate connections"""
        dict_conn = {}
        for conn in self.connections:
            dict_conn[conn.node_id] = conn
        self.connections = list(dict_conn.values())

    def size(self):
        """Count only those that have a node id"""
        self.remove_duplicate_connections()
        return len(list(filter(lambda x: x.node_id != -1, self.connections)))
