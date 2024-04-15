"""A class for communicating between the rpc , the nodes and the state machine."""

from queue import Queue

from operation import Operation


class OperationBuffer:
    """El Buffer de comunicacion"""

    def __init__(self):
        self.pq = Queue(100)

    def put(self, ms: Operation):
        """add an operation to teh queue"""
        self.pq.put(ms, block=True)
        #print("Agregando operacion a buffer de operaciones")

    def get(self):
        """get the first item"""
        res = self.pq.get(block=True)
        #print("Quitando operacion a buffer de operaciones")
        return res
