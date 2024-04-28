import socket
from LogModule import Log
import pickle


class server(Log):
    """
    server类用于实现一个基于socket的服务器

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
        handle(address, client_sock): 处理客户端连接
        start(): 启动服务器

    Example:
        S = server()
        S.start()
    """
    def __init__(self, host='localhost', port=8848, buffsize=1024, backlog=5, encoding='utf-8'):
        super().__init__()
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

    def handle(self, address, client_sock):
        """
        处理客户端连接
        """
        print('Got connection from {}'.format(address))
        while True:
            # 接收客户端发送的数据
            msg = client_sock.recv(self.buffsize)
            if not msg:
                # 如果接收到的数据为空，则退出循环
                break
            msg = self.load(msg)
            print(self.log(("Recieve Info:" + str(msg))))
            client_sock.sendall(self.dump('query result: 1134522'))

        # 关闭客户端连接
        client_sock.close()

    def start(self):
        """
        启动服务器
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # 绑定地址
            sock.bind(self.ADDR)
            print('Bound to {}'.format(self.ADDR))
            print('Server started.Listening...')
            # 监听连接
            sock.listen(self.backlog)
            while True:
                # 接受客户端连接
                client_sock, client_addr = sock.accept()
                # 调用echo_handler处理客户端连接
                self.handle(client_addr, client_sock)


if __name__ == '__main__':
    S = server()
    S.start()