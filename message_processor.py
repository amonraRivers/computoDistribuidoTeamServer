""" Procesadodr de mensajes """

from threading import Condition, Thread

from connection_pool import ConnectionPool
from message_buffer import MessageBuffer
from operation_buffer import OperationBuffer
from utils import get_constants


class MessageProcessor:
    """Procesador de mensajes"""

    def __init__(self, mb: MessageBuffer, ob: MessageBuffer):
        self.mb = mb
        self.ob = ob
        self.thread = Thread(target=self.run)
        self.condition = Condition()
        self.conn_pool = None

    def start(self):
        """Start"""
        self.thread.start()

    def run(self):
        """Run"""
        constants = get_constants("serverips.txt")
        while True:
            message = self.mb.get()
            # if message.get_node_id() == constants.get_server_id():

            self.ob.put(message)
            message = None

    def attach_connection_pool(self, conn_pool: ConnectionPool):
        """Attach connection pool"""
        self.conn_pool = conn_pool

    def join(self):
        """Join"""
        self.thread.join()

    def get_condition(self):
        """Get the condition"""
        return self.condition
