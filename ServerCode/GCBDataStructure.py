from baseCFG import PathCFG
from Utils.hashTools import *
import pickle
from typing import List
cfg = PathCFG()
hashTool = hashTool()


class MerkleTree:
    def __init__(self):
        self.tree = []

    def add(self, data):
        self.tree.append(data)

    def _hash(self, data):
        return hashTool.hashFunc(data)

    def _build(self):
        # 构建Merkle树
        if len(self.tree) == 0:
            return
        # 计算叶子节点数量
        num_leaves = len(self.tree)
        # 计算层数
        levels = 1
        while 2 ** levels < num_leaves:
            levels += 1

        # 构建树
        self.tree.insert(0, '')
        for i in range(levels, 0, -1):
            # 计算当前层节点数量
            num_nodes = len(self.tree)
            # 计算当前层节点索引
            idx = 0
            while idx < num_nodes:
                # 计算当前节点哈希值
                left_child = self.tree[idx]
                right_child = self.tree[idx + 1] if idx + 1 < num_nodes else ''
                self.tree[i - 1] = self._hash(left_child + right_child)
                idx += 2

    def getRoot(self):
        # 获取Merkle树的根节点
        self._build()
        return self.tree[0]

    def getProof(self, data):
        # 获取数据在Merkle树中的证明
        self._build()
        idx = self.tree.index(data)
        proof = []
        for i in range(1, len(self.tree)):
            if idx % 2 == 0:
                proof.append(self.tree[i - 1])
                idx = idx // 2
            else:
                proof.append(self.tree[i])
                idx = (idx - 1) // 2

        return proof

    def verify(self, data, proof, root):
        # 验证数据在Merkle树中的证明
        hash_data = self._hash(data)
        for node in proof:
            if hash_data < node:
                hash_data = self._hash(hash_data + node)
            else:
                hash_data = self._hash(node + hash_data)

        return hash_data == root


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
