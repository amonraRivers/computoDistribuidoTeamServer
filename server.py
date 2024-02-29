"""StateMachine""" #not in use anymore 

# librería
# https://docs.python.org/3/library/xmlrpc.html

from xmlrpc.server import SimpleXMLRPCServer


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


class RPCServer:
    """Server"""

    def __init__(self):
        self.state_machine = StateMachine()
        self.server = SimpleXMLRPCServer(("0.0.0.0", 8000))
        self.server.register_instance(self)

    # read y update
    def read(self, key):
        """Read"""
        return self.state_machine.get(key)

    def update(self, key, value, operation):
        """Update"""
        if operation == "set":
            return self.state_machine.set(key, value)
        if operation == "add":
            return self.state_machine.add(key, value)
        if operation == "mult":
            return self.state_machine.mult(key, value)
        return False

    # server on/off
    def run(self):
        """Run"""
        try:
            print("Servidor iniciado.")
            self.server.serve_forever()
        except KeyboardInterrupt:
            print("Servidor detenido.")
            self.server.server_close()


### main ###
if __name__ == "__main__":
    server = RPCServer()
    server.run()
