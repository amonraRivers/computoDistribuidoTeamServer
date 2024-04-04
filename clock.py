""" Reloj lógico de Lamport"""

class Clock:
    
    def __init__(self):
        self.stamp = 0
        self.comparison = 0
        self.msg = {}
    
    def stamper(self):
        self.stamp = self.stamp + 1
        return (self.stamp)
    
    def sync(self, msg):
        self.msg = msg.lt
        if self.msg > self.stamp:
            self.stamp = self.msg + 1
            print("Syncing... New clock: ", self.stamp)
        else:
            print("Clock is already synced")
    
    ## compare not in use
    def compare(self, msg_a, msg_b):
        self.msg_a = msg_a
        self.msg_b = msg_b
        if self.msg_a.get('stamp') > self.msg_b.get('stamp'):
            self.comparison = 1
            print("A is greater than B")
        else:
            self.comparison = 0
            print("B is greater than A")
    
LAMP_CLOCK = None

def get_clock():
    """Obtiene las constantes del servidor."""
    global LAMP_CLOCK
    if LAMP_CLOCK is None:
        LAMP_CLOCK = Clock()
    return LAMP_CLOCK
