"""La clase para los mensajes del sistema distribuido"""

import json
from uuid import uuid4

from clock import get_clock
from operation import Operation
from utils import get_constants


class Message:
    """Mensaje para el sistmea distribuido"""

    def __init__(self, op: Operation | None, lt: int, t: str = "request", uuid=None):
        self.operation = op
        self.lt = lt
        if uuid:
            self.uuid = str(uuid)
        else:
            self.uuid = str(uuid4())
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
            "uuid": self.uuid,
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

    def get_id(self):
        """Get the id of the message"""
        return self.uuid

    def __repr__(self):
        x = self.to_dict()
        return json.dumps(x)

    @classmethod
    def from_string(cls, s):
        """parse a json string to the operation"""
        # #print(s)
        # #print(len(s))
        js = json.loads(s)
        # #print(js)
        o = Message(
            lt=js.get("lt"),
            op=Operation.from_dict(js.get("operation")),
            t=js.get("type"),
            uuid=js.get("uuid"),
        )
        o.set_node_id(js.get("server_id"))
        return o

    @classmethod
    def create_reply_from_message(cls, msg: "Message"):
        """Create a reply message"""

        return Message(None, get_clock().stamper(), "reply", msg.get_id())

    @classmethod
    def create_release_from_message(cls, msg: "Message"):
        """Create a release message"""
        return Message(None, get_clock().stamper(), "release", msg.get_id())

    def __lt__(self, other):
        print("lower than", self.lt, other.lt)
        print(self.get_node_id(), other.get_node_id())
        if self.lt == other.lt:
            return self.get_node_id() < other.get_node_id()
        return self.lt < other.lt

    def __eq__(self, other):
        return self.uuid == other.uuid

    def __gt__(self, other):
        print("greater than")
        print(self.get_node_id(), other.get_node_id())
        if self.lt == other.lt:
            return self.get_node_id() > other.get_node_id()
        return self.lt > other.lt

    def __le__(self, other):
        # print("le")
        return self.lt <= other.lt

    def __ge__(self, other):
        # print("ge")
        return self.lt >= other.lt

    def __ne__(self, other):
        return self.uuid != other.uuid
