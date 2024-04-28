import socket
from LogModule import Log
from Protocol import GCBPProtocol
import pickle


class client(Log, GCBPProtocol):
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
        Log.__init__(self)
        GCBPProtocol.__init__(self)
        self.host = host
        self.port = port
        self.ADDR = (self.host, self.port)
        self.buffsize = buffsize
        self.backlog = backlog
        self.encoding = encoding

    def request(self, request_msg, msgType=1):
        """
        发送请求给服务器

        Args:
            request_msg (str or list): 请求消息
            msgType (int): 消息类型，默认为1

        Returns:
            response (str or list): 服务器响应消息，为标准GCB格式
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # 绑定地址
            sock.connect(self.ADDR)
            self.send(request_msg, sock, msgType)
            res = self.load(sock)
            # sock.close()
            assert self.check_format(res), "Response format error"
            return res


if __name__ == '__main__':
    c = client()