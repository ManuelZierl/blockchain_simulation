from datetime import time


def hash(block):
    # Hashes a Block
    pass

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

    def add_block(self, pow, prev_hash = None):
        self.chain.append({
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'pow': pow,
            'prev_hash': prev_hash or hash(self.chain[-1]),
        })

        self.current_transactions = []

    def add_transaction(self, sender, to, amount ):

        self.current_transactions.append({
            'sender': sender,
            'to': to,
            'amount': amount,
        })




    def get_current_block(self):
        # Returns the last Block in the chain
        pass