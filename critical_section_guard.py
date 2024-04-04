""" guard for the critical section """

from threading import Lock


class CriticalSectionGuard:
    """guard for the critical section"""

    def __init__(self):
        self.given_to = None
        self.replies = 0
        self._should_release = False
        self.lock = Lock()

    def add_reply(self):
        """Add a reply"""
        with self.lock:
            self.replies += 1

    def request(self):
        """Request the guard"""
        result = False
        with self.lock:
            if self.given_to is None:
                self.given_to = "request"
                result = True
        return result

    def release(self):
        """Release the guard"""
        with self.lock:
            self._reset()

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

    def get_replies(self):
        """Get the number of replies"""
        with self.lock:
            return self.replies

    def set_should_release(self):
        """Should release the guard"""
        with self.lock:
            self._should_release = True

    def should_release(self):
        """Should release the guard"""
        with self.lock:
            return self._should_release

    def __del__(self):
        self.lock.release()


CSG = None


def get_csg():
    """Get the global critical section guard"""
    global CSG
    if CSG is None:
        CSG = CriticalSectionGuard()
    return CSG
