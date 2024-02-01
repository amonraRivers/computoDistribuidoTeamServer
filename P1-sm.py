# librería 
# https://docs.python.org/3/library/xmlrpc.html

from xmlrpc.server import SimpleXMLRPCServer


###### Máquina de estado ######
class StateMachine:
    def __init__(self):
        self.data = {}
    
    # Métodos
    def get(self, key):
        return self.data.get(key, None)

    def set(self, key, value):
        self.data[key] = value
        return True

    def add(self, key, value):
        if key in self.data:
            self.data[key] += value
            return True
        else:
            return False

    def mult(self, key, value):
        if key in self.data:
            self.data[key] *= value
            return True
        else:
            return False
        
#### Server ####
class RPCServer:
    def __init__(self):
        self.state_machine = StateMachine()
        self.server = SimpleXMLRPCServer(("localhost", 8000))
        self.server.register_instance(self)
    
    # read y update
    def read(self, key):
        return self.state_machine.get(key)

    def update(self, key, value, operation):
        if operation == 'set':
            return self.state_machine.set(key, value)
        elif operation == 'add':
            return self.state_machine.add(key, value)
        elif operation == 'mult':
            return self.state_machine.mult(key, value)
        else:
            return False

    # server on/off
    def run(self):
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


