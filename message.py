"""La clase para los mensajes del sistema distribuido"""

import json
from uuid import uuid4

from operation import Operation


class Message:
    """Mensaje para el sistmea distribuido"""

    def __init__(self, payload: Operation, lt: int):
        self.payload = payload
        self.logic_time = lt
        self.uuid = uuid4()
        self._owned = False

    def to_dict(self):
        """Transform the operation to a dict"""
        return {
            "payload": self.payload.to_dict(),
            "logicTime": self.logic_time,
        }

    def to_owned(self):
        """Mark the message as owned"""
        self._owned = True

    def __repr__(self):
        x = self.to_dict()
        return json.dumps(x)

    @classmethod
    def from_string(cls, s):
        """parse a json string to the operation"""
        js = json.loads(s)
        o = Message(js.lt, Operation.from_dict(js.payload))
        return o
