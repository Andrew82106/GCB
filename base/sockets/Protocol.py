import time


class GCBPProtocol:
    """
    GCBPProtocol类用于定义GCB服务器之间交换信息的协议格式

    Attributes:
        protocol_format (dict): 协议格式字典，包含以下键值对：
        - 'msgType' (int): 消息类型，1表示请求，2表示更改链信息
        - 'msgLength' (int): 消息长度
        - 'msgContent' (str): 消息内容

    Methods:
        GCBmsg(msg, msgType): 生成符合GCB协议格式的消息
    """
    def __init__(self):
        self.protocol_format = {
            'msgType': 0,
            'msgLength': 0,
            'msgContent': None,
            'timeStamp': time.time_ns()
        }


    def GCBmsg(self, msg, msgType):
        self.protocol_format['msgContent'] = msg
        self.protocol_format['msgLength'] = len(msg)
        self.protocol_format['msgType'] = msgType

        assert self.protocol_format['msgType'] in [1, 2], "msgType must be 1 or 2"
        return self.protocol_format
