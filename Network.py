from Miner import Miner


class Network:
    def __init__(self):
        self.miners = []
        self.miner_count = 0

    def show_meta(self):
        for miner in self.miners:
            print("MINER: " + str(miner.id), " POWER: " + str(miner.power), " DELAY:" + str(miner.delay))

    def add_miner(self, miner):
        self.miner_count += 1
        self.miners.append(miner)

    def start_mining(self):
        for miner in self.miners:
            miner.start()

    def broadcast(self, b):
        # todo broadcst pow to network
        # todo: -> all other miners
        pass



n = Network()
n.add_miner(Miner(n, 1))
n.add_miner(Miner(n, 0.5))
n.add_miner(Miner(n, 0.5))

n.show_meta()
n.start_mining()