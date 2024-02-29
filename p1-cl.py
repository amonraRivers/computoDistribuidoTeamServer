import xmlrpc.client
##### cliente #####
class RPCClient:
    def __init__(self, url):
        self.client = xmlrpc.client.ServerProxy(url)

    def read(self, key):
        return self.client.read(key)

    def update(self, key, value, operation):
        return self.client.update(key, value, operation)

if __name__ == "__main__":
    client = RPCClient("http://localhost:8000/")
    ####purebas
    print(client.update("a", 10, "set"))  # True
    print(client.read("a"))  # 10
    print(client.update("a", 5, "add"))  # True
    print(client.read("a"))  # 15
    print(client.update("a", 2, "mult"))  # True
    print(client.read("a"))  # 30