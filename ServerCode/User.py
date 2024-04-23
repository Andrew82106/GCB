import random
from Utils.hashTools import *
from typing import List
hashTool = hashTool()


class User:
    def __init__(self, address_):
        self.address = address_


class UserPool:
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