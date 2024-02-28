"""A class for communicating between the rpc , the nodes and the state machine."""

from queue import PriorityQueue

from message import Message


class Buffer:
    """El Buffer de comunicacion"""

    def __init__(self):
        self.pq = PriorityQueue(100)

    def insert(self, ms: Message):
        """add an operation to teh queue"""
        self.pq.put(ms)

    def extract(self):
        """get the first item"""
        return self.pq.get()
