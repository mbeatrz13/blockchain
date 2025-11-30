from typing import List
from blockchain import Blockchain, Block

class Node:
    def __init__(self, name: str, difficulty: int = 3):
        self.name = name
        self.blockchain = Blockchain(difficulty=difficulty)
        self.peers: List['Node'] = []

    def connect_peer(self, peer: 'Node'):
        if peer not in self.peers and peer is not self:
            self.peers.append(peer)

    def broadcast_block(self, block: Block):
        for p in self.peers:
            p.receive_block(block)

    def receive_block(self, block: Block):
        last = self.blockchain.last_block()
        if block.previous_hash == last.hash and block.index == last.index + 1:
            # append block (assume block.hash já foi calculado pelo minerador)
            self.blockchain.chain.append(block)
            self.blockchain.pending_transactions = [tx for tx in self.blockchain.pending_transactions if tx not in block.transactions]
        else:
            self.consensus()

    def consensus(self):
        longest = self.blockchain
        for p in self.peers:
            if len(p.blockchain.chain) > len(longest.chain) and p.blockchain.is_valid():
                longest = p.blockchain
        if longest is not self.blockchain:
            self.blockchain = longest

    def add_transaction(self, sender: str, recipient: str, amount: float):
        self.blockchain.add_transaction(sender, recipient, amount)

    def mine(self):
        block = self.blockchain.mine_pending(self.name)
        if block:
            self.broadcast_block(block)
        return block
