"""Operation executor"""

from threading import Condition, Thread

from connection_pool import ConnectionPool
from critical_section_guard import get_csg
from log import Log
from message import Message
from message_buffer import MessageBuffer
from response_buffer import Response, ResponseBuffer
from state_machine import StateMachine
from utils import get_constants
from clock import get_clock

class OperationExecutor:
    """Operation executor"""

    def __init__(self, ob: MessageBuffer, rb: ResponseBuffer):
        """Constructor"""
        self.ob = ob
        self.thread = Thread(target=self.run)
        self.state_machine = StateMachine()
        self.rb = rb
        self.log = Log()
        self.conn_pool: ConnectionPool | None = None
        self.enter_condition: Condition | None = None
        self.release_condition: Condition | None = None

    def start(self):
        """Start"""
        self.thread.start()

    def run(self):
        """Run"""
        while True:
            # print(self.state_machine.get_operations_count())
            # bloquear hasta que haya una nueva operacion

            csg = get_csg()
            constants = get_constants()
            msg = self.ob.get()
            op = msg.operation
            print(msg.get_node_id(), constants.get_server_id())
            if msg.get_node_id() != constants.get_server_id():
                print("sending to", msg.get_node_id())
                self.conn_pool.send_to(Message.create_reply(0), msg.get_node_id())
            else:
                print("sending to myself")

            if op:
                self.log.append(op)
                print("Ejecutando operacion", op.uuid)
                payload = None
                if op.action == "get":
                    payload = self.state_machine.get(op.key)
                elif op.action == "set":
                    payload = self.state_machine.set(op.key, op.value)
                elif op.action == "add":
                    payload = self.state_machine.add(op.key, op.value)
                elif op.action == "mult":
                    payload = self.state_machine.mult(op.key, op.value)
                if op.owned:
                    res = Response(payload, op.uuid)
                    self.rb.put(res)
                get_clock().stamper()
            op = None

    def join(self):
        """Join"""
        self.thread.join()

    def attach_connection_pool(self, conn_pool: ConnectionPool):
        """Attach connection pool"""
        self.conn_pool = conn_pool

    def set_cs_condition(self, condition: Condition):
        """Set the condition"""
        self.enter_condition = condition

    def set_release_condition(self, condition: Condition):
        """Set the condition"""
        self.release_condition = condition
