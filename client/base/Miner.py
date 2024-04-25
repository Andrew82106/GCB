import random
from Transactions import MerkleTree
from GCBChainStructure import Block, Chain


class Miner:
    """
    Miner类用于封装矿工的行为。

    Attributes:
        address (str): 矿工的地址。
        defaultChain (Chain): 矿工默认的区块链副本方法。

    Methods:
        mine(preBlocksTLst, preHash, transaction): 挖矿方法，用于生成新的区块。
    """
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