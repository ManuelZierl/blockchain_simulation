import hashlib
import random
import string
import threading
import time
import binascii

import codecs

import _thread
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
        self.ledger = dict()
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

    def run(self, blocks=1):
        # -1  -> no limit
        # 1: -> mine until this amout of block are mined
        block_nr = self.chain[-1]["id"]
        self.transactions.append(self.transaction(self.public_key, 1, sender=""))
        while self.chain[-1]["id"] != block_nr + blocks:
            block_hash = hash_block(self.chain[-1])
            random_str = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
            dk = hashlib.pbkdf2_hmac('sha1', block_hash, str.encode(random_str), 100)
            if binascii.hexlify(dk)[-1:] == b'f':
                print(random_str)
                block = {
                    "id": len(self.chain),
                    "proof": random_str,
                    "transactions": self.transactions,
                    "previous_hash": block_hash
                }
                # reset transcations
                self.transactions = []
                self.transactions.append(self.transaction(self.public_key, 1, sender=""))
                self.broadcast(block, "pow")
                self.chain.append(block)
                if not self.public_key in self.ledger:
                    self.ledger[self.public_key] = 1
                else:
                    self.ledger[self.public_key] += 1

            self.calls += 1
            time.sleep(self.delay)
        _thread.exit()

    # VERIFICATION
    def verify_new_block(self, block):
        if block["id"] != len(self.chain):
            return False

        block_hash = hash_block(self.chain[-1])
        dk = hashlib.pbkdf2_hmac('sha1', block_hash, str.encode(block["proof"]), 100)
        if not binascii.hexlify(dk)[-1:] == b'f':
            return False

        block_reward = False
        for transaction in block["transactions"]:
            if self.verify_transaction(transaction) is False:
                if transaction["sender"] == "":
                    if block_reward is True:
                        return False
                    block_reward = True
                    if transaction["amount"] != 1:
                        return False
                    print("VER")
                    if not transaction["to"] in self.ledger:
                        self.ledger[transaction["to"]] = 1
                    else:
                        self.ledger[transaction["to"]] += 1

                else:
                    return False

        return True

    def verify_transaction(self, transaction):
        if not "sender" in transaction.keys():
            return False

        if not transaction["sender"] in self.ledger:
            return False
        # todo: check if sum is spendable

        if self.ledger[transaction["sender"]] < transaction["amount"]:
            return False
        else:
            self.ledger[transaction["sender"]] -= transaction["amount"]

        transaction_copy = dict(transaction)
        signatur = transaction_copy["signature"]
        transaction_copy.pop('signature', None)
        transaction_string = str(transaction_copy)

        public_key = transaction_copy["sender"]

        try:
            vk = VerifyingKey.from_string(bytes.fromhex(public_key), curve=ecdsa.SECP256k1)
            if vk.verify(bytes.fromhex(signatur), transaction_string.encode()) is True:
                return True
            else:
                return False
        except:
            return False

    def verify(self, chain):
        # todo
        # todo: verfiy the validity of a chain
        # todo: has to verify all blocks/transactions
        pass

    def transaction(self, to, amount, sender=None):
        if sender is None:
            sender = self.public_key
        transaction = {
            'sender': sender,
            'to': to,
            'amount': amount,
        }

        transaction_string = str(transaction)
        p_key = SigningKey.from_string(bytes.fromhex(self.__private_key), curve=ecdsa.SECP256k1)
        signature = p_key.sign(transaction_string.encode())
        transaction["signature"] = codecs.encode(signature, 'hex').decode("utf-8")
        return transaction

    def send(self, to, amount):
        t = self.transaction(to, amount)
        self.transactions.append(t)
        self.broadcast(t, "tra")

    # COMMUNICATION
    # SEND:
    def broadcast(self, data, type=None):
        if type == "pow":
            for miner in self.network.miners:
                if miner != self:
                    miner.broadcast_proof_of_work(data)

        if type == "tra":
            for miner in self.network.miners:
                if miner != self:
                    miner.broadcast_transaction(data)

    # RECEIVE:
    def broadcast_proof_of_work(self, block):
        if block["id"] != len(self.chain):
            return

        if self.verify_new_block(block) == True:
            self.transactions = []
            self.transactions.append(self.transaction(self.public_key, 1, sender=""))
            self.chain.append(block)

        # todo: mabey there are multiple blocks to verify


    def broadcast_transaction(self, transaction):
        if self.verify_transaction(transaction) is True:
            self.transactions.append(transaction)
        pass
