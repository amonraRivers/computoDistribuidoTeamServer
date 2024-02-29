""" Procesadodr de mensajes """

from threading import Thread

from message_buffer import MessageBuffer
from operation_buffer import OperationBuffer


class MessageProcessor:
    """Procesador de mensajes"""

    def __init__(self, mb: MessageBuffer, ob: OperationBuffer):
        self.mb = mb
        self.ob = ob
        self.thread = Thread(target=self.run)

    def start(self):
        """Start"""
        self.thread.start()

    def run(self):
        """Run"""
        while True:
            message = self.mb.get()
            self.ob.put(message.operation)
            message = None

    def join(self):
        """Join"""
        self.thread.join()
