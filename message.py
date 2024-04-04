"""La clase para los mensajes del sistema distribuido"""

import json
from uuid import uuid4

from operation import Operation
from utils import get_constants


class Message:
    """Mensaje para el sistmea distribuido"""

    def __init__(self, op: Operation | None, lt: int, t: str = "request"):
        self.operation = op
        self.lt = lt
        self.uuid = uuid4()
        self.server_id = get_constants().get_server_id()
        self.typ = t

    def to_dict(self):
        """Transform the operation to a dict"""
        op_dict = None
        if self.operation is not None:
            op_dict = self.operation.to_dict()

        return {
            "operation": op_dict,
            "lt": self.lt,
            "server_id": self.server_id,
            "type": self.typ,
        }

    def get_type(self):
        """Get the type of the message"""
        return self.typ

    def get_node_id(self):
        """Get the node id"""
        return self.server_id

    def set_node_id(self, server_id):
        """Set the node id"""
        self.server_id = server_id

    def set_type(self, t):
        """Set the type of the message"""
        self.typ = t

    def __repr__(self):
        x = self.to_dict()
        x.pop("lt")
        return json.dumps(x)

    @classmethod
    def from_string(cls, s):
        """parse a json string to the operation"""
        # print(s)
        # print(len(s))
        js = json.loads(s)
        # print(js)
        o = Message(lt=1, op=Operation.from_dict(js.get("operation")))
        o.set_node_id(js.get("server_id"))
        o.set_type(js.get("type"))
        return o

    @classmethod
    def create_reply(cls, lt: int):
        """Create a reply message"""
        return Message(None, lt, "reply")

    def __lt__(self, other):
        if self.lt == other.lt:
            return self.get_node_id() < other.get_node_id()
        return self.lt < other.lt

    def __eq__(self, other):
        return self.uuid == other.uuid

    def __gt__(self, other):
        if self.lt == other.lt:
            return self.get_node_id() > other.get_node_id()
        return self.lt > other.lt

    def __le__(self, other):
        print("le")
        return self.lt <= other.lt

    def __ge__(self, other):
        print("ge")
        return self.lt >= other.lt

    def __ne__(self, other):
        return self.uuid != other.uuid
