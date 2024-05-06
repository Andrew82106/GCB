import random
from utils.hashTools import *
from utils.publicKeyEncryption import pubEnc
from utils.symmetricalEncryption import symEnc
from wallet import *
import pickle

hashTool = hashTool()
pubEnc = pubEnc()
symEnc = symEnc()


class User:
    """
    User类用于表示用户，包括用户的地址信息。

    Attributes:
        address (str): 用户的地址信息。
        wallet (Wallet): 用户的钱包，用于管理用户的交易。
    """
    def __init__(self, address_, username, password):
        self.address = address_
        self.username = username
        self.wallet = Wallet(address_)
        (self.publicKey, self._privateKey) = pubEnc.generateKey()
        self.key = pubEnc.encrypt(symEnc.generateKey(), self.publicKey)
        self.password = symEnc.encrypt(password, pubEnc.decryptFunc(self.key, self._privateKey))

    def authentication(self, password):
        """
        验证用户身份。

        Args:
            password (str): 用户输入的密码。

        Returns:
            bool: 验证结果，True表示验证成功，False表示验证失败。
        """
        return self.password == symEnc.encrypt(password, pubEnc.decryptFunc(self.key, self._privateKey))

    def changePassword(self, oldPassword, newPassword):
        """
        修改用户密码。

        Args:
            oldPassword (str): 用户输入的旧密码。
            newPassword (str): 用户输入的新密码。

        Returns:
            bool: 修改结果，True表示修改成功，False表示修改失败。
        """
        if self.authentication(oldPassword):
            self.password = symEnc.encrypt(newPassword, pubEnc.decryptFunc(self.key, self._privateKey))
            return True
        return False



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

    def load_userpool_from_pkl(self, poolPath):
        # 从pkl文件中加载用户池
        with open(poolPath, 'rb') as f:
            self.userPool = pickle.load(f)

    def save_userpool_to_pkl(self, poolPath):
        # 将用户池保存到pkl文件中
        with open(poolPath, 'wb') as f:
            pickle.dump(self.userPool, f)

    def _addUser(self, address_, username, password):
        if address_ in [user.address for user in self.userPool]:
            return False
        self.userPool.append(User(address_, username, password))
        return True

    def addNewUser(self, username, password=111111):
        # 添加用户
        print("Adding new user...")
        maxRandomCnt = 0
        if username in [user.username for user in self.userPool]:
            print("Username already exists.")
            return False
        while 1:
            maxRandomCnt += 1
            address_ = hashTool.hashFunc(random.randint(0, 2 ** 256 - 1))
            if self._addUser(address_, username, password):
                break
            if maxRandomCnt > 1000000:
                print("Failed to add new user.")
                return False
        return address_

    def login(self, username, password):
        # 登录
        for user in self.userPool:
            if user.username == username and user.authentication(password):
                return user
        return False


# 测试
if __name__ == "__main__":
    userPool = UserPool()
    address = userPool.addNewUser('GCBGod')
    print(address)