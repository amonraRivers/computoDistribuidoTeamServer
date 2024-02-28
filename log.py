"""module for storing operations"""

from threading import Semaphore

from operation import Operation


class Log:
    """class for storing operations"""

    def __init__(self):
        self._semaphore = Semaphore(1)
        self._queue = []

    def append(self, op: Operation):
        """append operation to queue"""
        with self._semaphore:
            print("Appending operation to log", op.uuid)
            self._queue.append(op)

    def get_index(self, index):
        """get operation from queue"""
        res = None
        with self._semaphore:
            if index >= len(self._queue):
                return None
            res = self._queue[index]

        return res

    def __repr__(self):
        result = ""
        for op in self._queue:
            result += str(op) + "\n"
        return result
