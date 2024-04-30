import socket
import random


class client:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8848
        self.ADDR = (self.host, self.port)
        self.buffsize = 1024
        self.max_listen = 5
        self.encoding = 'utf-8'

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.ADDR)
            print('connected')
            cnt = 1
            while cnt < 10:
                data = str(random.randint(1, 100))
                s.send(data.encode(self.encoding))
                recv_data = s.recv(self.buffsize)
                print(recv_data)
                cnt += 1
            s.close()
            print("disconnected")


if __name__ == '__main__':
    c = client()
    c.start()