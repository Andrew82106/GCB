import random
from Transactions import MerkleTree
from GCBChainStructure import Block, Chain


class Miner:
    def __init__(self, MinerAddress):
        self.address = MinerAddress
        self.defaultChain = Chain('')

    def mine(self, preBlocksTLst, preHash, transaction):
        while 1:
            nonce = random.randint(1, 1000000)
            MTree = MerkleTree(preBlocksTLst + [transaction])
            newBlock = Block(MTree, nonce, preHash)
            if self.defaultChain.checkHash(newBlock.block_hash):
                return nonce, newBlock