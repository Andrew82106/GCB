import random
from base.baseCFG import *
from base.GCBChainStructure import *
from base.User import *
from base.Miner import *

#server 的任务:1. 生成区块 2. 验证交易 3. 验证区块 4. 广播区块 5. 存储区块 6.存储交易 7.接受广播
import server_h

def server_init(ipaddress, N,status,timestamp,chain,port=8848,name="default"):
    server = server_h.Server(ipaddress, port, N, name, status, timestamp,chain)
# 向网络广播本机情况

# 向其他node建立连接请求获取链数据
def connect_to_nodes():

# 导入区块链
blockchain = Chain()