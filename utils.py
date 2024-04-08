"""Módulo con funciones útiles para el proyecto."""


class ServerConstants:
    """Clase para leer la dirección IP y el puerto del archivo especificado."""

    def __init__(self, filename):
        self._filename = filename
        self._server = None
        self._server_socket = None
        self._nodes = []
        self._id = None
        self._clock = 0
        with open(filename, "r") as file:
            lines = file.readlines()
            for line in lines:
                line.strip()
                elements = line.split()
                if elements[0] == "server":
                    self._server = (elements[1], int(elements[2]))
                elif elements[0] == "serverSocket":
                    #print("serverSocket")
                    self._server_socket = (elements[1], int(elements[2]))
                elif elements[0] == "node":
                    self._nodes.append((elements[1], int(elements[2])))
                elif elements[0] == "id":
                    self._id = elements[1]
                elif elements[0] == "clock":
                    self._clock = int(elements[1])

    def get_server_clock(self):
        """Lee el reloj del servidor del archivo especificado."""
        return self._clock

    def get_server_address(self):
        """Lee la dirección IP y el puerto del archivo especificado."""
        return self._server

    def get_server_id(self):
        """Lee el id del servidor del archivo especificado."""
        return self._id

    def get_server_socket(self):
        """Lee la dirección IP y el puerto del archivo especificado."""
        return self._server_socket

    def get_nodes(self):
        """Lee la dirección IP y el puerto del archivo especificado."""
        return self._nodes


SERVER_CONSTANTS = None


def get_constants(filename=""):
    """Obtiene las constantes del servidor."""
    global SERVER_CONSTANTS
    if SERVER_CONSTANTS is None:
        SERVER_CONSTANTS = ServerConstants(filename)
    return SERVER_CONSTANTS
