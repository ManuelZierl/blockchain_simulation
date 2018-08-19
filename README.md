#### ABSTRACT

This repository should emulate a blockchain on one computer.
Each node runs in its own thread. The purpose is to get a better understanding of the blockchain technology and to be 
able to simulate and understand certain scenarios without the use of several computers. 

This repository is not complete yet and blockchain enthusiastic contributors are welcome!



#### SIMPLE EXAMPLE

Here is a simple example of what is already possible:

```python
from Network import Network
from Miner import Miner

network = Network()
network.new_miners(3, 10) # add 3 new trusfull miners with a computing power of 10
```
```python
network.start_working(blocks=6) # let the nodes mine for 6 blocks
```
    MINER 2  FOUND BLOCK
    MINER 1  FOUND BLOCK
    MINER 1  FOUND BLOCK
    MINER 1  FOUND BLOCK
    MINER 1  FOUND BLOCK
    MINER 1  FOUND BLOCK

```python
network.consensus() # check if all nodes have the same chain and the same ledger
```
    True
    
```python
network.nodes[0].show_ledger()
```

    LEDGER OF MINER 0: 
      MINER 2 (e25db...): 1
      MINER 1 (53c2b...): 5
```python
network.nodes[0].show_chain()
```
     +---------------------+  +---------------------+  +---------------------+  +---------------------+
     | BLOCK NR: 0         |  | BLOCK NR: 1         |  | BLOCK NR: 2         |  | BLOCK NR: 3         |
     + - - - - - - - - - - +  + - - - - - - - - - - +  + - - - - - - - - - - +  + - - - - - - - - - - +
     | PROOF: ifrt153ouh   |  | PROOF: wabhyco48j   |  | PROOF: 5yqgstsy31   |  | PROOF: lk639by7ob   |
     + - - - - - - - - - - +  + - - - - - - - - - - +  + - - - - - - - - - - +  + - - - - - - - - - - +
     | TRANSACTIONS: 0     |  | TRANSACTIONS: 1     |  | TRANSACTIONS: 1     |  | TRANSACTIONS: 1     |
     + - - - - - - - - - - +  |                     |  |                     |  |                     |
     | DIFF: 1             |  | from: rewar         |  | from: rewar         |  | from: rewar         |
     + - - - - - - - - - - +  | to: e25db...        |  | to: 53c2b...        |  | to: 53c2b...        |
     | PREV_H: genes...    |  | amount: 1           |  | amount: 1           |  | amount: 1           |
     +---------------------+  + - - - - - - - - - - +  + - - - - - - - - - - +  + - - - - - - - - - - +
                              | DIFF: 2             |  | DIFF: 2             |  | DIFF: 2             |
                              + - - - - - - - - - - +  + - - - - - - - - - - +  + - - - - - - - - - - +
                              | PREV_H: b'def2f'... |  | PREV_H: b'31bc4'... |  | PREV_H: b'ad46e'... |
                              +---------------------+  +---------------------+  +---------------------+
    
     +---------------------+  +---------------------+  +---------------------+
     | BLOCK NR: 4         |  | BLOCK NR: 5         |  | BLOCK NR: 6         |
     + - - - - - - - - - - +  + - - - - - - - - - - +  + - - - - - - - - - - +
     | PROOF: 00fq0tywq3   |  | PROOF: kz1rq3f0wd   |  | PROOF: x3kiwkxsku   |
     + - - - - - - - - - - +  + - - - - - - - - - - +  + - - - - - - - - - - +
     | TRANSACTIONS: 1     |  | TRANSACTIONS: 1     |  | TRANSACTIONS: 1     |
     |                     |  |                     |  |                     |
     | from: rewar         |  | from: rewar         |  | from: rewar         |
     | to: 53c2b...        |  | to: 53c2b...        |  | to: 53c2b...        |
     | amount: 1           |  | amount: 1           |  | amount: 1           |
     + - - - - - - - - - - +  + - - - - - - - - - - +  + - - - - - - - - - - +
     | DIFF: 2             |  | DIFF: 2             |  | DIFF: 2             |
     + - - - - - - - - - - +  + - - - - - - - - - - +  + - - - - - - - - - - +
     | PREV_H: b'4ffd4'... |  | PREV_H: b'97c4e'... |  | PREV_H: b'6de48'... |
     +---------------------+  +---------------------+  +---------------------+


