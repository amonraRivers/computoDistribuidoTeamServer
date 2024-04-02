"""Setup for the package."""

from message_buffer import MessageBuffer
from message_processor import MessageProcessor
from operation_buffer import OperationBuffer
from operation_executor import OperationExecutor
from response_buffer import ResponseBuffer
from rpc_server import RPCServer
from socket_client import ClientSocket
from socket_server import ServerSocket
from utils import ServerAddress


def create_server(file_name):
    """Create the server."""
    s, p = ServerAddress.get_server_address(file_name)
    ips = tuple((server, int(port)) for server, port in zip(s, p))

    print("This is the setup_server.py file")
    mb = MessageBuffer()
    rb = ResponseBuffer()
    ob = OperationBuffer()

    mp = MessageProcessor(mb, ob)
    op = OperationExecutor(ob, rb)

    print(ips)
    ss = ServerSocket(ips[1], mb)
    sc = ClientSocket(ips[2:], mb)
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
