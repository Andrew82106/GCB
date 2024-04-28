import time
import socket
import threading


# 定义一个函数，用于连接并发送消息
def connect_and_send(i):
    # 创建一个socket对象
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 连接到本地主机，端口为20002
    s.connect(('localhost', 20002))
    # 向服务器发送消息
    s.send(f'Hello!I am client {i}'.encode('utf-8'))
    # 接收服务器返回的消息
    print(f"Thread {i}: {s.recv(8192)}")
    # 关闭socket对象
    s.close()


# 创建一个线程列表
threads = []
# 循环50次，创建50个线程
for i in range(50):
    # 创建一个线程，目标函数为connect_and_send，参数为i
    t = threading.Thread(target=connect_and_send, args=(i,))
    # 将线程添加到线程列表
    threads.append(t)
    # 启动线程
    t.start()
    # 线程休眠0.1秒
    time.sleep(0.1)

# 循环线程列表，等待所有线程结束
for t in threads:
    t.join()
