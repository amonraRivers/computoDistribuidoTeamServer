"""Operation executor"""

from threading import Condition, Thread

from log import Log
from operation_buffer import OperationBuffer
from response_buffer import Response, ResponseBuffer
from state_machine import StateMachine


class OperationExecutor:
    """Operation executor"""

    def __init__(self, ob: OperationBuffer, rb: ResponseBuffer):
        """Constructor"""
        self.ob = ob
        self.thread = Thread(target=self.run)
        self.state_machine = StateMachine()
        self.rb = rb
        self.log = Log()

    def start(self):
        """Start"""
        self.thread.start()

    def run(self):
        """Run"""
        while True:
            # print(self.state_machine.get_operations_count())
            # bloquear hasta que haya una nueva operacion

            op = self.ob.get()
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
            op = None

    def join(self):
        """Join"""
        self.thread.join()
