import random

from base.pathconfig import Pathconfig

cfg = Pathconfig()

from base.webconnnection.client import client
from base.GCBChainStructure import Chain, Block
from base.GCBChainStructure import Transaction, MerkleTree
from base.User import UserPool, User
from base.config import *

userPool = UserPool()
userPool.load_userpool_from_pkl()


class miner_client(client):
    """
    模拟一个客户端代码（挖矿并请求添加）
    """
    def __init__(self, address_):
        super().__init__()
        self.address = address_

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
        通过发送post请求，查询当前账号最新资产
        :return: 返回的资产数量
        """
        r = self.get()
        assert self.check_format(r), "check_format failed"
        assert isinstance(self.extract_msg(r), Chain), "check_format failed"
        chain_: Chain = self.extract_msg(r)
        assets = chain_.calculateAssets(self.address)
        return assets


# 首先登录
op = input("1. login\n2. add user\n3. exit\n")
username = None
password = None
user = None
if op == "1":
    username, password = input("username: "), input("password: ")
    user = userPool.login(username, password)
    if user:
        print("login success")

    else:
        print("login failed")
        exit(0)

elif op == "2":
    username, password = input("username: "), input("password: ")
    address = userPool.addNewUser(username, password)
    user = userPool.login(username, password)
    if user:
        print("add user success")
        userPool.save_userpool_to_pkl()
        print("userpool saved")

    else:
        print("add user failed")
        exit(0)

elif op == "3":
    exit(0)


# 然后创建钱包
assert username is not None and password is not None, "username and password must be not None"
user: User
address = user.address
client_instance = miner_client(address)
# 开始处理循环
while 1:
    op = input("1. query chain\n2. queryAssets\n3. mineTranscation\n4. exit\n")
    if op == "1":
        r = client_instance.query()
        r.debugOutputChain()
    elif op == "2":
        r = client_instance.queryAssets()
        print(f"{user.address}: {r}")

    elif op == "3":
        newBlock = client_instance.mine(
            sender=ChainMan,
            recipent=user.address,
            amount=10
        )
        if client_instance.update(newBlock):
            print("update success")

        else:
            print("update failed")

    elif op == "4":
        break


