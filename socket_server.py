""" This module is responsible for creating the server socket and the connection socket."""

import socket
from threading import Thread

from connection_pool import ConnectionPool
from message_buffer import MessageBuffer
from socket_connection import SocketConnection

SERVER = socket.gethostbyname(socket.gethostname())
DISCONNECT_MESSAGE = "!DISCONNECT"


class ServerSocket:
    """Server socket class."""

    def __init__(self, addr, mb: MessageBuffer):
        """Initialize the server socket."""
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(addr)
        self.mb = mb
        self.threads = []
        self.thread = None

    def start(self, thread_pool):
        """Start the server."""
        self.thread = Thread(target=self.create_connections, args=(thread_pool,))
        self.thread.start()

    def create_connections(self, thread_pool: ConnectionPool):
        """Create the connections."""
        print("[STARTING] Server is starting")
        self.server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}")
        while True:
            print("esperando")
            conn, address = self.server.accept()

            Thread(
                target=self.create_connection, args=(conn, address, thread_pool)
            ).start()

    def create_connection(self, conn, address, thread_pool: ConnectionPool):
        """Create the connection."""
        print(f"[NEW CONNECTION] {address} connected.")
        client = SocketConnection(conn, self.mb)
        client.start()
        thread_pool.add_connection(client)
