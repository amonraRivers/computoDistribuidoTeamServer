"""Setup for the package."""

from message_buffer import MessageBuffer
from message_processor import MessageProcessor
from operation_buffer import OperationBuffer
from operation_executor import OperationExecutor
from response_buffer import ResponseBuffer
from rpc_server import RPCServer
from socket_client import ClientSocket
from socket_server import ServerSocket
from utils import get_constants


def create_server(file_name):
    """Create the server."""


    cs = get_constants(file_name)
    ips = cs.get_nodes()
    rpc_server = cs.get_server_address()
    server_socket = cs.get_server_socket()


    print("This is the setup_server.py file")
    mb = MessageBuffer()
    rb = ResponseBuffer()
    ob = OperationBuffer()

    mp = MessageProcessor(mb, ob)
    op = OperationExecutor(ob, rb)

    print(ips)
    ss = ServerSocket(server_socket, mb)
    sc = ClientSocket(ips, mb)
    rpc = RPCServer(rpc_server, mb, rb, ss, sc)

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
