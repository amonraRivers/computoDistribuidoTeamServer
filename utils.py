def get_server_address(filename):
    """Lee la dirección IP y el puerto del archivo especificado."""
    with open(filename, 'r') as file:
        line = file.readline().strip()
        host, port = line.split()
        return host, port