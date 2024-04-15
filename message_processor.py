""" Procesadodr de mensajes """

from threading import Condition, Thread

from clock import get_clock
from connection_pool import ConnectionPool
from critical_section_guard import get_csg
from message_buffer import MessageBuffer
from operation_buffer import OperationBuffer
from utils import get_constants


class MessageProcessor:
    """Procesador de mensajes"""

    def __init__(self, mb: MessageBuffer, ob: MessageBuffer):
        self.mb = mb
        self.ob = ob
        self.thread = Thread(target=self.run)
        self.enter_condition: Condition | None = None
        self.release_condition: Condition | None = None
        self.conn_pool: ConnectionPool | None = None

    def start(self):
        """Start"""
        self.thread.start()

    def run(self):
        """Run"""
        constants = get_constants()
        server_id = constants.get_server_id()
        csg = get_csg()
        while True:
            message = self.mb.get()

            get_clock().sync(message)

            # print("Message received")
            # print(message.get_type(), "request")
            if message.get_type() == "request":
                # print("Request received")
                print("[INFO] [REQUEST]", message)
                self.ob.put(message)
            elif message.get_type() == "reply":
                # print("Reply received")
                csg.add_reply(message)
                print("[INFO] [REPLY]", message, "replies")
                print("[INFO]", csg.get_replies(message))

            elif message.get_type() == "release":
                # print("Release received")
                print("[INFO] [RELEASE]", message)
                csg.set_should_release(message)

            with self.enter_condition:
                self.enter_condition.notify()
            message = None

    def attach_connection_pool(self, conn_pool: ConnectionPool):
        """Attach connection pool"""
        self.conn_pool = conn_pool

    def join(self):
        """Join"""
        self.thread.join()

    def set_cs_condition(self, condition: Condition):
        """Set the condition"""
        self.enter_condition = condition

    def set_release_condition(self, condition: Condition):
        """Set the condition"""
        self.release_condition = condition
