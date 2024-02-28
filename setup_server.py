"""Setup for the package."""

from threading import Condition

from log import Log
from operation_executor import OperationExecutor
from response_queue import ResponseQueue
from rpc_server import RPCServer

if __name__ == "__main__":
    print("This is the setup_server.py file")
    log = Log()
    r = ResponseQueue()
    condition = Condition()
    executor = OperationExecutor(log, r, condition)
    server = RPCServer(log, r, condition)

    server.start()
    executor.start()

    server.join()
    executor.join()
