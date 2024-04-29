import socket
from LogModule import Log
from Protocol import GCBPProtocol
from WebConnection import webConnection


class server(webConnection, GCBPProtocol):
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
        webConnection.__init__(self)
        GCBPProtocol.__init__(self)
        self.host = host
        self.port = port
        self.ADDR = (self.host, self.port)
        self.buffsize = buffsize
        self.backlog = backlog
        self.encoding = encoding

    def handle(self, address, client_sock):
        """
        处理特定客户端连接
        这里的代码只是样例，在具体的类中该函数被重载，使用不同的写法进行重写
        """
        print('Got connection from {}'.format(address))
        while True:
            # 接收客户端发送的数据
            msg = self.receive(client_sock)
            if not msg:
                # 如果接收到的数据为空，则退出循环
                break
            print(self.log(("Recieve Info:" + str(msg))))
            self.send('query result: 1134522', client_sock)

        # 关闭客户端连接
        client_sock.close()

    def start(self):
        """
        启动服务器，开始接受信息
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # 绑定地址
            sock.bind(self.ADDR)
            print(self.log('Bound to {}'.format(self.ADDR)))
            print(self.log('Server started.Listening...'))
            # 监听连接
            sock.listen(self.backlog)
            while True:
                # 接受客户端连接
                client_sock, client_addr = sock.accept()
                print(self.log(("Accepted connection from {}".format(client_addr))))
                # 调用echo_handler处理客户端连接
                self.handle(client_addr, client_sock)
                print(self.log('handle message successfully'))


if __name__ == '__main__':
    S = server()
    S.start()