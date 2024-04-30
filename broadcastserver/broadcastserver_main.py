import random
import time

from base.pathconfig import *
from base.GCBChainStructure import *
from base.User import *
from base.Miner import *

'''
broadcastserver 的任务:
6. 存储总链
1. 接收连接并将ip存储
2. 向request的ip发送链文件
3. 监听模式
4. 接受miner广播的区块并验证，将区块连接到链上
5. 向iplist中的ip广播区块 
'''
import broadcastserver_h as broadcast_h

def server_init(ipaddress, remoteipaddress,status,timestamp,chain,port=8848,name="default"):
    server = broadcast_h.Server(ipaddress, port, remoteipaddress, name, status, timestamp,chain)
# 向网络广播本机情况

# 向其他node建立连接请求获取链数据
def request_to_net():
    return 0

# 接收连接并将ip存储
def receive_connection(ipaddress, port):
    return 0

# 挖矿生成新区块
def mine():
    return 0

# broadcastBlock
def broadcastBlock():
    return 0


# 监听模式
def monitormode():
    return 0

# 存储
def storage():
    return 0

if __name__ == '__main__':
    time_now = time.time_ns()
    server_init("127.0.0.1","remoteipaddress",0,time_now)