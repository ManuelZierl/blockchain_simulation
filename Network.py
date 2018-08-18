from Miner import Miner
from Observer import Observer
import atexit

class Network:
    def __init__(self):
        self.nodes = []
        self.nodes_count = 0

    def show_meta(self):
        for miner in self.nodes:
            print("MINER: " + str(miner.id), " POWER: " + str(miner.power), " DELAY:" + str(miner.delay))

    def add_node(self, node):
        self.nodes_count += 1
        self.nodes.append(node)

    def start_working(self, blocks=1):
        for node in self.nodes:
            node.run(blocks)

    def new_miners(self, amount, power):
        for i in range(amount):
            self.add_node(Miner(self, power))



n = Network()
n.add_node(Miner(n, 0.5))
n.add_node(Miner(n, 0.5))
n.add_node(Miner(n, 0.5))
n.add_node(Miner(n, 0.5))

n.start_working(blocks=5)

def atexit_x():
    for node in n.nodes:
        node.show_ledger()

atexit.register(atexit_x)
#
# n.start_working(blocks=5)
#

#o = Observer(n, 3)
#o.start()

#n.show_meta()

