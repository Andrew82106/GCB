import random

from base.pathconfig import Pathconfig

cfg = Pathconfig()

from base.webconnnection.client import client
from base.GCBChainStructure import Chain, Block
from base.GCBChainStructure import Transaction, MerkleTree
from base.User import UserPool
from base.config import *

userPool = UserPool()


class miner_client(client):
    """
    模拟一个客户端代码（挖矿并请求添加）
    """
    def __init__(self, address):
        super().__init__()
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
        res_ = self.post(self.GCBmsg(newBlock, 2))
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
    print("end")

