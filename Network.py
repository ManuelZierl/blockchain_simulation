from Miner import Miner

class Network:
    def __init__(self):
        self.nodes = []
        self.nodes_count = 0
        self.difficulty = 1

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

    def consensus(self):
        for i in range(1, len(self.nodes)):
            if not self.nodes[i - 1].ledger == self.nodes[i].ledger:
                return False

            if not self.nodes[i - 1].chain == self.nodes[i].chain:
                return False
        return True
