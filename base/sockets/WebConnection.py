from LogModule import Log
import pickle


class webConnection(Log):
    def __init__(self):
        super().__init__()
        self.msg_per_length = 64
        self.buffsize = 1024
        self.backlog = 5
        self.encoding = 'utf-8'

    @staticmethod
    def dump(info):
        """
        将输入的各种元素转化为可发送的字节码
        """
        info_bytes = pickle.dumps(info)
        return info_bytes


    def send(self, msg, socket_):
        """
        向已经建立的套接字发送消息
        :param msg: 消息的原数据，无需封装
        :param socket_: 已经建立的套接字
        :return:
        """
        # 将消息转换为字节
        msg_bytes = self.dump(msg)

        # 获取消息的长度
        msg_length = len(msg_bytes)

        # 将消息长度转换为字节，并补全到self.msg_per_length位
        send_length = str(msg_length).encode(self.encoding)

        send_length += b' ' * (self.msg_per_length - len(send_length))

        # 先发送消息长度
        socket_.send(send_length)

        # 再发送消息字节
        socket_.sendall(msg_bytes)

    def receive(self, socket_):
        """
        从已经建立的套接字中接受信息
        :param socket_: 已经建立的套接字
        :return msg: 得到的信息
        """
        # 接受消息长度
        get_length = socket_.recv(self.msg_per_length)
        if len(get_length) == 0:
            return None
        # 将消息长度转换为整数
        msg_length = int(get_length.decode(self.encoding))
        print(self.log(f'msg_length: {msg_length}'))

        # 接受消息
        msg_bytes = socket_.recv(msg_length)

        # 将消息转换为原数据
        msg = pickle.loads(msg_bytes)

        return msg
