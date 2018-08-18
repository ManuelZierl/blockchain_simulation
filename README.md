This repository should emulate a blockchain on one computer. 
Each node runs in its own thread. The purpose is to get a better understanding of the blockchain technology and to be 
able to simulate and understand certain scenarios without the use of several computers. 

This repository is not complete yet and blockchain enthusiastic contributors are welcome!

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
