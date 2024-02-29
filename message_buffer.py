"""A class for communicating between the rpc , the nodes and the state machine."""

from queue import PriorityQueue

from message import Message


class MessageBuffer:
    """El Buffer de comunicacion"""

    def __init__(self):
        self.pq = PriorityQueue(100)

    def put(self, ms: Message):
        """add an operation to teh queue"""
        self.pq.put(ms)
        print("Agregando mensaje a buffer de mensajes")

    def get(self):
        """get the first item"""
        payload = self.pq.get()
        print("Quitando mensaje a buffer de mensajes")
        return payload
