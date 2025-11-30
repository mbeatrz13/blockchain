# blockchain.py
import hashlib
import json
import time
from typing import List, Dict

class Block:
    def __init__(self, index: int, transactions: List[Dict], previous_hash: str, timestamp: float = None, nonce: int = 0):
        self.index = index
        self.timestamp = timestamp if timestamp is not None else time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = None

    def compute_hash(self) -> str:
        block_content = {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }
        block_string = json.dumps(block_content, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine(self, difficulty: int):
        assert difficulty >= 0
        prefix = '0' * difficulty
        while True:
            self.hash = self.compute_hash()
            if self.hash.startswith(prefix):
                return
            self.nonce += 1

class Blockchain:
    def __init__(self, difficulty: int = 3):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_transactions: List[Dict] = []
        # create genesis block
        genesis = Block(0, [], "0")
        genesis.hash = genesis.compute_hash()
        self.chain.append(genesis)

    def last_block(self) -> Block:
        return self.chain[-1]

    def add_transaction(self, sender: str, recipient: str, amount: float):
        tx = {'sender': sender, 'recipient': recipient, 'amount': amount}
        self.pending_transactions.append(tx)

    def mine_pending(self, miner_address: str):
        if not self.pending_transactions:
            return None
        new_block = Block(len(self.chain), list(self.pending_transactions), self.last_block().hash)
        new_block.mine(self.difficulty)
        self.chain.append(new_block)
        # reward miner (simple fixed reward)
        self.pending_transactions = [{'sender': 'network', 'recipient': miner_address, 'amount': 1}]
        return new_block

    def is_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.previous_hash != previous.hash:
                return False
            if current.compute_hash() != current.hash:
                return False
            if not current.hash.startswith('0' * self.difficulty):
                return False
        return True

    def to_dict(self):
        return [ {
            'index': b.index,
            'timestamp': b.timestamp,
            'transactions': b.transactions,
            'previous_hash': b.previous_hash,
            'nonce': b.nonce,
            'hash': b.hash
        } for b in self.chain ]
