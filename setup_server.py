"""Setup for the package."""

from rpc_server import RPCServer

if __name__ == "__main__":
    print("This is the setup_server.py file")
    server = RPCServer()
    server.run()
