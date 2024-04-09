"""Operation executor"""

from threading import Condition, Thread

from clock import get_clock
from connection_pool import ConnectionPool
from critical_section_guard import get_csg
from log import Log
from message import Message
from message_buffer import MessageBuffer
from operation import Operation
from state_machine import StateMachine
from utils import get_constants

class OperationExecutor:
    """Operation executor"""

    def __init__(self, ob: MessageBuffer):
        """Constructor"""
        self.ob = ob
        self.thread = Thread(target=self.run)
        self.state_machine = StateMachine()
        self.log = Log()
        self.conn_pool: ConnectionPool | None = None
        self.enter_condition: Condition | None = None

    def start(self):
        """Start"""
        self.thread.start()

    def should_enter_cs(self, msg: Message):
        """Should enter critical section"""
        csg = get_csg()
        replies = csg.get_replies(msg)
        constants = get_constants()
        # print("Replies", replies)
        return replies >= len(constants.get_nodes())

    def run(self):
        """Run"""
        while True:
            # #print(self.state_machine.get_operations_count())
            # bloquear hasta que haya una nueva operacion

            csg = get_csg()

            constants = get_constants()
            msg = self.ob.peek()
            enter = False
            while not enter:
                msg = self.ob.peek()
                print("[OperationExecutor] msg ", msg)
                op = msg.operation
                # print("Checking if should enter CS")

                if msg.get_node_id() != constants.get_server_id():
                    print("Sending reply")
                    self.conn_pool.send_to(
                        Message.create_reply_from_message(msg), msg.get_node_id()
                    )
                    with self.enter_condition:
                        if not (csg.should_release(msg) and msg == self.ob.peek()):
                            print("Waiting for release")
                            self.enter_condition.wait(1)

                        if csg.should_release(msg) and msg == self.ob.peek():
                            msg = self.ob.get()
                            csg.reset_release(msg)
                            enter = True

                else:
                    # print("Esperando entrar a la seccion critica")
                    with self.enter_condition:
                        if not (self.should_enter_cs(msg) and msg == self.ob.peek()):
                            print("Waiting for replies")
                            self.enter_condition.wait(1)
                        if self.should_enter_cs(msg) and msg == self.ob.peek():
                            msg = self.ob.get()
                            csg.remove_replies(msg)
                            self.conn_pool.send_to_all(
                                Message.create_release_from_message(msg)
                            )
                            enter = True
                            with self.additem_condition:
                                self.additem_condition.notify() 

            # print("[OperationExecutor] msg timestamp", msg.lt)
            self.log.append(op)

    def join(self):
        """Join"""
        self.thread.join()

    def attach_connection_pool(self, conn_pool: ConnectionPool):
        """Attach connection pool"""
        self.conn_pool = conn_pool

    def set_cs_condition(self, condition: Condition):
        """Set the condition"""
        self.enter_condition = condition
    
    def set_additem_condition(self, condition: Condition):
        """Set the add item condition"""
        self.additem_condition = condition

    def set_log(self, log: Log):
        shared_log = self.log
