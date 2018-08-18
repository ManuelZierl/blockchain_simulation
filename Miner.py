import hashlib
import random
import string
import threading
import time
import binascii
import codecs
import sys
import ecdsa
import json
from copy import copy
from ecdsa import SigningKey
from ecdsa import VerifyingKey
from Node import Node

def hash_block(block):
    block_string = str(block)
    return binascii.hexlify(hashlib.pbkdf2_hmac('sha1', str.encode(block_string), b'valarmorghulis', 100))

class Miner(Node):
    def __init__(self, network, power=1, chain=None):
        Node.__init__(self, network, power=power)

        self.ledger = dict()
        self.chain = []
        self.LOCK = threading.Lock()
        if chain is None:
            with open('genesis_block.json') as data_file:
                self.chain = json.load(data_file)
        else:
            for i in range(1, len(chain) + 1):
                self.chain.append(chain[i - 1])

                if i < len(chain):
                    if self.verify_new_block(chain[i]) is False:
                        raise Exception("YOU HAVE TYRIED TO INIT A NEW NODE WITH A INVALID CHAIN")

        private_key = SigningKey.generate(curve=ecdsa.SECP256k1)
        public_key = private_key.get_verifying_key()

        self.__private_key = codecs.encode(private_key.to_string(), 'hex').decode("utf-8")
        self.public_key = codecs.encode(public_key.to_string(), 'hex').decode("utf-8")

        self.transactions = []
        self.transactions.append(self.transaction(self.public_key, 1, sender=""))

    def work(self):
        while self.blocks_to_go > 0:
            block_hash = hash_block(self.chain[-1])
            random_str = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
            dk = hashlib.pbkdf2_hmac('sha1', block_hash, str.encode(random_str), 100)
            if binascii.hexlify(dk)[-1 * self.network.difficulty:] == b'f' * self.network.difficulty:
                print("MINER " + str(self.id) + "  FOUND BLOCK")
                block = {
                    "id": len(self.chain),
                    "proof": random_str,
                    "transactions": self.transactions,
                    "difficulty": self.network.difficulty,
                    "previous_hash": block_hash
                }

                self.transactions = []
                self.transactions.append(self.transaction(self.public_key, 1, sender=""))

                new_chain = self.chain + [block]
                self.send_broadcast({"type": "pow", "chain": new_chain})

            self.calls += 1
            time.sleep(self.delay)

    # VERIFICATION
    def verify_new_block(self, block):
        if block["id"] != len(self.chain):
            return False

        block_hash = hash_block(self.chain[-1])
        dk = hashlib.pbkdf2_hmac('sha1', block_hash, str.encode(block["proof"]), 100)
        difficulty = block["difficulty"]
        if not binascii.hexlify(dk)[-1 * difficulty:] == b'f' * difficulty:
            return False

        reward = None
        for transaction in block["transactions"]:
            if self.verify_transaction(transaction) is False:
                if transaction["sender"] == "":
                    if reward is not None:
                        return False
                    if transaction["amount"] != 1:
                        return False

                    reward = transaction["to"]
                else:
                    return False

        for transaction in block["transactions"]:
            if transaction["sender"] != "":
                self.ledger[transaction["sender"]] -= transaction["amount"]
                if transaction["to"] not in self.ledger:
                    self.ledger[transaction["to"]] = transaction["amount"]
                else:
                    self.ledger[transaction["to"]] += transaction["amount"]

        if reward not in self.ledger:
            self.ledger[reward] = 1
        else:
            self.ledger[reward] += 1

        return True

    def verify_transaction(self, transaction):
        if "sender" not in transaction.keys():
            return False

        if not transaction["sender"] in self.ledger:
            return False

        if self.ledger[transaction["sender"]] < transaction["amount"]:
            return False

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
        self.send_broadcast({"type": "tra", "transaction": t})

    def receive_broadcast(self, data):
        self.LOCK.acquire()
        if data["type"] == "pow":
            self.broadcast_proof_of_work(data["chain"])

        if data["type"] == "tra":
            self.broadcast_transaction(data["transaction"])
        self.LOCK.release()

    def broadcast_proof_of_work(self, chain):
        if len(chain) <= len(self.chain):
            return

        last_matching = None
        for i in range(len(self.chain)):
            if chain[i] == self.chain[i]:
                last_matching = i

        new_blocks = chain[last_matching + 1:]
        old_chain = copy(self.chain)
        old_ledger = copy(self.ledger)

        for block in new_blocks:
            if self.verify_new_block(block):
                self.chain.append(block)
            else:
                self.chain = old_chain
                self.ledger = old_ledger
                return

        self.blocks_to_go -= len(new_blocks)

        self.transactions = []
        self.transactions.append(self.transaction(self.public_key, 1, sender=""))

    def broadcast_transaction(self, transaction):
        if self.verify_transaction(transaction) is True:
            self.transactions.append(transaction)
        pass

    # console utils
    def show_ledger(self):
        sys.stdout.write( "LEDGER OF MINER "+ str(self.id) + ": " + "\n")
        miners = self.network.nodes
        for key in self.ledger.keys():
            id = next(x.id for x in self.network.nodes if x.public_key == key)
            sys.stdout.write("   MINER " + str(id) + " (" + str(key[:5]) + "... ): " + str(self.ledger[key]) + "\n")
        sys.stdout.write("\n\n")

    def show_chain(self):
        for block in self.chain:
            sys.stdout.write (" +---------------------+\n") # 24 + - - - - - - - - - - +
            sys.stdout.write((" | BLOCK NR: " + str(block["id"])).ljust(23) + "|\n")
            sys.stdout.write (" + - - - - - - - - - - +\n")
            sys.stdout.write((" | PROOF: " + str(block["proof"])).ljust(23) + "|\n")
            sys.stdout.write (" + - - - - - - - - - - +\n")
            sys.stdout.write((" | TRANSACTIONS: " + str(len(block["transactions"]))).ljust(23) + "|\n")
            for transaction in block["transactions"]:
                sender = transaction["sender"]
                if sender == "":
                    sender = "reward"
                sys.stdout.write(" |                     |\n")
                sys.stdout.write((" | from: "+ str(sender)[:7] + "...").ljust(23) +"|\n")
                sys.stdout.write((" | to: "+ str(transaction["to"][:8]) + "...").ljust(23) +"|\n")
                sys.stdout.write((" | amount: "+ str(transaction["amount"])).ljust(23) +"|\n")

            sys.stdout.write(" + - - - - - - - - - - +\n")
            sys.stdout.write((" | DIFF: " + str(block["difficulty"])).ljust(23) + "|\n")
            sys.stdout.write(" + - - - - - - - - - - +\n")
            sys.stdout.write((" | PREV_H: " + str(block["previous_hash"])[:5] + "...").ljust(23) + "|\n")
            sys.stdout.write(" +---------------------+\n\n")

           # print(block)
            pass

        pass

    def save_chain(self, name):
        with open(name + '.json', 'w') as outfile:
            json.dump(self.chain, outfile)

    def save_ledger(self, name):
        with open(name + '.json', 'w') as outfile:
            json.dump(self.ledger, outfile)
