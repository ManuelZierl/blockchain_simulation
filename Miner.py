import threading
import time

class Miner(threading.Thread):
    def __init__(self, network, power = 1):
        threading.Thread.__init__(self)
        self.id = network.miner_count
        self.power = power
        self.delay = 1/power
        self.calls = 0
        pass

    def run(self):
        while True:
            self.calls += 1
            print(self.id, self.calls)
            time.sleep(self.delay)

