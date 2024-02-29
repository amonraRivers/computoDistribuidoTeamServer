import socket

HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

SERVER = ["192.168.0.11", "192.168.0.12", "192.168.0.13"]
PORT = [5050, 5050, 5050]

ADDR_list = tuple((server, port) for server, port in zip(SERVER, PORT))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

for ADDR in ADDR_list:
    try:
        client.connect(ADDR)
    except:
        print(f"Could not connect to {ADDR}")
        ADDR_list = ADDR_list[1:]
        print(f"Trying to connect to {ADDR_list[0]}")

print(client.recv(2048).decode(FORMAT))

def send(msg):
    message = msg.encode(FORMAT)
    msg_lenght = len(message)
    send_lenght = str(msg_lenght).encode(FORMAT)
    send_lenght += b' ' * (HEADER - len(send_lenght))
    client.send(send_lenght)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))
