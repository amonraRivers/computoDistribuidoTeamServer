""" guard for the critical section """

from threading import Lock

from message import Message
from utils import get_constants


class CriticalSectionGuard:
    """guard for the critical section"""

    def __init__(self):
        self.given_to = None
        self.replies = {}
        self._should_release = {}
        self.lock = Lock()

    def add_reply(self, msg: Message):
        """Add a reply"""
        with self.lock:
            if msg.get_node_id() not in self.replies:
                self.replies[msg.get_node_id()] = {}
            self.replies[msg.get_node_id()][msg.get_id()] = True

    def remove_replies(self, msg: Message):
        """Remove the replies"""
        with self.lock:
            if msg.get_node_id() in self.replies:
                del self.replies[msg.get_node_id()][msg.get_id()]

    def get_replies(self, msg: Message):
        """Get the replies"""
        res = 0
        with self.lock:
            for i in self.replies:
                if msg.get_id() in self.replies[i]:
                    res += 1
        return res

    def request(self):
        """Request the guard"""
        result = False
        with self.lock:
            if self.given_to is None:
                self.given_to = "request"
                result = True
        return result

    def reset_release(self, msg: Message):
        """Release the guard"""
        with self.lock:
            if msg.get_id() in self._should_release:
                del self._should_release[msg.get_id()]

    def _reset(self):
        """Reset the guard"""
        self.given_to = None
        self.replies = 0
        self._should_release = False

    def is_given_to(self):
        """Is given to"""
        with self.lock:
            return self.given_to is not None

    def set_given_to(self, who):
        """Set who is given to"""
        with self.lock:
            self.given_to = who

    def reset(self):
        """Reset the guard"""
        with self.lock:
            self._reset()

    def reset_replies(self):
        """Reset the replies"""
        with self.lock:
            self.replies = 0

    def set_should_release(self, msg: Message):
        """Should release the guard"""
        with self.lock:
            self._should_release[msg.get_id()] = True

    def remove_should_release(self, msg: Message):
        """Should release the guard"""
        with self.lock:
            if msg.get_id() in self._should_release:
                del self._should_release[msg.get_id()]

    def should_release(self, msg: Message):
        """Should release the guard"""
        with self.lock:
            return self._should_release.get(msg.get_id(), False)

    def __del__(self):
        self.lock.release()


CSG = None


def get_csg():
    """Get the global critical section guard"""
    global CSG
    if CSG is None:
        CSG = CriticalSectionGuard()
    return CSG
