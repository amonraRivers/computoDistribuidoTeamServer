"""La clase para los mensajes del sistema distribuido"""

import json
from uuid import uuid4

from operation import Operation
from utils import get_constants


class Message:
    """Mensaje para el sistmea distribuido"""

    def __init__(self, op: Operation, lt: int):
        self.operation = op
        self.lt = lt
        self.uuid = uuid4()
        self._owned = False

    def to_dict(self):
        """Transform the operation to a dict"""
        cs=get_constants()

        return {
            "operation": self.operation.to_dict(),
            "lt": self.lt,
            "uuid": cs.get_server_id(), 
        }

    def to_owned(self):
        """Mark the message as owned"""
        self._owned = True

    def __repr__(self):
        x = self.to_dict()
        x.pop("lt")
        return json.dumps(x)

    @classmethod
    def from_string(cls, s):
        """parse a json string to the operation"""
        print(s)
        print(len(s))
        js = json.loads(s)
        print(js)
        o = Message(lt=1, op=Operation.from_dict(js.get("operation")))
        return o

    def __lt__(self, other):
        return self.lt < other.lt

    def __eq__(self, other):
        return self.lt == other.lt

    def __gt__(self, other):
        return self.lt > other.lt

    def __le__(self, other):
        return self.lt <= other.lt

    def __ge__(self, other):
        return self.lt >= other.lt

    def __ne__(self, other):
        return self.lt != other.lt
