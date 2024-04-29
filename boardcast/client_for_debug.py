import random
import time

from base.pathconfig import Pathconfig

cfg = Pathconfig()

from base.webconnnection.client import client
from base.GCBChainStructure import Chain, Block
from base.GCBChainStructure import Transaction, MerkleTree


class debug_client(client):
    """
    模拟一个客户端代码（只查询）
    """
    def __init__(self):
        super().__init__()

    def query(self):
        """
        通过发送post请求，查询最新链
        :return: 返回的链数据
        """
        r = self.get()
        assert self.check_format(r), "check_format failed"
        return self.extract_msg(r)


class miner_client(client):
    """
    模拟一个客户端代码（挖矿并请求添加）
    """
    def __init__(self):
        super().__init__()

    def mine(self) -> Chain:
        res_ = self.get()
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
        """
        将挖出的块添加到链上
        :param newBlock: 挖出的块，原数据
        :return:
        """
        res_ = c.post(self.GCBmsg(newBlock, 2))
        res_ = self.extract_msg(res_)
        print(res_)
        return 'accepted' in res_


if __name__ == '__main__':

    for _ in range(10):
        c = debug_client()
        res = c.query()
        res.debugOutputChain()


        c = miner_client()
        res = c.mine()
        c.update(res)


    print("end")

