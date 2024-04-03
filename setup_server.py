"""Setup for the package."""

from connection_pool import ConnectionPool
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
    ips_addresses = cs.get_nodes()
    rpc_server_address = cs.get_server_address()
    server_socket_address = cs.get_server_socket()

    socket_connection_pool = ConnectionPool([])

    print("This is the setup_server.py file")
    mb = MessageBuffer()
    rb = ResponseBuffer()
    ob = OperationBuffer()

    mp = MessageProcessor(mb, ob)
    mp.attach_connection_pool(socket_connection_pool)

    op = OperationExecutor(ob, rb)

    print(ips_addresses)
    ss = ServerSocket(server_socket_address, mb)
    sc = ClientSocket(ips_addresses, mb)
    rpc = RPCServer(rpc_server_address, mb, rb, socket_connection_pool)

    sc.start(socket_connection_pool)
    ss.start(socket_connection_pool)

    rpc.start()
    mp.start()
    op.start()

    rpc.join()
    op.join()
    mp.join()


if __name__ == "__main__":
    create_server("serverips.txt")
