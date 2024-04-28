import random
import time

from base.pathconfig import Pathconfig

cfg = Pathconfig()

from base.sockets.Client import client
from base.GCBChainStructure import Chain, Block
from base.GCBChainStructure import Transaction, MerkleTree


class debug_client(client):
    """
    模拟一个客户端代码（只查询）
    """
    def __init__(self):
        super().__init__()

    def fetch(self, info='query for chain') -> Chain:
        info = self.GCBmsg(info, 1)
        res_ = self.request(info)
        res_ = self.extract_msg(res_)
        return res_


class miner_client(client):
    """
    模拟一个客户端代码（挖矿并请求添加）
    """
    def __init__(self):
        super().__init__()

    def mine(self, info='query for chain') -> Chain:
        info = self.GCBmsg(info, 1)
        res_ = self.request(info)
        res_ = self.extract_msg(res_)
        res_: Chain
        lastestBlock = res_.latestBlock
        lastestBlock: Block
        newTranscation = Transaction(sender='sender', recipient='recipient', amount=10)

        print('mining...')
        while True:
            nonce = random.randint(1, 100000)
            newData = MerkleTree([newTranscation])
            newBlock = Block(data=lastestBlock.data + newData, nonce=nonce, prehash=lastestBlock.block_hash)
            if res_.createNewBlock(newBlock):
                print(f"mine a new block: nonce={nonce}")
                break

        return newBlock

    def update(self, newBlock: Block):
        res_ = c.request(newBlock, 2)
        res_ = self.extract_msg(res_)
        print(res_)


if __name__ == '__main__':

    c = debug_client()
    res = c.fetch('查询最新链')
    res.debugOutputChain()

    time.sleep(1)
    c = miner_client()
    res = c.mine('查询最新链')
    c.update(res)
    time.sleep(1)


    c = debug_client()
    res = c.fetch('查询最新链')
    res.debugOutputChain()
    print("end")

