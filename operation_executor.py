"""Operation executor"""

from threading import Condition, Thread

from log import Log
from response_queue import Response, ResponseQueue
from state_machine import StateMachine


class OperationExecutor:
    """Operation executor"""

    def __init__(self, log: Log, response_queue: ResponseQueue, codition: Condition):
        """Constructor"""
        self.log = log
        self.thread = Thread(target=self.run)
        self.state_machine = StateMachine()
        self.response_queue = response_queue
        self.condition = codition

    def start(self):
        """Start"""
        self.thread.start()

    def run(self):
        """Run"""
        while True:
            # print(self.state_machine.get_operations_count())
            # bloquear hasta que haya una nueva operacion
            op = self.log.get_index(self.state_machine.get_operations_count())
            print("Esperando operacion")
            if op:
                print("Executing operation", op.uuid)
                payload = None
                if op.action == "get":
                    payload = self.state_machine.get(op.key)
                elif op.action == "set":
                    payload = self.state_machine.set(op.key, op.value)
                elif op.action == "add":
                    payload = self.state_machine.add(op.key, op.value)
                elif op.action == "mult":
                    payload = self.state_machine.mult(op.key, op.value)
                with self.condition:
                    res = Response(payload, op.uuid)
                    print("Appending response to queue", payload, op.uuid)
                    self.response_queue.append(res)
                    self.condition.notify()
            op = None

    def join(self):
        """Join"""
        self.thread.join()
