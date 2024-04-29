# 编写代码，向127.0.0.1:8000发送一个get请求

import requests
import pickle
from Protocol import GCBPProtocol


class client(GCBPProtocol):
    def __init__(self):
        super().__init__()

    def get(self):
        """
        向服务器发送get请求
        :return:
        """
        response = requests.get('http://' + str(self.host) + ":" + str(self.port))
        return self.load(response.content)

    def post(self, data):
        dump_data = self.dump(data)
        response = requests.post('http://' + str(self.host) + ":" + str(self.port), data=dump_data)
        return self.load(response.content)


if __name__ == '__main__':
    c = client()
    print(c.get())
    print(c.post("hello"))