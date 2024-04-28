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
        dump(info): 将输入的各种元素转化为可发送的字节码
        load(info): 将接收到的字节码转化为各种元素
        send(info=f'Hello!I am client'): 发送信息

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

    @staticmethod
    def dump(info):
        """
        将输入的各种元素转化为可发送的字节码
        """
        info_bytes = pickle.dumps(info)
        return info_bytes

    def load(self, info):
        """
        将接收到的字节码转化为各种元素
        """
        return pickle.loads(info, encoding=self.encoding)

    def send(self, info=f'Hello!I am client'):
        """
        发送信息
        """
        print(self.log(f"send msg: {info}"))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.ADDR)
            print('connected')
            info = self.dump(self.GCBmsg(info, 1))
            s.send(info)
            result = self.load(s.recv(self.buffsize))
            result = self.extract_msg(result)
            print(f"recieve msg: {result}")

        print("disconnected")
        return result


if __name__ == '__main__':
    c = client()
    c.send(["Good Morning", 123]*10)