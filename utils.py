class ServerAddress:
    @staticmethod
    def get_server_address(filename):
        """Lee la dirección IP y el puerto del archivo especificado."""
        SERVER = []
        PORT = []
        with open(filename, "r") as file:
            lines = file.readlines()
            for line in lines:
                line.strip()
                host, port = line.split()
                SERVER.append(host)
                PORT.append(port)
        return (SERVER, PORT)
