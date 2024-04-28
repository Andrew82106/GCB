import socket
from time import ctime
import json
import time

HOST = ''
PORT = 9001
ADDR = (HOST, PORT)
BUFFSIZE = 1024
MAX_LISTEN = 5


def tcpServer():
    # TCP服务
    # with socket.socket() as s:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 绑定服务器地址和端口
        s.bind(ADDR)
        # 启动服务监听
        s.listen(MAX_LISTEN)
        print('等待用户接入。。。。。。。。。。。。')
        while True:
            # 等待客户端连接请求,获取connSock
            conn, addr = s.accept()
            print('警告，远端客户:{} 接入系统！！！'.format(addr))
            with conn:
                while True:
                    print('接收请求信息。。。。。')
                    # 接收请求信息
                    data = conn.recv(BUFFSIZE)
                    print('data=%s' % data)
                    print('接收数据：{!r}'.format(data.decode('utf-8')))

                    # 发送请求数据
                    conn.send(str(data).encode('utf-8'))
                    print('发送返回完毕！！！')
            s.close()


# 创建UDP服务
def udpServer():
    # 创建UPD服务端套接字
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # 绑定地址和端口
        s.bind(ADDR)
        # 等待接收信息
        while True:
            print('UDP服务启动，准备接收数据。。。')
            # 接收数据和客户端请求地址
            data, address = s.recvfrom(BUFFSIZE)

            if not data:
                break

            print('接收请求信息：{}'.format(data.decode('utf-8')))

            s.sendto(b'i am udp,i got it', address)

        s.close()


if __name__ == '__main__':

    while True:
        choice = 't'

        if choice != 't' and choice != 'u':
            print('please input t or u,ok?')
            continue

        if choice == 't':
            print('execute tcpsever')
            tcpServer()
        else:
            print('execute udpsever')
            udpServer()
