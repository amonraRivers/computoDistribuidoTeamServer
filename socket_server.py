import socket
import threading
from time import sleep

from message import Message
from message_buffer import MessageBuffer
from operation import Operation

HEADER = 1024
FORMAT = "utf-8"
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"


class Server_Socket:
    def __init__(self, mb: MessageBuffer):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)
        self.mb = mb
        self.thread = threading.Thread(target=self.create_connections)

    def start(self):
        self.thread.start()

    def create_connections(self):
        print("[STARTING] Server is starting")
        self.server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}")
        while True:
            print("esperando")
            conn, addr = self.server.accept()
            client = SocketConnection(conn, self.mb)
            client.start()


class SocketConnection:
    def __init__(self, conn, mb: MessageBuffer):
        self.conn = conn
        self.thread_incomming = threading.Thread(target=self.handle_incomming)
        self.thread_outgoing = threading.Thread(target=self.handle_outgoing)
        self.mb = mb

    def start(self):
        self.thread_incomming.start()
        self.thread_outgoing.start()
        # print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    def handle_incomming(self):
        conn = self.conn
        while True:
            res = conn.recv(HEADER).decode(FORMAT)
            res = res.strip()
            res = Message.from_string(res)
            self.mb.put(res)

    def handle_outgoing(self):
        conn = self.conn

        while True:
            sleep(1)
            m = str(Message(Operation("get", "a", 1), 1))
            print(m)
            self.send(m)

    def send(self, msg):
        conex = self.conn
        message = msg.encode(FORMAT)
        msg_lenght = len(message)
        send_lenght = str(msg_lenght).encode(FORMAT)
        send_lenght += b" " * (HEADER - len(send_lenght))
        conex.send(message)

    def join(self):
        self.thread_incomming.join()
        self.thread_outgoing.join()