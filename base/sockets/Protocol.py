import time
import pickle


class GCBPProtocol:
    """
    GCBPProtocol类用于定义GCB服务器之间交换信息的协议格式

    Attributes:
        protocol_format_ (dict): 协议格式字典，包含以下键值对：
        - 'msgType' (int): 消息类型，0表示返回结果，1表示请求，2表示更改链信息
        - 'msgLength' (int): 消息长度
        - 'msgContent' (str): 消息内容
        - 'timeStamp' (int): 时间戳，以纳秒为单位

        msg_per_length (int): TCP发送消息时每条消息的单位长度限制

    Methods:
        GCBmsg(msg, msgType): 生成符合GCB协议格式的消息
        dump(info): 将输入的各种元素转化为可发送的字节码
        send(msg, socket_): 发送信息，按照规定的大小发送数据段，同时在发送数据段之前先发送数据的数量
        load(socket_): 调用套接字，将接收到的字节码转化为各种元素
        extract_msg(msg): 提取消息内容
        extract_msg_type(msg): 提取消息类型
        extract_msg_length(msg): 提取消息长度
        extract_time_stamp(msg): 提取时间戳
        check_format(GCBmsg): 检查输入值GCBmsg是否符合GCB格式

    """

    def __init__(self):
        self.protocol_format_ = {
            'msgType': 0,
            'msgLength': 0,
            'msgContent': None,
            'timeStamp': time.time_ns()
        }
        self.msg_per_length = 64
        self.buffsize = 1024
        self.backlog = 5
        self.encoding = 'utf-8'

    def GCBmsg(self, msg, msgType):
        """
        生成符合GCB协议格式的消息

        Args:
            msg (str): 消息内容
            msgType (int): 消息类型，0表示返回结果，1表示请求，2表示更改链信息

        Returns:
            dict: 符合GCB协议格式的消息字典
        """
        protocol_format = self.protocol_format_.copy()
        protocol_format['msgContent'] = msg
        protocol_format['msgLength'] = len(msg)
        protocol_format['msgType'] = msgType

        assert protocol_format['msgType'] in [0, 1, 2], "msgType must be 0 or 1 or 2"
        return protocol_format

    @staticmethod
    def dump(info):
        """
        将输入的各种元素转化为可发送的字节码
        """
        info_bytes = pickle.dumps(info)
        return info_bytes

    def send(self, msg, socket_, msgType=1):
        """
        发送信息，按照规定的大小发送数据段，同时在发送数据段之前先发送数据的数量
        该函数中加入了GCB协议规范的封装，因此在调用该函数的时候无需封装
        在外部调用的时候不能忘了关闭套接字
        """
        msg = self.dump(self.GCBmsg(msg, msgType))
        data_length = len(msg)

        # 发送数据长度
        socket_.sendall(self.dump(data_length))

        # 发送数据
        socket_.sendall(msg)

    def load(self, socket_):
        """
        调用套接字，将接收到的字节码转化为各种元素
        该函数中加入了GCB协议规范的封装，因此在调用该函数的时候无需封装
        该函数的返回值符合GCB协议格式
        """

        # 接收数据长度
        data_length = socket_.recv(10)
        if not data_length:
            return None
        data_length = pickle.loads(data_length)
        print(data_length)
        assert isinstance(data_length, int), 'data_length is not a number'

        data = []
        # 根据数据长度，接收数据
        while data_length > 0:
            if data_length > self.buffsize:
                temp = socket_.recv(self.buffsize)
            else:
                temp = socket_.recv(data_length)
            data.append(temp)
            data_length -= len(temp)

        # 将接收到的数据转化为字符串
        msg = b"".join(data)
        # 防止缓冲区太小将数据截断

        # 返回转化后的数据
        result = pickle.loads(msg, encoding=self.encoding)
        assert self.check_format(result), 'The format of the received data is incorrect'
        return result

    @staticmethod
    def extract_msg(msg):
        # 提取消息内容
        return msg['msgContent']

    @staticmethod
    def extract_msg_type(msg):
        # 提取消息类型
        return msg['msgType']

    @staticmethod
    def extract_msg_length(msg):
        # 提取消息长度
        return msg['msgLength']

    @staticmethod
    def extract_time_stamp(msg):
        # 提取时间戳
        return msg['timeStamp']

    @staticmethod
    def check_format(GCBmsg):
        # 检查输入值GCBmsg是否符合GCB格式
        return isinstance(GCBmsg, dict) and all(
            key in GCBmsg for key in ('msgType', 'msgLength', 'msgContent', 'timeStamp'))
