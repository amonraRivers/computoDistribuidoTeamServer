""" Module for the RequestQueue class. """

from queue import PriorityQueue

from message import Message


class RequestQueue:
    """A class to represent a queue of requests."""

    def __init__(self):
        self.queue = PriorityQueue()

    def add_request(self, request: Message):
        """Add a request to the queue."""
        self.queue.put(request)

    def get_request(self):
        """Get the next request"""
        return self.queue.get()
