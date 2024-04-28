from utils.hashTools import *
from typing import List

hashTool = hashTool()


class Transaction:
    """
    Transaction类用于表示交易

    Attributes:
        sender (str): 发送方地址
        recipient (str): 接收方地址
        amount (float): 交易金额
        time_stamp (str): 交易时间戳
        hash (str): 交易哈希值
    """
    def __init__(self, sender, recipient, amount, time_stamp=time.time_ns()):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.time_stamp = time_stamp
        self.hash = hashTool.hashFunc(str(self.sender) + str(self.recipient) + str(self.amount) + str(self.time_stamp))


class MerkleTree:
    """
    MerkleTree类用于表示Merkle Tree

    Attributes:
        type (int): 0表示保存全量交易，1表示保存根节点交易哈希值
        MTreeLst (List[Transaction]): 保存交易信息的列表
        rootHash (str): 根节点哈希值

    Methods:
        _hashMTree: 迭代式哈希MTree中的每个交易
        queryTransaction: 根据交易索引查询交易
        queryTransactionByHash: 根据交易哈希查询交易
        debugOutputChain: 打印MTree中的所有信息
    """
    def __init__(self, TransactionLst: List[Transaction], Type=0):
        self.type = Type
        # type=0则该保存全量交易
        # type=1则该保存根节点交易哈希值
        self.MTreeLst = TransactionLst if Type == 0 else None
        self.rootHash = self._hashMTree(TransactionLst)

    def __add__(self, other):
        if self.type == 0:
            # 如果两个MerkleTree的type都为0，则将它们的MTreeLst合并
            if other.type == 0:
                return MerkleTree(self.MTreeLst + other.MTreeLst, 0)
            # 如果其中一个MerkleTree的type为1，则将另一个MerkleTree的MTreeLst转换为type=0
            else:
                return MerkleTree(self.MTreeLst + [other.rootHash], 0)
        else:
            # 如果两个MerkleTree的type都为1，则将它们的rootHash进行合并
            if other.type == 1:
                return MerkleTree([self.rootHash, other.rootHash], 1)
            # 如果其中一个MerkleTree的type为0，则将另一个MerkleTree的rootHash转换为type=1
            else:
                return MerkleTree([self.rootHash, other.MTreeLst[0].hash], 1)

    def __len__(self):
        return len(self.MTreeLst) if self.type == 0 else 1

    @staticmethod
    def _hashMTree(TransactionLst):
        # 将self.MTree中的每个交易进行迭代式哈希，得到根节点哈希
        lst = [instance.hash for instance in TransactionLst]
        while len(lst) > 1:
            # print(lst)
            lst1 = []
            for index in range(0, len(lst) - 1, 2):
                lst1.append(hashTool.hashFunc(lst[index] + lst[index + 1]))
            if len(lst) % 2:
                lst1.append(lst[-1])
            lst = lst1
        assert len(lst) == 1, 'Merkle Tree哈希错误'
        return lst[0]

    def queryTransaction(self, TransactionIndex):
        if self.type == 1:
            return None
        # 根据交易索引查询交易
        return self.MTreeLst[TransactionIndex]

    def queryTransactionByHash(self, Hash):
        if self.type == 1:
            return None
        # 根据交易哈希查询交易
        for instance in self.MTreeLst:
            if instance.hash == Hash:
                return instance
        return None

    def debugOutputChain(self):
        # 打印MTree中的所有信息
        print("-" * 10, "Merkle Tree Debug Output", "-" * 10)
        for instance in self.MTreeLst:
            print(f"Sender: {instance.sender}, Recipient: {instance.recipient}, Amount: {instance.amount}, Time Stamp: {instance.time_stamp}, Hash: {instance.hash}")

        print("-" * 10, "Merkle Tree Debug Output", "-" * 10)
