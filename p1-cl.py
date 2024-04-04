import xmlrpc.client


##### cliente #####
class RPCClient:
    def __init__(self, url):
        self.client = xmlrpc.client.ServerProxy(url)

    def read(self, key):
        return self.client.read(key)

    def update(self, key, value, operation):
        return self.client.update(key, value, operation)


def get_server_url(filename):
    with open(filename, "r") as file:
        line = file.readline().strip()
        ip, port = line.split()
        url = f"http://{ip}:{port}/"
        return url


if __name__ == "__main__":
    url = get_server_url("ips.txt")
    client = RPCClient(url)
    ####purebas
    a = client.read("a")
    if a == 0:
        print(client.read("a"))
        print(client.update("a", 10, "set"))

    for i in range(10):
        print(client.read("a"))  # 10
        print(client.update("a", 1, "add"))  # True
        print(client.read("a"))  # 15
        print(client.update("a", 3, "add"))  # True
        print(client.read("a"))  # 30
        a = client.read("a")
        if a > 200000000000:
            print(client.update("a", 1, "set"))
    # client.print_log()
