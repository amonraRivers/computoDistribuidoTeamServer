############################################################################################
import threading
import time

class SharedMessageBuffer:
    def __init__(self):
        self.message = None
        self.lock = threading.Lock()
        self.threads_that_read = set()
        self.total_threads = 0

    def add_message(self, message):
        with self.lock:
            self.message = message
            self.threads_that_read.clear()

    def read_message(self, thread_id):
        with self.lock:
            if self.message is not None and thread_id not in self.threads_that_read:
                print(f'Thread {thread_id} lee: {self.message}')
                self.threads_that_read.add(thread_id)
                if len(self.threads_that_read) == self.total_threads:
                    print(f'leído por todos, borrando: {self.message}')
                    self.message = None
                return True
            return False

def worker(thread_id, shared_buffer):
    while True:
        message_read = shared_buffer.read_message(thread_id)
        if not message_read:
            time.sleep(1) 
            
num_threads = 5
shared_buffer = SharedMessageBuffer()
shared_buffer.total_threads = num_threads

# haciendo threads
threads = [threading.Thread(target=worker, args=(i, shared_buffer)) for i in range(num_threads)]
for thread in threads:
    thread.start()

# mensajes
for i in range(3):
    shared_buffer.add_message(f'Message {i}')
    time.sleep(5)  

for thread in threads:
    thread.join()