import socket
import threading

HEADER = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = ["192.168.0.11", "192.168.0.12", "192.168.0.13"]
PORT = [5050, 5050, 5050]

ADDR_list = tuple((server, port) for server, port in zip(SERVER, PORT))
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class Client_Socket:
    def __init__(self, client, Handle_Connection, ADDR_list):
        self.client = client
        self.handle_connection = Handle_Connection
        self.ADDR_list = ADDR_list
        
    def start(ADDR_list):
        print("[STARTING] Client is starting")
        
        for ADDR in ADDR_list:        
            try:
                print(f"Trying to connect to {ADDR}")
                conex = client.connect(ADDR)
                print(client.recv(2048).decode(FORMAT))
                Handle_Connection(conex)
            except:
                print(f"Could not connect to {ADDR}")
                ADDR_list = ADDR_list[1:]
                
class Handle_Connection:
    def __init__(self, conex):
        self.conex = conex
        self.thread = threading.Thread(target=self.handle_connection)
        
    def recieve(self):
        self.thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    
    def handle_connection(self):
        conex = self.conex
        conex.self.send(f"You are connected to {SERVER}")
        conex.self.send("DISCONNECT_MESSAGE")
        
    def send(self, msg):
        conex = self.conex
        message = msg.encode(FORMAT)
        msg_lenght = len(message)
        send_lenght = str(msg_lenght).encode(FORMAT)
        send_lenght += b' ' * (HEADER - len(send_lenght))
        conex.send(send_lenght)
        conex.send(message)
        print(conex.recv(HEADER).decode(FORMAT))
    
    #send (DISCONNECT_MESSAGE)


        
Client_Socket.start(ADDR_list)

### previous that works

#for ADDR in ADDR_list:
#    try:
#        client.connect(ADDR)
#    except:
#        print(f"Could not connect to {ADDR}")
#        ADDR_list = ADDR_list[1:]
#        print(f"Trying to connect to {ADDR_list[0]}")

# print(client.recv(2048).decode(FORMAT))

# def send(msg):
#    message = msg.encode(FORMAT)
#    msg_lenght = len(message)
# send_lenght = str(msg_lenght).encode(FORMAT)
#    send_lenght += b' ' * (HEADER - len(send_lenght))
#    client.send(send_lenght)
#    client.send(message)
#    print(client.recv(2048).decode(FORMAT))

### starts from here