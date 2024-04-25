import random
from Transactions import MerkleTree
from GCBChainStructure import Block, Chain


class Miner:
    def __init__(self, MinerAddress):
        self.address = MinerAddress
        self.defaultChain = Chain('')

    def mine(self, preBlocksTLst, preHash, transaction):
        print("Mining......")
        while 1:
            nonce = random.randint(1, 100000000)
            MTree = MerkleTree(preBlocksTLst + [transaction])
            newBlock = Block(MTree, nonce, preHash)
            if self.defaultChain.checkHash(newBlock.block_hash):
                print("Mining Success!")
                return nonce, newBlock