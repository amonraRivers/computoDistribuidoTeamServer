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

if __name__ == "__main__":
    s, p = Server_Address.get_server_address("serverips.txt")
    ips = tuple((server, port) for server, port in zip(s, p))

    print("This is the setup_server.py file")
    mb = MessageBuffer()
    rb = ResponseBuffer()
    ob = OperationBuffer()

    mp = MessageProcessor(mb, ob)
    op = OperationExecutor(ob, rb)

    ss = Server_Socket(mb)

    sc = Client_Socket([], mb)

    sc.start()
    ss.start()
    sc_threads = sc.get_threads()
    ss_threads = ss.get_threads()
    sockets_threads = sc_threads + ss_threads

    rpc = RPCServer(mb, rb, ss, sc)
    rpc.start()
    mp.start()
    op.start()

    rpc.join()
    op.join()
    mp.join()
