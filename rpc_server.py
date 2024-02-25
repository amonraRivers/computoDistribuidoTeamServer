"""RPC Server"""

from xmlrpc.server import SimpleXMLRPCServer

from state_machine import StateMachine


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
