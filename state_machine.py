"""Módulo que contiene la clase StateMachine"""


class StateMachine:
    """Máquina de estado"""

    def __init__(self):
        self.data = {}

    # Métodos
    def get(self, key):
        """Get"""
        return self.data.get(key, None)

    def set(self, key, value):
        """Set"""
        self.data[key] = value
        return True

    def add(self, key, value):
        """Add"""
        if key in self.data:
            self.data[key] += value
            return True
        return False

    def mult(self, key, value):
        """Mult"""
        if key in self.data:
            self.data[key] *= value
            return True
        return False
