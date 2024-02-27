"""The message queue client"""

from threading import Semaphore


class Response:
    """A class for the response"""

    def __init__(self, payload, _id: int):
        self.payload = payload
        self._id = _id

    def get_id(self):
        """get the id"""
        return self._id

    def get_payload(self):
        """get the payload"""
        return self.payload

    def set_payload(self, payload):
        """set the payload"""
        self.payload = payload


class ResponseQueue:
    """A class for sending messages to the buffer"""

    def __init__(
        self,
    ):
        self._semaphore = Semaphore(1)
        self._queue = {}

    def append(self, r: Response):
        """send a message to the buffer"""
        with self._semaphore:
            print("Appending response to queue", r.payload, r.get_id())
            self._queue[r.get_id()] = r.get_payload()

    def get(self, _id: int):
        """get a message by id"""
        res = None
        with self._semaphore:
            if _id in self._queue:
                res = self._queue[_id]
                del self._queue[_id]

        return res
