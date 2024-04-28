import time


class Log:
    """
    Log类用于格式化项目中的日志信息。

    Attributes:
        time_format (str): 时间格式，默认为"%Y-%m-%d %H:%M:%S"。

    Methods:
        time_stamp(): 返回当前时间，格式化为time_format。
        log(msg): 返回格式化后的日志信息，包括时间戳和msg。
    """
    def __init__(self):
        self.time_format = "%Y-%m-%d %H:%M:%S"

    def time_stamp(self):
        return time.strftime(self.time_format, time.localtime())

    def log(self, msg):
        return f"[{self.time_stamp()}]: {msg}"