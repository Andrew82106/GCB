import random
import time

from base.pathconfig import Pathconfig

cfg = Pathconfig()

from base.webconnnection.client import client
from base.GCBChainStructure import Chain, Block
from base.GCBChainStructure import Transaction, MerkleTree
from base.User import UserPool
from base.config import *

userPool = UserPool()


class debug_client(client):
    """
    模拟一个客户端代码（只查询）
    """
    def __init__(self, address, host_, port_):
        super().__init__(host_, port_)
        self.address = address

    def query(self):
        """
        通过发送post请求，查询最新链
        :return: 返回的链数据
        """
        r = self.get()
        assert self.check_format(r), "check_format failed"
        return self.extract_msg(r)

    def queryAssets(self):
        """
        通过发送post请求，查询最新链
        :return: 返回的链数据
        """
        r = self.get()
        assert self.check_format(r), "check_format failed"
        assert isinstance(self.extract_msg(r), Chain), "check_format failed"
        chain_: Chain = self.extract_msg(r)
        assets = chain_.calculateAssets(self.address)
        return assets


class miner_client(client):
    """
    模拟一个客户端代码（挖矿并请求添加）
    """
    def __init__(self, address, host, port):
        super().__init__(host, port)
        self.address = address

    def mine(self, sender='sender', recipent='recipent', amount=10) -> Chain:
        res_ = self.get()
        res_ = self.extract_msg(res_)
        res_: Chain
        lastestBlock = res_.latestBlock
        lastestBlock: Block
        sender_assets = res_.calculateAssets(sender)
        if not sender_assets >= amount:
            print("not enough assets")
            return False
        newTranscation = Transaction(sender=sender, recipient=recipent, amount=amount)
        newTranscation1 = Transaction(sender=ChainMan, recipient=self.address, amount=amount*0.3)
        print('mining...')
        while True:
            nonce = random.randint(1, 100000)
            newData = MerkleTree([newTranscation, newTranscation1])
            newBlock = Block(data=lastestBlock.data + newData, nonce=nonce, prehash=lastestBlock.block_hash)
            if res_.createNewBlock(newBlock):
                print(f"mine a new block: nonce={nonce}")
                break

        return newBlock

    def update(self, newBlock: Block):
        """
        将挖出的块添加到链上
        :param newBlock: 挖出的块，原数据
        :return:
        """
        res_ = c.post(self.GCBmsg(newBlock, 2))
        res_ = self.extract_msg(res_)
        print(res_)
        return 'accepted' in res_

    def queryAssets(self):
        """
        通过发送post请求，查询最新链
        :return: 返回的链数据
        """
        r = self.get()
        assert self.check_format(r), "check_format failed"
        assert isinstance(self.extract_msg(r), Chain), "check_format failed"
        chain_: Chain = self.extract_msg(r)
        assets = chain_.calculateAssets(self.address)
        return assets


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    # 创建一个新用户
    userAddress = userPool.addNewUser(host, port)
    # 创建一个调试客户端
    dc = debug_client(userAddress, host, port)
    # 查询客户端
    res = dc.query()
    # 输出客户端链信息
    res.debugOutputChain()
    # 查询客户端资产
    dc_assets = dc.queryAssets()
    print(f"dc_assets: {dc_assets}")

    # 创建一个新用户
    userAddress1 = userPool.addNewUser(host, port)
    # 创建一个矿工客户端
    c = miner_client(userAddress1, host, port)
    # 挖矿，发送者是ChainMan，接收者是userAddress，金额是1000
    res = c.mine(sender=ChainMan, recipent=userAddress, amount=1000)
    # 如果挖矿成功，更新客户端
    if res:
        c.update(res)

    # 查询客户端资产
    c_assets = c.queryAssets()
    print(f"c_assets: {c_assets}")
    # 查询调试客户端资产
    dc_assets = dc.queryAssets()
    print(f"dc_assets: {dc_assets}")

    # 查询链信息
    chain = dc.query()
    # 计算ChainMan的资产
    chainman_assets = chain.calculateAssets(ChainMan)
    print(f"chainman_assets: {chainman_assets}")


    print("end")

