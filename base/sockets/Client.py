import socket
import time

from LogModule import Log
from Protocol import GCBPProtocol
from WebConnection import webConnection


class client(webConnection, GCBPProtocol):
    """
    client类用于实现一个基于socket的客户端

    Attributes:
        host (str): 服务器地址
        port (int): 服务器端口
        ADDR (tuple): 服务器地址和端口的元组
        buffsize (int): 缓冲区大小
        backlog (int): 等待连接队列的最大长度
        encoding (str): 编码方式

    Methods:

    Example:
        c = client()
        c.send(["Good Morning", 123]*10)
    """
    def __init__(self, host='localhost', port=8848, buffsize=1024, backlog=5, encoding='utf-8'):
        webConnection.__init__(self)
        GCBPProtocol.__init__(self)
        self.host = host
        self.port = port
        self.ADDR = (self.host, self.port)
        self.buffsize = buffsize
        self.backlog = backlog
        self.encoding = encoding

    def request(self, request_msg):
        """
        发送请求给服务器

        Args:
            request_msg (str or list): 请求消息

        Returns:
            response (str or list): 服务器响应消息
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # 绑定地址
            sock.connect(self.ADDR)
            self.send(request_msg, sock)
            result = self.receive(sock)
            return result


if __name__ == '__main__':
    c = client()
    for _ in range(100):
        time.sleep(0.5)
        res = c.request(["Good Morning", 123111]*10000)
        print(res)