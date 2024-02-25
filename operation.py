"""A class to serialize State Machine instructions"""

import json


class Operation:
    """State Machine Operation"""

    def __init__(self, action, key, value, timestamp):
        self.action = action
        self.value = value
        self.timestamp = timestamp
        self.key = key

    def to_dict(self):
        """Transform the operation to a dict"""
        return {
            "action": self.action,
            "key": self.key,
            "value": self.value,
            "timestamp": self.timestamp,
        }

    def __repr__(self):
        x = self.to_dict()
        return json.dumps(x)

    @classmethod
    def from_string(cls, s):
        """parse a json string to the operation"""
        js = json.loads(s)
        o = Operation(js.action, js.value, js.timestamp, js.key)
        return o

    @classmethod
    def from_dict(cls, d):
        """parse a json string to the operation"""
        o = Operation(d.action, d.value, d.timestamp, d.key)
        return o
