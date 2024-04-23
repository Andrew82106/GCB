from baseCFG import PathCFG
from Utils.hashTools import *

cfg = PathCFG()
hashTool = hashTool()


class Block:
    def __init__(self, data, nonce, prehash):
        self.prehash = prehash  # 前哈希
        self.timestamp = time.time_ns()  # 区块时间戳
        self.data = data  # 区块数据项
        self.nonce = nonce  # nonce
        self.block_hash = self.generate_hash()  # 本区块哈希

    def generate_hash(self):
        # 返回由prehash、timestamp、data、nonce生成的哈希值
        return hashTool.hashFunc(self.prehash + str(self.timestamp) + str(self.data) + str(self.nonce))


class Chain:
    def __init__(self, minerAddress):
        # super().__init__()
        self.Blocks = []  # 区块存储位置
        self.difficulty = 4  # 挖矿难度
        self.minerAddress = minerAddress  # 本链创建者
        self.prehash = '0' * hashTool.hashLength  # 默认创世区块前哈希
        self._createGenesisBlock()  # 创建创世区块

    def _createGenesisBlock(self):
        self.Blocks.append(Block(self.minerAddress, 0, self.prehash))

    def createNewBlock(self, data):
        # 向链中添加一个新区块
        new_block_hash = hashTool.hashFunc(self.prehash + str(time.time()) + str(data) + str(0))
        new_block = Block(data, 0, self.Blocks[-1].block_hash)
        self.Blocks.append(new_block)
        self.prehash = new_block_hash



if __name__ == '__main__':
    # 测试代码
    NewChain = Chain('123')
