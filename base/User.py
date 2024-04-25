import random
from utils.hashTools import *
from typing import List
hashTool = hashTool()


class User:
    """
    User类用于表示用户，包括用户的地址信息。

    Attributes:
        address (str): 用户的地址信息。
    """
    def __init__(self, address_):
        self.address = address_


class UserPool:
    """
    UserPool类用于管理用户池，包括添加新用户、验证用户身份等操作。

    Attributes:
        userPool (list): 用户池，存储所有用户的信息。

    Methods:
        _addUser(address_): 添加新用户到用户池中。
        addNewUser(): 添加新用户到用户池中，并返回新用户的地址。
    """
    def __init__(self):
        self.userPool = []
        # 添加类型提示
        self.userPool: list[User]

    def _addUser(self, address_):
        if address_ in [user.address for user in self.userPool]:
            return False
        self.userPool.append(User(address_))
        return True

    def addNewUser(self):
        # 添加用户
        print("Adding new user...")
        maxRandomCnt = 0
        while 1:
            maxRandomCnt += 1
            address_ = hashTool.hashFunc(random.randint(0, 2 ** 256 - 1))
            if self._addUser(address_):
                break
            if maxRandomCnt > 1000000:
                print("Failed to add new user.")
                return False
        return address_


# 测试
if __name__ == "__main__":
    userPool = UserPool()
    address = userPool.addNewUser()
    print(address)