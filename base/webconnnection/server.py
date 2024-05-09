from base.webconnnection.Protocol import GCBPProtocol
from sanic.views import HTTPMethodView
from sanic import raw, Sanic
import pickle


class server(GCBPProtocol, HTTPMethodView):
    def __init__(self, host, port):
        GCBPProtocol.__init__(self, host, port)

    async def get(self, request):
        """
        客户端向服务器发送更新请求，服务器流式发送更新数据

        此处测试数据为['data_', '1111', '2222']
        :param request:
        :param data: 服务器返回的数据
        :return:
        """
        response = await request.respond(content_type="text/text")
        # 将data转化为字节码，使用pickle
        data = self.dump(['data_', '1111', '2222'])
        await response.send(data)
        await response.eof()

    async def post(self, request):
        """
        客户端发送更新请求
        :param request:
        :return:
        """
        cont = request.body
        # 将字节码转化为data
        data = pickle.loads(cont)
        print(data)
        send_back = "I am post method"
        send_back = self.dump(send_back)
        return raw(send_back)


# app = Sanic("MyHelloWorldApp")
# app.add_route(server.as_view(), "/")
