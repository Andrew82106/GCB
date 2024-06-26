import random
from GCBChainStructure import *
from User import *
from Miner import *

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
minerAddress = userPool.addNewUser()
print("Miner Address:", minerAddress)

# 创建交易
t0 = Transaction(GodAddress, evalAddress, 0, time.time_ns())

# 挖矿
m = Miner(minerAddress)
nonce, newBlock = m.mine(GCBChain.fetchLatestBlock().data.MTreeLst, GCBChain.fetchLatestBlock().block_hash, t0)

if GCBChain.createNewBlock(newBlock):
    print("validate Mining result")
else:
    print("invalidate Mining result")


# 输出链信息进行调试
GCBChain.debugOutputChain()
print("end")