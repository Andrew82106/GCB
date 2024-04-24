import random

from GCBChainStructure import *
from User import *

# 创建账号GodAddress
userPool = UserPool()
GodAddress = userPool.addNewUser()

print("God Address:", GodAddress)

# 创建链
GCBChain = Chain(GodAddress)
# 输出链信息进行调试
GCBChain.debugOutputChain()
# 创建其他账号

evalAddress = userPool.addNewUser()
print("Eval Address:", evalAddress)

# 创建交易
t0 = Transaction(GodAddress, evalAddress, 0, time.time_ns())

# 挖矿
while 1:
    nonce = random.randint(1, 1000000)
    MTree = MerkleTree(GCBChain.Blocks[-1].data.MTreeLst + [t0])
    newBlock = Block(MTree, nonce, GCBChain.Blocks[-1].block_hash)
    if newBlock.block_hash[0] == "0":
        print("nonce:", nonce)
        print("new block hash:", newBlock.block_hash)
        if GCBChain.createNewBlock(t0, nonce):
            break
        else:
            print("nonce error")

# 输出链信息进行调试
GCBChain.debugOutputChain()
print("end")