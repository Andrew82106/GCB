from base.pathconfig import Pathconfig

cfg = Pathconfig()

from base.webconnnection.server import server
from base.GCBChainStructure import Chain, Block, loadChain
import socket
from sanic import Sanic, raw
import pickle

debug_chain = loadChain()
if not debug_chain:
    debug_chain = Chain('000000000')


class boardcastServer:
    """
    boardcastServer类用于实现广播服务器中的数据存储部分，网络接口部分由b_server类负责

    Attributes:
        IP_list (list): 用于存储所有客户端的IP地址
        chain (Chain): 用于存储区块链

    Methods:
        _update_IP_list(ip): 更新IP_list列表
        update_chain(newBlock: Block): 更新区块链

    """
    def __init__(self, chain: Chain):
        self.IP_list = []
        self.chain = chain

    def _update_IP_list(self, ip):
        if ip not in self.IP_list:
            self.IP_list.append(ip)

    def update_chain(self, newBlock: Block):
        res = self.chain.createNewBlock(newBlock)
        self.chain.chainLocalSaver()
        return res


class b_server(server):
    """
    b_server类用于实现广播服务器中的网络接口部分，数据存储部分由boardcastServer类负责

    Attributes:
        chainOperator (boardcastServer): 用于存储区块链和客户端IP地址的类

    Methods:
        __init__(self): 初始化b_server类
        get(self, request): 处理客户端的GET请求
        post(self, request): 处理客户端的POST请求

    """
    def __init__(self):
        super().__init__()
        self.chainOperator = boardcastServer(debug_chain)

    async def get(self, request):
        """
        客户端向服务器发送更新请求，服务器流式发送更新数据
        这里的客户端只需要发送一个空的request请求即可
        服务端会将整条链发送给客户端
        :param request: sanic请求变量
        :return: None（由于是流式传输，因此不用返回值这种方式回传数据）
        """
        response = await request.respond(content_type="text/text")

        # 将data转化为字节码，使用pickle
        data = self.dump(self.GCBmsg(self.chainOperator.chain, 1))

        await response.send(data)
        await response.eof()

    async def post(self, request):
        """
        客户端发送更新链的请求
        服务器检查是否能更新链
        如果能则更新链，如果不能则拒绝更新链
        并返回相应信息
        返回值是字节码
        :param request: sanic请求变量
        :return: 新块添加情况
        """
        cont = request.body
        # 将字节码转化为data
        data = self.load(cont)
        # print(data_)
        block = self.extract_msg(data)
        if self.chainOperator.update_chain(block):
            send_back = self.GCBmsg('new block accepted', 0)
        else:
            send_back = self.GCBmsg('new block rejected', 0)
        return raw(self.dump(send_back))


app = Sanic("GCBBoardCastServer")
app.add_route(b_server.as_view(), "/")