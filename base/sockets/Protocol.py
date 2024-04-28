import time


class GCBPProtocol:
    """
    GCBPProtocol类用于定义GCB服务器之间交换信息的协议格式

    Attributes:
        protocol_format (dict): 协议格式字典，包含以下键值对：
        - 'msgType' (int): 消息类型，0表示返回结果，1表示请求，2表示更改链信息
        - 'msgLength' (int): 消息长度
        - 'msgContent' (str): 消息内容

    Methods:
        GCBmsg(msg, msgType): 生成符合GCB协议格式的消息
    """
    def __init__(self):
        self.protocol_format_ = {
            'msgType': 0,
            'msgLength': 0,
            'msgContent': None,
            'timeStamp': time.time_ns()
        }


    def GCBmsg(self, msg, msgType):
        protocol_format = self.protocol_format_.copy()
        protocol_format['msgContent'] = msg
        protocol_format['msgLength'] = len(msg)
        protocol_format['msgType'] = msgType

        assert protocol_format['msgType'] in [0, 1, 2], "msgType must be 0 or 1 or 2"
        return protocol_format

    @staticmethod
    def extract_msg(msg):
        return msg['msgContent']

    @staticmethod
    def extract_msg_type(msg):
        return msg['msgType']

    @staticmethod
    def extract_msg_length(msg):
        return msg['msgLength']

    @staticmethod
    def extract_time_stamp(msg):
        return msg['timeStamp']

    @staticmethod
    def check_format(GCBmsg):
        # 检查输入值GCBmsg是否符合GCB格式
        return isinstance(GCBmsg, dict) and all(key in GCBmsg for key in ('msgType', 'msgLength', 'msgContent', 'timeStamp'))
