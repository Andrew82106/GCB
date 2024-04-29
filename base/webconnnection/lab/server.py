from sanic import Sanic, raw
from sanic.views import HTTPMethodView
import pickle
from sanic import Request, Websocket

app = Sanic("MyHelloWorldApp")


class TView(HTTPMethodView):

    async def get(self, request):
        response = await request.respond(content_type="text/text")
        data = ["foo," * 2, "bar", "baz"]
        # 将data转化为字节码，使用pickle
        data = pickle.dumps(data)
        await response.send(data)
        # Optionally, you can explicitly end the stream by calling:
        await response.eof()

    # You can also use async syntax
    async def post(self, request):
        cont = request.body
        # 将字节码转化为data
        print(type(cont))
        print(cont)
        data = pickle.loads(cont)
        print(data)

        send_back = "I am post method"
        send_back = pickle.dumps(send_back)
        return raw(send_back)


app.add_route(TView.as_view(), "/")