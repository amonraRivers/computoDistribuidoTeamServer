import socket
import threading

HEADER = 64
FORMAT = "utf-8"
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

class Server_Socket:
    def __init__(self, server, Handle_Client):
        self.server = server
        self.handle_client = Handle_Client

    def start():
        print("[STARTING] Server is starting")
        server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}")
        while True:
            conn, addr = server.accept()            
            client = Handle_Client(conn, addr)
            client.recieve()


class Handle_Client:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.thread = threading.Thread(target=self.handle_client)
        
    def recieve(self):
        self.thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    
    def handle_client(self):
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
                    
                    print(f"[{addr}] {msg}")
                    conn.send("Msg recevied".encode(FORMAT))
        
        conn.close()
        
Server_Socket.start()