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
        GCBmsg(msg, msgType): 生成符合GCB协议格式的消息=
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
        self.port = 8000
        self.host = '127.0.0.1'

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
    def dump(data):
        return pickle.dumps(data)

    def load(self, data):
        return pickle.loads(data, encoding=self.encoding)


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
