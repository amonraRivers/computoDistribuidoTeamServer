import socket
import threading

from message import Message
from message_buffer import MessageBuffer

HEADER = 64
FORMAT = "utf-8"
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"


class Server_Socket:
    def __init__(self, mb: MessageBuffer, sb):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(ADDR)
        self.server = server

    def start(self):
        print("[STARTING] Server is starting")
        server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}")
        while True:
            conn, addr = server.accept()
            client = SocketConnection(conn, addr, mb)
            client.start()


class SocketConnection:
    def __init__(self, conn, addr, mb: MessageBuffer):
        self.conn = conn
        self.addr = addr
        self.thread_incomming = threading.Thread(target=self.handle_incomming)
        self.thread_outgoing = threading.Thread(target=self.handle_outgoing)
        self.mb = mb

    def start(self):
        self.thread_incomming.start()
        self.thread_outgoing.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    def handle_incomming(self):
        conn = self.conn
        addr = self.addr

        print(f"[NEW CONNECTION] {addr} connected.")
        conn.send(f"You are connected to {SERVER}".encode(FORMAT))

        connected = True
        while connected:
            msg_lenght = conn.recv(HEADER).decode(FORMAT)
            if msg_lenght:
                msg_lenght = int(msg_lenght)
                msg = conn.recv(msg_lenght).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                # message from string
                message = Message.from_string(msg)
                self.mb.put(message)
                print(f"[{addr}] {msg}")

        conn.close()

    def handle_outgoing(self):
        conn = self.conn
        addr = self.addr

        connected = True
        while connected:
            msg = self.mb.get_message()
            if msg:
                conn.send(msg.encode(FORMAT))

        conn.close()
