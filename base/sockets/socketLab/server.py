from socket import socket, AF_INET, SOCK_STREAM


# 定义一个函数echo_handler，用于处理客户端的连接
def echo_handler(address, client_sock):
    print('Got connection from {}'.format(address))
    while True:
        # 接收客户端发送的数据
        msg = client_sock.recv(8192)
        if not msg:
            # 如果接收到的数据为空，则退出循环
            break
        # 将接收到的数据原样发送给客户端
        print(type(msg))
        print(str(msg))
        client_sock.sendall(bytes("for query {" + msg.decode('utf-8') + "}:query result", 'utf-8'))

    # 关闭客户端连接
    client_sock.close()


# 定义一个函数echo_server，用于创建一个TCP服务器
def echo_server(address, backlog=5):
    # 创建一个socket对象
    sock = socket(AF_INET, SOCK_STREAM)
    # 绑定地址
    sock.bind(address)
    # 监听连接
    sock.listen(backlog)
    while True:
        # 接受客户端连接
        client_sock, client_addr = sock.accept()
        # 调用echo_handler处理客户端连接
        echo_handler(client_addr, client_sock)


# 如果直接运行该文件，则启动一个TCP服务器，监听20000端口
if __name__ == '__main__':
    # 这是一个多线程的服务器了
    echo_server(('', 20002))
