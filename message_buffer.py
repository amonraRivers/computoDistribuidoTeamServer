"""A class for communicating between the rpc , the nodes and the state machine."""

from queue import PriorityQueue

from message import Message


class MessageBuffer:
    """El Buffer de comunicacion"""

    def __init__(self):
        # priority queue of message type
        self.pq: PriorityQueue[Message] = PriorityQueue(100)

    def put(self, ms: Message):
        """add an operation to teh queue"""
        self.pq.put(ms)

    def get(self):
        """get the first item"""
        payload = self.pq.get()
        return payload

    def peek(self):
        """peek the first item"""
        temp = self.pq.get()
        self.pq.put(temp)
        return temp
