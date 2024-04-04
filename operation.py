"""A class to serialize State Machine instructions"""

import json
from uuid import uuid4


class Operation:
    """State Machine Operation"""

    def __init__(self, action, key, value, uuid=None, owned=False):
        """Constructor"""
        if uuid:
            self.uuid = str(uuid)
        else:
            self.uuid = str(uuid4())
        self.action = action
        self.value = value
        self.key = key
        self.owned = owned

    def to_dict(self):
        """Transform the operation to a dict"""
        return {
            "action": self.action,
            "key": self.key,
            "value": self.value,
            "uuid": self.uuid,
        }

    def __repr__(self):
        x = self.to_dict()
        return json.dumps(x)

    @classmethod
    def from_string(cls, s):
        """parse a json string to the operation"""
        js = json.loads(s)
        if not js:
            return None
        o = Operation(js.action, js.value, js.key, js.uuid)
        return o

    @classmethod
    def from_dict(cls, d):
        """parse a json string to the operation"""
        if not d:
            return None
        o = Operation(d.get("action"), d.get("value"), d.get("key"), d.get("uuid"))
        return o
