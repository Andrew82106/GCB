from baseCFG import PathCFG
from utils.hashTools import *
import pickle
from typing import List
cfg = PathCFG()
hashTool = hashTool()


class Transaction:
    def __init__(self, sender, recipient, amount, time_stamp):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.time_stamp = time_stamp
        self.hash = hashTool.hashFunc(str(self.sender) + str(self.recipient) + str(self.amount) + str(self.time_stamp))


class MerkleTree:
    def __init__(self, TransactionLst: List[Transaction], Type=0):
        self.type = Type
        # type=0则该保存全量交易
        # type=1则该保存根节点交易哈希值
        self.MTreeLst = TransactionLst if Type == 0 else None
        self.rootHash = self._hashMTree(TransactionLst)

    @staticmethod
    def _hashMTree(TransactionLst):
        # 将self.MTree中的每个交易进行迭代式哈希，得到根节点哈希
        lst = [instance.hash for instance in TransactionLst]
        while len(lst) > 1:
            # print(lst)
            lst1 = []
            for index in range(0, len(lst)-1, 2):
                lst1.append(hashTool.hashFunc(lst[index] + lst[index + 1]))
            if len(lst) % 2:
                lst1.append(lst[-1])
            lst = lst1
        assert len(lst) == 1, 'Merkle Tree哈希错误'
        return lst[0]


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
        self._Blocks = []  # 区块存储位置
        self._Blocks: List[Block]
        # 添加类型提示，self.Blocks中的元素都是Block类型
        self._difficulty = 4  # 挖矿难度
        self._minerAddress = minerAddress  # 本链创建者
        self._initHash = '0' * hashTool.hashLength  # 默认创世区块前哈希
        self._createGenesisBlock()  # 创建创世区块

    def _createGenesisBlock(self):
        self._Blocks.append(Block(self._minerAddress, 0, self._initHash))

    def chainLocalSaver(self, chainPath):
        # 将链存到本地，以pkl的形式存储
        with open(chainPath, 'wb') as f:
            pickle.dump(self, f)

    def _checkHash(self, Hash: str):
        # 校验哈希值是否合法
        for index in range(self._difficulty):
            if Hash[index] != '0':
                return False
        return True

    def createNewBlock(self, data, nonce):
        # 向链中添加一个新区块
        newBlock = Block(data, nonce, self._Blocks[-1].block_hash)
        if self._checkHash(newBlock.block_hash):
            self._Blocks.append(newBlock)
            return True
        else:
            return False



if __name__ == '__main__':
    # 测试代码
    NewChain = Chain('123')

    # 用for循环随机定义10个交易
    TLst = []
    for i in range(10):
        TLst.append(Transaction(f'sender{i}', f'recipient{i**3}', i, time.time_ns()))

    MT = MerkleTree(TLst)
    print(MT.rootHash)
