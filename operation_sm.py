# operation_sm

from queue import Queue
from threading import Condition, Thread

from clock import get_clock
from log import Log
from operation import Operation
from response_buffer import Response, ResponseBuffer
from state_machine import StateMachine


class OperationStateMachine:

    def __init__(self, rb: ResponseBuffer):
        self.thread = Thread(target=self.run)
        self.state_machine = StateMachine()
        self.log: Log | None = None
        self.additem_condition: Condition | None = None
        self.index = 0
        self.rb = rb

    def do_operation(self, op: Operation):
        """Do operation"""
        if op:
            # print("Ejecutando operacion", op.uuid)
            payload = None
            if op.action == "get":
                payload = self.state_machine.get(op.key)
            elif op.action == "set":
                payload = self.state_machine.set(op.key, op.value)
            elif op.action == "add":
                payload = self.state_machine.add(op.key, op.value)
            elif op.action == "mult":
                payload = self.state_machine.mult(op.key, op.value)
            elif op.action == "print":
                print("[LOG]", self.log)
                payload = str(self.log)
            if op.owned:
                res = Response(payload, op.uuid)
                self.rb.put(res)
            get_clock().stamper()

    def set_additem_condition(self, condition: Condition):
        """Set the add item condition"""
        self.additem_condition = condition

    def set_log(self, log: Log):
        self.log = log

    def start(self):
        self.thread.start()

    def join(self):
        self.thread.join()

    def run(self):
        while True:

            with self.additem_condition:
                if self.index >= self.log.get_size():
                    self.additem_condition.wait()
                if self.index < self.log.get_size():
                    op = self.log.get_index(self.index)
                    self.do_operation(op)
                    self.index += 1
