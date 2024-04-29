from Protocol import GCBPProtocol
from sanic.views import HTTPMethodView
from sanic import raw, Sanic
import pickle


class server(GCBPProtocol, HTTPMethodView):
    def __init__(self):
        GCBPProtocol.__init__(self)

    async def get(self, request):
        """
        客户端向服务器发送更新请求，服务器流式发送更新数据
        :param request:
        :param data:
        :return:
        """
        response = await request.respond(content_type="text/text")
        # 将data转化为字节码，使用pickle
        data = self.dump(['data', '1111', '2222'])
        await response.send(data)
        # Optionally, you can explicitly end the stream by calling:
        await response.eof()

    # You can also use async syntax
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
