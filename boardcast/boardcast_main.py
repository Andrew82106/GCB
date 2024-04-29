from base.pathconfig import Pathconfig

cfg = Pathconfig()

from base.sockets.Server import server
from base.GCBChainStructure import Chain, Block
import socket


class boardcastServer(server):
    """
    boardcastServer用于实现广播站服务器功能，即：
    1. 存放最新链
    2. 向各个请求更新链信息的客户端发送最新链
    3. 接受挖矿服务器更新最新链的请求并且广播最新链


    Attributes:
        boardcast_socket (socket): 广播站服务器的socket
        IP_list (list): 存放当前网络中所有已知客户端的IP地址

    Methods:
        _update_IP_list(ip): 更新IP_list

    """
    def __init__(self, chain: Chain):
        super().__init__()
        self.boardcast_socket = None
        self.IP_list = []
        self.chain = chain

    def _update_IP_list(self, ip):
        if ip not in self.IP_list:
            self.IP_list.append(ip)

    def update_chain(self, newBlock: Block):
        return self.chain.createNewBlock(newBlock)

    def handle(self, address, client_sock):
        """
        这个函数重写的目的在于实现广播服务器的具体功能

        具体而言，收到信息后，该服务器首先需要识别接收到的信息是什么类型的

        对于请求查询类的信息，该服务器需要将本地的链直接发送给对方

        对于请求更新链的信息，该服务器需要将本地的链更新，并且广播给所有已知客户端

        """
        print(self.log('Handle connection from {}'.format(address)))
        while True:
            # 接收客户端发送的数据
            msg = self.load(client_sock)
            print(self.log(("Recieve Info:" + str(msg)[:10] + "....")))
            if msg is None:
                # TODO: 这里改的有点问题，当没有消息来的时候应该怎么办
                print(self.log("Recieve None, maybe client close"))
                break

            msg_type = self.extract_msg_type(msg)
            if msg_type == 1:
                print(self.log(f"send chain to client {address}"))
                self.send(self.chain, client_sock, 0)
            elif msg_type == 2:
                newBlock = self.extract_msg(msg)
                status = self.update_chain(newBlock)
                print(self.log(f"update chain from client {address}"))
                if status:
                    print(self.log("update block successfully"))
                    self.send('update block successfully', client_sock, 0)
                else:
                    print(self.log("update block failed"))
                    self.send('update block failed', client_sock, 0)

        # 关闭客户端连接
        client_sock.close()


if __name__ == '__main__':
    debug_chain = Chain('000000000')
    boardcast_server = boardcastServer(debug_chain)
    boardcast_server.start()