### 51% ATTACK

Here is a simple demonstration for a 51% Attack:


```python
from Network import Network
from Miner import Miner
from Evil_Miner import Evil_Miner

network = Network()
# 3 honest miners with a power of 6
miner_0 = Miner(network, 6) 
miner_1 = Miner(network, 6)
miner_2 = Miner(network, 6)
# 1 evil Miner with a power of 50
evil_miner_3 = Evil_Miner(network, 50, secret_working=False) 

network.add_node(miner_0)
network.add_node(miner_1)
network.add_node(miner_2)
network.add_node(evil_miner_3)

# mine 10 blocks
network.start_working(blocks=10)
```
    MINER 1  FOUND BLOCK
    EVIL_MINER 3  FOUND BLOCK
    EVIL_MINER 3  FOUND BLOCK
    EVIL_MINER 3  FOUND BLOCK
    EVIL_MINER 3  FOUND BLOCK
    MINER 2  FOUND BLOCK
    EVIL_MINER 3  FOUND BLOCK
    EVIL_MINER 3  FOUND BLOCK
    EVIL_MINER 3  FOUND BLOCK
    EVIL_MINER 3  FOUND BLOCK
    
```python
network.consensus() # everything fine so far
```
    True
```python
network.nodes[0].show_ledger()
```
    LEDGER OF MINER 0: 
       MINER 1 (fe047... ): 1
       MINER 3 (07459... ): 8
       MINER 2 (6dbf9... ): 1

```python
# send to miner_0 an amout of 8
evil_miner_3.send(miner_0.public_key, 8)

# from now on work secretly own chain. Find blocks but dont broadcast them
evil_miner_3.secret_working = True

```
```python
len(evil_miner_3.transactions)
```
    2
```python
del evil_miner_3.transactions[1]
```
```python
len(evil_miner_3.transactions)
```
    1
```python
evil_miner_3.transactions
```
    [{'sender': '',
      'to': '0745903784bf1547aa8aca26fcd000d34d03b88b7ef9ace36b6e9c19ea5bdf53ae76233320dc7eea3df98177bc23afcec44a816f8d5ee6f58bd23b0089f3cca5',
      'amount': 1,
      'signature': '72d9f41f9770953604a57d7dce351fc9722ce522128fb270eeedc6022688ac0acf579e99dc6f61c0ac4bc0d503d09a4e27d59d78cc097fd87377480ff611d6a9'}]

```python
network.start_working(blocks=100, time=30)
```
    EVIL_MINER 3  FOUND BLOCK
    EVIL_MINER 3  FOUND BLOCK
    MINER 0  FOUND BLOCK
    EVIL_MINER 3  FOUND BLOCK
    EVIL_MINER 3  FOUND BLOCK
    EVIL_MINER 3  FOUND BLOCK
    EVIL_MINER 3  FOUND BLOCK
 
```python
network.consensus()
```
    True
```python
len(miner_0.chain)
```
    12
```python
len(evil_miner_3.chain), len(evil_miner_3.secret_chain)
```
    (12, 17) // evil miner has a longer secret chain
```python
network.nodes[0].show_ledger() # correct chain
```
    LEDGER OF MINER 0: 
       MINER 1 (fe047... ): 1
       MINER 3 (07459... ): 0
       MINER 2 (6dbf9... ): 1
       MINER 0 (4302d... ): 9   
```python
# no send the secret chain as broadcast to the other nodes
evil_miner_3.send_broadcast({"type": "pow", "chain": evil_miner_3.secret_chain})
```
```python
len(miner_0.chain)
```
    17
```python
miner_0.show_ledger()
```
    LEDGER OF MINER 0: 
       MINER 1 (fe047... ): 1
       MINER 3 (07459... ): 14
       MINER 2 (6dbf9... ): 1
       
the first transaction was reset