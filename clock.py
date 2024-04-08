""" Reloj lógico de Lamport"""

from utils import get_constants
from threading import Lock

class Clock:
    """Clase que representa un reloj de Lamport."""

    def __init__(self):
        self.stamp = get_constants().get_server_clock()
        #print("Clock initialized with: ", self.stamp)
        self.comparison = 0
        self.msg = {}
        self.lock = Lock()

    def stamper(self):
        """Incrementa el reloj en 1."""
        with self.lock:
            self.stamp += 1
        return self.stamp

    def sync(self, msg):
        """Sincroniza el reloj con el de otro nodo."""
        with self.lock:
            self.msg = msg.lt
            if self.msg > self.stamp:
                self.stamp = self.msg + 1
                #print("Syncing... New clock: ", self.stamp)
            else:
                #print("Clock is already synced")
                pass
    
    ## compare not in use
    def compare(self, msg_a, msg_b):
        """Compara dos mensajes y determina cuál es mayor."""
        self.msg_a = msg_a
        self.msg_b = msg_b
        if self.msg_a.get("stamp") > self.msg_b.get("stamp"):
            self.comparison = 1
            #print("A is greater than B")
        else:
            self.comparison = 0
            #print("B is greater than A")

LAMP_CLOCK = None

def get_clock():
    """Obtiene las constantes del servidor."""
    global LAMP_CLOCK
    if LAMP_CLOCK is None:
        LAMP_CLOCK = Clock()
    return LAMP_CLOCK
