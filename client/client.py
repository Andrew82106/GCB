from base.pathconfig import Pathconfig

cfg = Pathconfig()

from base.webconnnection.client import client
from base.GCBChainStructure import Chain
from base.User import UserPool, User

userPool = UserPool()
userPool.load_userpool_from_pkl()


class wallet_client(client):
    """
    模拟一个客户端代码（只查询）
    """
    def __init__(self, _address):
        super().__init__()
        self.address = _address

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
        assets_ = chain_.calculateAssets(self.address)
        return assets_


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
client_instance = wallet_client(address)
# 开始处理循环
while 1:
    op = input("1. query\n2. queryAssets\n3. exit\n")
    if op == "1":
        chain = client_instance.query()
        chain.debugOutputChain()
    elif op == "2":
        assets = client_instance.queryAssets()
        print(f"assets: {assets}")
    elif op == "3":
        break