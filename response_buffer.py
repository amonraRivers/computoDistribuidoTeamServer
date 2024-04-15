"""The message queue client"""

from queue import Queue


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


class ResponseBuffer:
    """A class for sending a response to the rpc server"""

    def __init__(
        self,
    ):
        self._queue = Queue()

    def put(self, r: Response):
        """send a message to the buffer"""
        self._queue.put(r)
        #print("Agregando respuesta a buffer de respuestas")

    def get(self) -> Response:
        """get a message by id"""
        res = None
        res = self._queue.get()
        #print("Quitando respuesta a buffer de respuestas")

        return res
