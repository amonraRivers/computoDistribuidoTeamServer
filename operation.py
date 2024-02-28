"""A class to serialize State Machine instructions"""

import json
from uuid import uuid4


class Operation:
    """State Machine Operation"""

    def __init__(self, action, key, value, uuid=None):
        """Constructor"""
        if uuid:
            self.uuid = uuid
        else:
            self.uuid = uuid4()
        self.action = action
        self.value = value
        self.key = key

    def to_dict(self):
        """Transform the operation to a dict"""
        return {
            "action": self.action,
            "key": self.key,
            "value": self.value,
        }

    def __repr__(self):
        x = self.to_dict()
        return json.dumps(x)

    @classmethod
    def from_string(cls, s):
        """parse a json string to the operation"""
        js = json.loads(s)
        o = Operation(js.action, js.value, js.key)
        return o

    @classmethod
    def from_dict(cls, d):
        """parse a json string to the operation"""
        o = Operation(d.action, d.value, d.key)
        return o
