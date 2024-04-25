import os
import sys
import pickle
''' server 的键值
    ipaddress:127.0.0.1
    status:(0)broadcast_server, (1)only_mine_server, (2) 
    timestamp:上一次更新时间
    
'''
class Server():
    #初始化服务器
    def __init__(self, ipaddress, port, net, name, status, timestamp,chain=None):
        # super().__init__()
        self.ipaddress = ipaddress  # 区块存储位置
        self.port = port
        self.net = net #main_net_ip
        self.name = name #服务器名称
        self.status = status  # 状态
        self.timestamp = timestamp  # 上一次更新时间
        self.chain = chain #chain


    def _checkchain(self):
        # 创建创世交易
        genesisTransaction = Transaction(self._minerAddress, '0', 0, time.time_ns())
        # 创建创世区块的Merkle树
        genesisMerkleTree = MerkleTree([genesisTransaction])
        # 将创世交易添加到创世区块中
        self.Blocks.append(Block(genesisMerkleTree, 0, self._initHash))

    #导入链
    def LoadChainpkl(self, ChainPath):
        # 将pkl的形式存储链展开，
        with open(ChainPath, 'wb') as f:
            pickle.load(self, f)

    #导入链
    def expkl(self, pkl):
        # 校验哈希值是否合法
        for index in range(self._difficulty):
            if Hash[index] != '0':
                return False
        return True

    #向网络广播新区块
    def broadcast(self):

    def LoadChain(self, ChainPath):
        # 将链存到本地，以pkl的形式存储
        with open(ChainPath, 'wb') as f:
            pickle.load(self, f)

    def createNewBlock(self, newBlock):
        # 检查新区块的哈希值是否符合要求
        if self.checkHash(newBlock.block_hash):
            self.Blocks.append(newBlock)
            return True
        else:
            return False




    def DebugServer(self):
        print(f"\n\n\nServer Debug" + "||" * 100)
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
