from Miner import Miner
from Observer import Observer


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
            miner.start(arg=1)

    def mine_next_block(self):
        pass

    def broadcast(self, b):
        # todo broadcst pow to network
        # todo: -> all other miners
        pass



n = Network()
n.add_miner(Miner(n, 10))
n.add_miner(Miner(n, 0.5))
n.add_miner(Miner(n, 0.5))
#o = Observer(n, 3)
#o.start()

#n.show_meta()
n.start_mining()
