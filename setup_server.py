"""Setup for the package."""

from message_buffer import MessageBuffer
from message_processor import MessageProcessor
from operation_buffer import OperationBuffer
from operation_executor import OperationExecutor
from response_buffer import ResponseBuffer
from rpc_server import RPCServer
from socket_server import Server_Socket

if __name__ == "__main__":
    print("This is the setup_server.py file")
    mb = MessageBuffer()
    rb = ResponseBuffer()
    ob = OperationBuffer()

    mp = MessageProcessor(mb, ob)
    op = OperationExecutor(ob, rb)

    rpc = RPCServer(mb, rb)
    ss = Server_Socket(mb)

    ss.start()
    rpc.start()
    mp.start()
    op.start()

    rpc.join()
    op.join()
    mp.join()
