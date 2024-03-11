"""Módulo que contiene la clase StateMachine"""


class StateMachine:
    """Máquina de estado"""

    def __init__(self):
        self._data = {}
        self._operations_count = 0

    def _add_operation_count(self):
        self._operations_count += 1

    # Métodos
    def get(self, key):
        """Get"""
        self._add_operation_count()
        return self._data.get(key, 0)

    def set(self, key, value):
        """Set"""
        self._add_operation_count()
        self._data[key] = value
        return True

    def add(self, key, value):
        """Add"""
        self._add_operation_count()
        if key in self._data:
            self._data[key] += value
            return True
        return False

    def mult(self, key, value):
        """Mult"""
        self._add_operation_count()
        if key in self._data:
            self._data[key] *= value
            return True
        return False

    def get_operations_count(self):
        """Get operations count"""
        return self._operations_count
