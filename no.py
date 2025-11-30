# node.py
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
        # Em uma rede real, enviaríamos via socket / HTTP.
        # Aqui propagamos chamando método de cada peer.
        for p in self.peers:
            p.receive_block(block)

    def receive_block(self, block: Block):
        # versão simples: aceitar se predecessor bater e índice for esperado
        last = self.blockchain.last_block()
        if block.previous_hash == last.hash and block.index == last.index + 1:
            # append block (assume block.hash já foi calculado pelo minerador)
            self.blockchain.chain.append(block)
            # limpar mempool local que estão na block (simples)
            # nota: abordagem didática, não completa
            self.blockchain.pending_transactions = [tx for tx in self.blockchain.pending_transactions if tx not in block.transactions]
        else:
            # conflito: pedir chain do peer (na simulação, iremos recarregar)
            self.consensus()

    def consensus(self):
        # pega a cadeia mais longa entre peers
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
            # after mining, broadcast to peers
            self.broadcast_block(block)
        return block
