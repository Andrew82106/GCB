import os.path
from pathconfig import Pathconfig
from utils.hashTools import *
from Transactions import Transaction, MerkleTree
import pickle
from typing import List
cfg = Pathconfig()
hashTool = hashTool()


class Block:
    """
    Block类用于表示区块链中的一个区块。

    Attributes:
        prehash (str): 前哈希
        timestamp (int): 区块时间戳
        data (MerkleTree): 区块数据项
        nonce (int): nonce
        block_hash (str): 本区块哈希

    Methods:
        _generate_hash: 生成哈希值
        blockLocalSaver: 将block存到本地，以pkl的形式存储
    """
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

    def blockLocalSaver(self, blockPath=cfg.blockchain_cache_path, filename=f'block_timestamp_{time.time_ns()}.pkl'):
        # 将block存到本地，以pkl的形式存储
        with open(os.path.join(blockPath, filename), 'wb') as f:
            pickle.dump(self, f)


class Chain:
    """
    Chain类用于表示区块链。

    Attributes:
        Blocks (List[Block]): 区块列表
        _difficulty (int): 挖矿难度
        _minerAddress (str): 矿工地址
        _initHash (str): 创世区块前哈希

    Methods:
        _createGenesisBlock: 创建创世区块
        checkHash: 校验哈希值是否合法
        chainLocalSaver: 将链存到本地，以pkl的形式存储(加载链放在类的外部，即loadChain函数)
        createNewBlock: 检查新区块的哈希值是否符合要求
        debugOutputChain: 打印Chain中的所有信息
        fetchLatestBlock: 返回最新的区块
    """
    def __init__(self, minerAddress):
        # super().__init__()
        self.Blocks = []  # 区块存储位置
        self.Blocks: List[Block]
        # 添加类型提示，self.Blocks中的元素都是Block类型
        self._difficulty = 6  # 挖矿难度
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

    def chainLocalSaver(self, chainPath=cfg.blockchain_cache_path, filename=f'chain_timestamp_{time.time_ns()}.pkl'):
        # 将链存到本地，以pkl的形式存储
        with open(os.path.join(chainPath, filename), 'wb') as f:
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

    @property
    def latestBlock(self):
        # 返回最新的区块
        return self.Blocks[-1]


def loadChain(chainPth=cfg.blockchain_cache_path, filename=None):
    """
    加载区块链

    :param chainPth: 区块链存储路径
    :param filename: 区块链文件名
    :return: 区块链
    """
    if filename is None:
        # 从chainPth读取所有子文件名
        filenames = os.listdir(chainPth)
        mtime = 0
        for name in filenames:
            if 'chain' in name:
                try:
                    t = int(name.split('_')[-1].split('.')[0])
                except:
                    continue
                if mtime < t:
                    mtime = t
                    filename = name
    assert filename is not None, "No chain file found"
    # 从本地加载链
    with open(os.path.join(chainPth, filename), 'rb') as f:
        chain = pickle.load(f)
    return chain


def loadBlock(chainPth=cfg.blockchain_cache_path, filename=None):
    if filename is None:
        # 从chainPth读取所有子文件名
        filenames = os.listdir(chainPth)
        mtime = 0
        for name in filenames:
            if 'block' in name:
                try:
                    t = int(name.split('_')[-1].split('.')[0])
                except:
                    continue
                if mtime < t:
                    mtime = t
                    filename = name
    assert filename is not None, "No block file found"
    # 从本地加载区块
    with open(os.path.join(chainPth, filename), 'rb') as f:
        block = pickle.load(f)
    return block


if __name__ == '__main__':
    # 测试代码
    NewChain = Chain('123')

    # 用for循环随机定义10个交易
    TLst = []
    for i in range(10):
        TLst.append(Transaction(f'sender{i}', f'recipient{i**3}', i, time.time_ns()))

    MT = MerkleTree(TLst)
    print(MT.rootHash)

    NewChain.chainLocalSaver()

    Chain = loadChain()
    Chain.debugOutputChain()

    print("end")


