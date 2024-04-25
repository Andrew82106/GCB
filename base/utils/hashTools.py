# 封装一个函数，使用sha256加密对象
import hashlib
import time


def sha256_hash(obj):
    # 使用sha256函数计算obj哈希值
    hash_object = hashlib.sha256(str(obj).encode('utf-8'))
    return hash_object.hexdigest()


class hashTool:
    """
    hashTool类用于封装sha256哈希函数，并提供一些辅助功能。

    Attributes:
        hashLength (int): 哈希值的长度，默认为64。
        hashFunc (function): 哈希函数，默认为sha256_hash。

    Methods:
        hash(obj): 计算obj的哈希值。
        hash_dev(obj): 计算obj的哈希值，并返回计算时间。

    Example:
        hashTool = hashTool()
        print(hashTool.hash("Hello, World!"))
    """
    def __init__(self):
        self.hashLength = 64
        self.hashFunc = sha256_hash  # hashFunc和hashLength要对应

    def hash(self, obj):
        return self.hashFunc(obj)

    def hash_dev(self, obj):
        # 使用time模型计算hash计算时间(秒）
        t0 = time.time_ns()
        hash_object = self.hashFunc(obj)
        t1 = time.time_ns()

        return hash_object, (t1 - t0)/1e9




if __name__ == '__main__':
    # 测试
    HashTool = hashTool()
    print(HashTool.hash("Hello, World!"), type(HashTool.hash("Hello, World!")), len(HashTool.hash("Hello, World!")))
    print(HashTool.hash_dev("H"*2560000))
    print(HashTool.hash_dev("H"*16))
    print(HashTool.hash_dev("H"*16))
    print(HashTool.hash_dev("H"*16))
    print(HashTool.hash_dev("H"*16))