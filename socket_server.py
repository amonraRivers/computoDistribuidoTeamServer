""" This module is responsible for creating the server socket and the connection socket."""
import socket
import threading
from queue import Queue
from time import sleep

from message import Message
from message_buffer import MessageBuffer
from operation import Operation

HEADER = 1024
FORMAT = "utf-8"
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
        self.thread = threading.Thread(target=self.create_connections)

    def start(self):
        """Start the server."""
        self.thread.start()

    def create_connections(self):
        """Create the connections."""
        print("[STARTING] Server is starting")
        self.server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}")
        while True:
            print("esperando")
            conn, _ = self.server.accept()
            client = SocketConnection(conn, self.mb)
            client.start()
            self.threads.append(client)

    def get_threads(self):
        """Get the threads."""
        return self.threads


class SocketConnection:
    """Socket connection class."""
    def __init__(self, conn, mb: MessageBuffer):
        """Initialize the socket connection."""
        self.conn = conn
        self.thread_incomming = threading.Thread(target=self.handle_incomming)
        self.thread_outgoing = threading.Thread(target=self.handle_outgoing)
        self.mb = mb
        self.out_queue = Queue()

    def start(self):
        """Start the connection."""
        self.thread_incomming.start()
        self.thread_outgoing.start()
        # print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    def handle_incomming(self):
        """Handle the incoming messages."""
        conn = self.conn
        while True:
            res = conn.recv(HEADER).decode(FORMAT)
            res = res.strip()
            if res:
                res = Message.from_string(res)
                self.mb.put(res)

    def handle_outgoing(self):
        """Handle the outgoing messages."""

        while True:
            m = self.out_queue.get()
            m = str(m)

            self.send(m)

    def send(self, msg):
        """Send the message."""
        conex = self.conn
        message = msg.encode(FORMAT)
        msg_lenght = len(message)
        message += b" " * (HEADER - len(message))
        conex.send(message)

    def join(self):
        """Join the connection."""
        self.thread_incomming.join()
        self.thread_outgoing.join()

    def get_out_queue(self):
        """Get the out queue."""
        return self.out_queue
