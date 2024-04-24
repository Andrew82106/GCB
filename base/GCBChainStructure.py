from baseCFG import PathCFG
from utils.hashTools import *
from Transactions import Transaction, MerkleTree
import pickle
from typing import List
cfg = PathCFG()
hashTool = hashTool()


class Block:
    def __init__(self, data, nonce, prehash):
        self.prehash = prehash  # 前哈希
        self.timestamp = time.time_ns()  # 区块时间戳
        self.data = data  # 区块数据项
        self.data: MerkleTree
        self.nonce = nonce  # nonce
        self.block_hash = self._generate_hash()  # 本区块哈希

    def _generate_hash(self):
        # 返回由prehash、timestamp、data、nonce生成的哈希值
        hashLst = [self.prehash, str(self.timestamp), str(self.data), str(self.nonce)]
        hashStr = ''.join(hashLst)
        return hashTool.hashFunc(hashStr)


class Chain:
    def __init__(self, minerAddress):
        # super().__init__()
        self.Blocks = []  # 区块存储位置
        self.Blocks: List[Block]
        # 添加类型提示，self.Blocks中的元素都是Block类型
        self._difficulty = 1  # 挖矿难度
        self._minerAddress = minerAddress  # 本链创建者
        self._initHash = '0' * hashTool.hashLength  # 默认创世区块前哈希
        self._createGenesisBlock()  # 创建创世区块

    def _createGenesisBlock(self):
        # 创建创世交易
        genesisTransaction = Transaction(self._minerAddress, '0', 0, time.time_ns())
        # 创建创世区块的Merkle树
        genesisMerkleTree = MerkleTree([genesisTransaction])
        # 将创世交易添加到创世区块中
        self.Blocks.append(Block(genesisMerkleTree, 0, self._initHash))

    def checkHash(self, Hash: str):
        # 校验哈希值是否合法
        for index in range(self._difficulty):
            if Hash[index] != '0':
                return False
        return True

    def chainLocalSaver(self, chainPath):
        # 将链存到本地，以pkl的形式存储
        with open(chainPath, 'wb') as f:
            pickle.dump(self, f)

    def createNewBlock(self, newBlock):
        # 检查新区块的哈希值是否符合要求
        if self.checkHash(newBlock.block_hash):
            self.Blocks.append(newBlock)
            return True
        else:
            return False

    def debugOutputChain(self):
        print(f"\n\n\nBlock Debug" + "||" * 100)
        # 打印Chain中的所有信息
        for index, block in enumerate(self.Blocks):
            print(f"Block {index}" + ">"*50)
            print(f'prehash: {block.prehash}')
            print(f'timestamp: {block.timestamp}')
            block.data.debugOutputChain()
            print(f'nonce: {block.nonce}')
            print(f'block_hash: {block.block_hash}')
            print(">"*50)
        print(f"Block Debug" + "||" * 100 + "\n\n\n")



if __name__ == '__main__':
    # 测试代码
    NewChain = Chain('123')

    # 用for循环随机定义10个交易
    TLst = []
    for i in range(10):
        TLst.append(Transaction(f'sender{i}', f'recipient{i**3}', i, time.time_ns()))

    MT = MerkleTree(TLst)
    print(MT.rootHash)
