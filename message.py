"""La clase para los mensajes del sistema distribuido"""

import json
from uuid import uuid4

from operation import Operation
from utils import get_constants


class Message:
    """Mensaje para el sistmea distribuido"""

    def __init__(self, op: Operation, lt: int, t: str = "request"):
        self.operation = op
        self.lt = lt
        self.uuid = uuid4()
        self.server_id = get_constants().get_server_id()
        self._type = t
        self.node_id = -1

    def to_dict(self):
        """Transform the operation to a dict"""

        return {
            "operation": self.operation.to_dict(),
            "lt": self.lt,
            "server_id": self.server_id,
            "type": self._type,
        }

    def get_type(self):
        """Get the type of the message"""
        return self._type

    def get_node_id(self):
        """Get the node id"""
        return self.node_id

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
        if self.lt == other.lt:
            return self.node_id < other.node_id
        return self.lt < other.lt

    def __eq__(self, other):
        return self.uuid == other.uuid

    def __gt__(self, other):
        if self.lt == other.lt:
            return self.node_id > other.node_id
        return self.lt > other.lt

    def __le__(self, other):
        print("le")
        return self.lt <= other.lt

    def __ge__(self, other):
        print("ge")
        return self.lt >= other.lt

    def __ne__(self, other):
        return self.uuid != other.uuid
