class Server_Address:
    def get_server_address(filename):
        """Lee la dirección IP y el puerto del archivo especificado."""
        SERVER = []
        PORT = []
        with open(filename, 'r') as file:
            for line in file:
                line = file.readline().strip()
                host, port = line.split()
                print(host, port)
                SERVER.append(host)
                PORT.append(port)
                print(SERVER, PORT)
        return SERVER, PORT