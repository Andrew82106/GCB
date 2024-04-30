import socket


class server:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8848
        self.ADDR = (self.host, self.port)
        self.buffsize = 1024
        self.max_listen = 5

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.ADDR)
            s.listen(self.max_listen)
            print('Server is running...'+str(self.ADDR[0])+':'+str(self.ADDR[1]))
            while True:
                conn, addr = s.accept()
                print('Connected by', addr)
                with conn:
                    while True:
                        data = conn.recv(self.buffsize)
                        print(f'Received {data}')
                        conn.send(data)
                s.close()


if __name__ == '__main__':
    S = server()
    S.start()