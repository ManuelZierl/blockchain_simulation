import hashlib
import random
import string
import threading
import time
import binascii

import codecs
from ecdsa import SigningKey
from ecdsa import VerifyingKey
import ecdsa
import json


def hash_block(block):
    block_string = str(block)
    return binascii.hexlify(hashlib.pbkdf2_hmac('sha1', str.encode(block_string), b'valarmorghulis', 100))


class Miner(threading.Thread):
    def __init__(self, network, power=1, chain=None):
        threading.Thread.__init__(self)
        self.network = network
        self.id = network.miner_count
        self.power = power
        self.delay = 1 / power
        self.calls = 0


        self.transactions = []
        self.chain = []
        if chain is None:
            with open('genesis_block.json') as data_file:
                self.chain = json.load(data_file)
        else:
            # todo: this miner joined later in the game
            # todo: before he starst mining he has to check
            # todo: the entire chain of validity
            pass

        # generate keys
        private_key = SigningKey.generate(curve=ecdsa.SECP256k1)
        public_key = private_key.get_verifying_key()

        """
        we assume you can't access the private key.
        Which of course would be possible in principle
        but this is just a simulation
        """
        self.__private_key = codecs.encode(private_key.to_string(), 'hex').decode("utf-8")
        self.public_key = codecs.encode(public_key.to_string(), 'hex').decode("utf-8")

    # VERIFICATION
    def verify_block(self, block):
        # todo: verfiy a new block
        # todo: check proof
        # todo: check for invalid transactions
        # todo: check if reward has correct amount and coorect adress
        # todo: ...
        # todo: check id
        pass

    def verify_transaction(self, transaction):
        transaction_copy = dict(transaction)
        signatur = transaction_copy["signature"]
        transaction_copy.pop('signature', None)
        transaction_string = str(transaction_copy)

        public_key = transaction_copy["sender"]

        vk = VerifyingKey.from_string(bytes.fromhex(public_key), curve=ecdsa.SECP256k1)
        try:
            if vk.verify(bytes.fromhex(signatur), transaction_string.encode()) is True:
                return True
            else:
                return False
        except:
            return False

    def transaction(self, to, amount):
        transaction = {
            'sender': self.public_key,
            'to': to,
            'amount': amount,
        }

        transaction_string = str(transaction)
        p_key = SigningKey.from_string(bytes.fromhex(self.__private_key), curve=ecdsa.SECP256k1)
        signature = p_key.sign(transaction_string.encode())
        transaction["signature"] = codecs.encode(signature, 'hex').decode("utf-8")
        return transaction

    def run(self, blocks = 0):
        # 0  -> no limit
        # 1: -> mine until this amout of block are mined
        while True: # todo: blocks

            block_hash = hash_block(self.chain[-1])
            random_str = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
            dk = hashlib.pbkdf2_hmac('sha1', block_hash, str.encode(random_str), 100)
            if binascii.hexlify(dk)[-1:] == b'f': #todo: <-- vllt anpassen?
                print(self.id, "--->", random_str)
                # creater new block
                block = {
                    "id": self.chain[-1]["id"] + 1,
                    "proof": random_str,
                    "transactions": self.transactions,
                    "previous_hash": block_hash
                  }

                #reset transcations
                self.transactions = []
                self.broadcast(block, "pow")
                self.chain.append(block)

            self.calls += 1
            time.sleep(self.delay)




    def verify(self, chain):
        # todo
        # todo: verfiy the validity of a chain
        # todo: has to verify all blocks/transactions
        pass


    # COMMUNICATION
    def broadcast(self, data, type=None):
        if type == "pow":
            for miner in self.network.miners:
                if miner != self:
                    miner.broadcast_proof_of_work(data)

        if type == "tra":
            for miner in self.network.miners:
                if miner != self:
                    miner.broadcast_transaction(data)


    def broadcast_proof_of_work(self, block):
        # todo: this function is called by other Miners when they try to broadcast a new block
        pass

    def broadcast_transaction(self, transaction):
        if self.verify_transaction(transaction) is True:
            self.transactions.append(transaction)
        # todo: this function is called by other Miners when they try to broadcast a new transaction
        pass
