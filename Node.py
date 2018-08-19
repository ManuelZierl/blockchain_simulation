import threading

import _thread
import time

import math


class Node:
    def __init__(self, network, power=1):
        self.network = network
        self.id = network.nodes_count
        self.network.nodes_count += 1
        self.power = power
        self.delay = 1 / power
        self.calls = 0
        self.blocks_to_go = 0

    def run(self, blocks, time):
        self.blocks_to_go = blocks
        thread = threading.Thread(target=self.work, args=[time])
        thread.start()

    def send_broadcast(self, data):
        for node in self.network.nodes:
            node.receive_broadcast(data)

    def receive_broadcast(self, data):
        raise Exception("Node is a abstract class. receive_broadcast() must be overwritten in subclasses")

    def work(self):
        raise Exception("Node is a abstract class. work() must be overwritten in subclasses")



