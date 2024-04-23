from baseCFG import PathCFG
from Utils.hashTools import *
import pickle
from typing import List
cfg = PathCFG()
hashTool = hashTool()


class Block:
    def __init__(self, data, nonce, prehash):
        self.prehash = prehash  # 前哈希
        self.timestamp = time.time_ns()  # 区块时间戳
        self.data = data  # 区块数据项
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
        self.difficulty = 4  # 挖矿难度
        self.minerAddress = minerAddress  # 本链创建者
        self.initHash = '0' * hashTool.hashLength  # 默认创世区块前哈希
        self._createGenesisBlock()  # 创建创世区块

    def _createGenesisBlock(self):
        self.Blocks.append(Block(self.minerAddress, 0, self.initHash))

    def chainLocalSaver(self, chainPath):
        # 将链存到本地，以pkl的形式存储
        with open(chainPath, 'wb') as f:
            pickle.dump(self, f)

    def _checkHash(self, Hash: str):
        # 校验哈希值是否合法
        for index in range(self.difficulty):
            if Hash[index] != '0':
                return False
        return True

    def createNewBlock(self, data, nonce):
        # 向链中添加一个新区块
        newBlock = Block(data, nonce, self.Blocks[-1].block_hash)
        if self._checkHash(newBlock.block_hash):
            self.Blocks.append(newBlock)
            return True
        else:
            return False



if __name__ == '__main__':
    # 测试代码
    NewChain = Chain('123')
