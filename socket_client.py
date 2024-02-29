import socket
import threading
from time import sleep

from message import Message
from message_buffer import MessageBuffer
from socket_server import SocketConnection
from utils import Server_Address

HEADER = 1024
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
#SERVER = ["127.0.0.1"]
#PORT = [5050]

SERVER, PORT = Server_Address.get_server_address("serverips.txt")

ADDR_LIST = tuple((server, port) for server, port in zip(SERVER, PORT))
print(ADDR_LIST)

class Client_Socket:
    def __init__(self, mb: MessageBuffer):
        self.ADDR_LIST = ADDR_LIST
        self.threads = []
        self.mb = mb

    def start(self):
        print("[STARTING] Client is starting")

        for ADDR in ADDR_LIST:
            try:
                print(f"Trying to connect to {ADDR}")
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(ADDR)
                connection = SocketConnection(client, self.mb)
                connection.start()
                self.threads.append(connection)
                print(f"Connected to {ADDR}")
            except:
                print(f"Could not connect to {ADDR}")

    def join(self):
        for thread in self.threads:
            thread.join()


if __name__ == "__main__":
    
    mb = MessageBuffer()
    cs = Client_Socket(mb)
    cs.start()
    cs.join()
