"""RPC Server"""

from threading import Condition, Thread
from uuid import uuid4
from xmlrpc.server import SimpleXMLRPCServer

from buffer import Buffer
from log import Log
from message import Message
from operation import Operation
from response_queue import ResponseQueue


class RPCServer:
    """Server"""

    def __init__(self, imq: Log, omq: ResponseQueue, co: Condition):
        self.thread = Thread(target=self._run)
        self.server = SimpleXMLRPCServer(("0.0.0.0", 8000))
        self.server.register_instance(self)
        self.inbound_message_queue = imq
        self.outbound_message_queue = omq
        self.condition = co

    # read y update
    def read(self, key):
        """Read"""
        uuid = uuid4()
        self.inbound_message_queue.append(
            Operation(action="get", key=key, value=None, uuid=uuid),
        )
        print("Esperando respuesta")
        # acto criminal,debe bloquear hasta que haya una respuesta
        response = False
        with self.condition:
            self.condition.wait()
            print("Respuesta recibida")
            response = self.outbound_message_queue.get(uuid)
        return response

    def update(self, key, value, operation):
        """Update"""
        valid_operations = ["set", "add", "mult"]
        if operation in valid_operations:
            uuid = uuid4()
            self.inbound_message_queue.append(
                Operation(action=operation, key=key, value=value, uuid=uuid),
            )
            response_ready = False
            response = None
            print("Esperando respuesta")
            # acto criminal, bloquear hasta que haya una respuesta
        response = False
        with self.condition:
            self.condition.wait()
            print("Respuesta recibida")
            response = self.outbound_message_queue.get(uuid)
        return response

    def start(self):
        """Inicia el Hilo"""
        self.thread.start()

    def join(self):
        """Espera a que termine el hilo"""
        self.thread.join()

    # server on/off
    def _run(self):
        """Run"""
        try:
            print("Servidor iniciado.")
            self.server.serve_forever()
        except KeyboardInterrupt:
            print("Servidor detenido.")
            self.server.server_close()
