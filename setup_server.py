"""Setup for the package."""

from message_buffer import MessageBuffer
from message_processor import MessageProcessor
from operation_buffer import OperationBuffer
from operation_executor import OperationExecutor
from response_buffer import ResponseBuffer
from rpc_server import RPCServer
from socket_client import Client_Socket
from socket_server import Server_Socket
from utils import Server_Address


def create_server(file_name):
    s, p = Server_Address.get_server_address(file_name)
    ips = tuple((server, int(port)) for server, port in zip(s, p))

    print("This is the setup_server.py file")
    mb = MessageBuffer()
    rb = ResponseBuffer()
    ob = OperationBuffer()

    mp = MessageProcessor(mb, ob)
    op = OperationExecutor(ob, rb)

    print(ips)
    ss = Server_Socket(ips[1], mb)
    sc = Client_Socket(ips[2:], mb)
    rpc = RPCServer(ips[0], mb, rb, ss, sc)

    sc.start()
    ss.start()

    rpc.start()
    mp.start()
    op.start()

    rpc.join()
    op.join()
    mp.join()


if __name__ == "__main__":
    create_server("serverips.txt")
