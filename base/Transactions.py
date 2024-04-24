from utils.hashTools import *
from typing import List
hashTool = hashTool()


class Transaction:
    def __init__(self, sender, recipient, amount, time_stamp):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.time_stamp = time_stamp
        self.hash = hashTool.hashFunc(str(self.sender) + str(self.recipient) + str(self.amount) + str(self.time_stamp))


class MerkleTree:
    def __init__(self, TransactionLst: List[Transaction], Type=0):
        self.type = Type
        # type=0则该保存全量交易
        # type=1则该保存根节点交易哈希值
        self.MTreeLst = TransactionLst if Type == 0 else None
        self.rootHash = self._hashMTree(TransactionLst)

    @staticmethod
    def _hashMTree(TransactionLst):
        # 将self.MTree中的每个交易进行迭代式哈希，得到根节点哈希
        lst = [instance.hash for instance in TransactionLst]
        while len(lst) > 1:
            # print(lst)
            lst1 = []
            for index in range(0, len(lst)-1, 2):
                lst1.append(hashTool.hashFunc(lst[index] + lst[index + 1]))
            if len(lst) % 2:
                lst1.append(lst[-1])
            lst = lst1
        assert len(lst) == 1, 'Merkle Tree哈希错误'
        return lst[0]