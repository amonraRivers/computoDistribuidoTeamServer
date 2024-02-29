"""RPC Server"""

from threading import Condition, Thread
from uuid import uuid4
from xmlrpc.server import SimpleXMLRPCServer

from message import Message
from message_buffer import MessageBuffer
from operation import Operation
from response_buffer import ResponseBuffer
from utils import Server_Address


class RPCServer:
    """Server"""

    def __init__(self, imq: MessageBuffer, omq: ResponseBuffer, ss, sc):

        host, port = Server_Address.get_server_address(
            "ips.txt"
        )  # Obtiene la dirección IP y el puerto

        self.thread = Thread(target=self._run)
        self.server = SimpleXMLRPCServer(
            (host[0], int(port[0]))
        )  # Usa la IP y el puerto obtenidos
        self.server.register_instance(self)
        self.inbound_message_queue = imq
        self.outbound_message_queue = omq
        self.ss = ss
        self.sc = sc

    # read y update
    def read(self, key):
        """Read"""
        uuid = uuid4()
        m = Message(
            Operation(action="get", key=key, value=None, uuid=uuid, owned=True), 1
        )
        self.inbound_message_queue.put(m)
        threads = self.ss.get_threads()
        for thread in threads:
            thread.get_out_queue().put(m)
        # acto criminal,debe bloquear hasta que haya una respuesta
        response = self.outbound_message_queue.get()
        return response.get_payload()

    def update(self, key, value, operation):
        """Update"""
        valid_operations = ["set", "add", "mult"]
        if operation in valid_operations:
            uuid = uuid4()
            m = Message(
                Operation(
                    action=operation, key=key, value=value, uuid=uuid, owned=True
                ),
                1,
            )

            self.inbound_message_queue.put(m)
            threads = self.ss.get_threads()
            for thread in threads:
                thread.get_out_queue().put(m)
        response = False
        # acto criminal,debe bloquear hasta que haya una respuesta
        response = self.outbound_message_queue.get()
        return response.get_payload()

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
            print("Servidor iniciado")
            self.server.serve_forever()
        except KeyboardInterrupt:
            print("Servidor detenido.")
            self.server.server_close()
