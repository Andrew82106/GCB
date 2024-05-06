from base.pathconfig import Pathconfig

cfg = Pathconfig()

from base.webconnnection.client import client
from base.GCBChainStructure import Chain
from base.User import UserPool

userPool = UserPool()


class wallet_client(client):
    """
    模拟一个客户端代码（只查询）
    """
    def __init__(self, address):
        super().__init__()
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



if __name__ == '__main__':
    pass
