import socket
import threading

from message_buffer import MessageBuffer
from socket_server import SocketConnection

HEADER = 1024
FORMAT = "utf-8"


class Client_Socket:
    def __init__(self, ips, mb: MessageBuffer):
        self.ips = ips
        self.threads = []
        self.mb = mb

    def start(self):
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
            except:
                print(f"Could not connect to {addr}")

    def join(self):
        for thread in self.threads:
            thread.join()

    def get_threads(self):
        return self.threads


if __name__ == "__main__":

    ips = [("127.0.0.1", 5050)]

    mb = MessageBuffer()
    cs = Client_Socket(ips, mb)
    cs.start()
    cs.join()
