""" Procesadodr de mensajes """

from threading import Thread

from buffer import Buffer
from log import Log


class MessageProcessor:
    def __init__(self,buffer,log):
        self.buffer=buffer
        self.log=log

    def start(self):
        self.thread=Thread(target=self.run)
        self.thread.start()

    def run(self):
        while True:
            message=self.buffer.get()
            self.log.append(message)
            print("Message processed",message)
            message=None

    def join(self):
        self.thread.join()
