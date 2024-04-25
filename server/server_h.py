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
    def __init__(self, ipaddress, port, net, name, status, timestamp,Chain=None):
        # super().__init__()
        self.ipaddress = ipaddress  # 区块存储位置
        self.port = port
        self.net = net #main_net_ip
        self.name = name #服务器名称
        self.status = status  # 状态
        self.timestamp = timestamp  # 上一次更新时间
        self.Chain = Chain #chain


    #导入链
    def loadChainpkl(self, ChainPath):
        # 将pkl的形式存储链展开，
        with open(ChainPath, 'wb') as f:
            pickle.load(self, f)



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
