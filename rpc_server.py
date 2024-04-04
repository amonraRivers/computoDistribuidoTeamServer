"""RPC Server"""

from threading import Condition, Thread
from uuid import uuid4
from xmlrpc.server import SimpleXMLRPCServer

from clock import get_clock
from connection_pool import ConnectionPool
from message import Message
from message_buffer import MessageBuffer
from operation import Operation
from response_buffer import ResponseBuffer


class RPCServer:
    """Server"""

    def __init__(
        self, ip, imq: MessageBuffer, omq: ResponseBuffer, thread_pool: ConnectionPool
    ):

        self.thread = Thread(target=self._run)
        self.server = SimpleXMLRPCServer(ip)  # Usa la IP y el puerto obtenidos
        self.server.register_instance(self)
        self.inbound_message_queue = imq
        self.outbound_message_queue = omq
        self.thread_pool = thread_pool

    # read y update
    def print_logs(self, key):
        """Read"""
        uuid = uuid4()
        m = Message(
            Operation(action="print", key=key, value=None, uuid=uuid, owned=True),
            lt=get_clock().stamper(),
        )
        self.inbound_message_queue.put(m)
        threads = self.thread_pool
        threads.send_to_all(m)
        # acto criminal,debe bloquear hasta que haya una respuesta
        response = self.outbound_message_queue.get()
        print("Esperando enviar a hilos", response)
        return response.get_payload()

    def read(self, key):
        """Read"""
        uuid = uuid4()
        m = Message(
            Operation(action="get", key=key, value=None, uuid=uuid, owned=True),
            lt=get_clock().stamper(),
        )
        self.inbound_message_queue.put(m)
        threads = self.thread_pool
        threads.send_to_all(m)
        # acto criminal,debe bloquear hasta que haya una respuesta
        response = self.outbound_message_queue.get()
        print("Esperando enviar a hilos", response)
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
                lt=get_clock().stamper(),
            )

            self.inbound_message_queue.put(m)
            threads = self.thread_pool
            threads.send_to_all(m)
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
