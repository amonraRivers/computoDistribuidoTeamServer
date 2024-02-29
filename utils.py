class Server_Address:
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
                print(host, port)
                SERVER.append(host)
                PORT.append(port)
                print(SERVER, PORT)
        return (SERVER, PORT)
