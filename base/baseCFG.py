import os
import sys


# 定义一个PathCFG类
class PathCFG:
    """
    PathCFG类用于设置项目的路径。

    Attributes:
        projectName (str): 项目名称。
        rootPth (str): 项目根路径。
        basePath (str): 项目基础路径。
        wheelsPath (str): 项目轮子路径。
        utilsPath (str): 项目工具路径。

    Methods:
        _add_sys_pth(): 将项目的相关路径都加入sys.path中。

    Example:
        C = PathCFG()

        print(C.projectName)  # 输出：GCB
    """
    # 初始化函数
    def __init__(self):
        # 设置项目名称
        self.projectName = 'GCB'
        # 设置根路径
        self.rootPth = None
        # 获取当前路径
        current_path = os.getcwd()
        # 循环查找项目根路径
        while True:
            # 如果当前路径下存在项目名称的文件夹，则设置根路径
            if os.path.exists(os.path.join(current_path, self.projectName)):
                self.rootPth = os.path.join(current_path, self.projectName)
                break
            # 获取上一级路径
            parent_path = os.path.dirname(current_path)
            # 如果当前路径等于上一级路径，则退出循环
            if current_path == parent_path:
                break
            # 更新当前路径
            current_path = parent_path
        # 如果找到根路径，则打印
        if self.rootPth:
            print(f"Project root path found: {self.rootPth}")
        # 如果没有找到根路径，则抛出异常
        else:
            raise Exception("Unable to find the project root path.")

        # 一级路径
        self.basePath = os.path.join(self.rootPth, "base")
        self.wheelsPath = os.path.join(self.rootPth, "Wheels")

        # 二级路径
        self.utilsPath = os.path.join(self.basePath, "utils")

        # 区块链默认缓存路径
        self.blockchain_cache_path = os.path.join(self.basePath, "blockchain_cache")

        # 添加系统路径
        self._add_sys_pth()


    def _add_sys_pth(self):
        # 将项目的相关路径都加入sys.path中
        sys.path.append(self.rootPth)
        sys.path.append(self.basePath)
        sys.path.append(self.wheelsPath)
        sys.path.append(self.utilsPath)
        # 将sys.path中的路径依次打印出来
        print("current system path cache:\n" + '*'*40)
        for pth in sys.path:
            print(">" + str(pth))
        print('*'*40)


if __name__ == '__main__':
    C = PathCFG()