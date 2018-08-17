
import threading

import time


class Observer(threading.Thread):
    def __init__(self,network, delay=1):
        threading.Thread.__init__(self)
        self.delay = delay
        self.network = network

    def run(self):
        while True:
            print(self.network.miners[0].ledger)
            print( len(threading.enumerate()))
            print()
            time.sleep(self.delay)
        pass

