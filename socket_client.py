""" This file is responsible for creating a client socket that connects to the server socket. """

import socket
from threading import Thread

from connection_pool import ConnectionPool
from message_buffer import MessageBuffer
from socket_server import SocketConnection

HEADER = 1024
FORMAT = "utf-8"


class ClientSocket:
    """Client socket class."""

    def __init__(self, ips, mb: MessageBuffer):
        """Initialize the client socket."""
        self.ips = ips
        self.mb = mb

    def start(self, thread_pool: ConnectionPool):
        """Start the client."""
        #print("[STARTING] Client is starting")
        starting_threads = []

        for addr in self.ips:
            th = Thread(target=self.start_thread, args=(addr, thread_pool))
            th.start()
            starting_threads.append(th)

        #print("[FINISHED] Client has finished")

    def start_thread(self, addr, thread_pool: ConnectionPool):
        """Start the client thread."""
        try:
            #print(f"Trying to connect to {addr}")
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(addr)
            connection = SocketConnection(
                client,
                self.mb,
            )
            connection.start()
            thread_pool.add_connection(connection)
            #print(f"Connected to {addr}")
        except Exception as e:
            #print(f"Could not connect to {addr} {e}")
            pass


if __name__ == "__main__":

    ix = [("127.0.0.1", 5050)]

    mx = MessageBuffer()
    cs = ClientSocket(ips=ix, mb=mx)
    cs.start(ConnectionPool([]))
