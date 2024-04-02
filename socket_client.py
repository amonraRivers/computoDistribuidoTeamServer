""" This file is responsible for creating a client socket that connects to the server socket. """
import socket

from message_buffer import MessageBuffer
from socket_server import SocketConnection

HEADER = 1024
FORMAT = "utf-8"


class ClientSocket:
    """Client socket class."""
    def __init__(self, ips, mb: MessageBuffer):
        """Initialize the client socket."""
        self.ips = ips
        self.threads = []
        self.mb = mb

    def start(self):
        """Start the client."""
        print("[STARTING] Client is starting")

        for addr in self.ips:
            try:
                print(f"Trying to connect to {addr}")
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(addr)
                connection = SocketConnection(
                    client,
                    self.mb,
                )
                connection.start()
                self.threads.append(connection)
                print(f"Connected to {addr}")
            except Exception as e:
                print(f"Could not connect to {addr} {e}")

    def join(self):
        """Join the client."""
        for thread in self.threads:
            thread.join()

    def get_threads(self):
        """Get the threads."""
        return self.threads


if __name__ == "__main__":

    ix = [("127.0.0.1", 5050)]

    mx= MessageBuffer()
    cs = ClientSocket(ips=ix, mb=mx)
    cs.start()
    cs.join()
