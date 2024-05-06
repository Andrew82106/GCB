# base package

- 定义所需的所有基础类和工具
- 以包的形式使用base，将编写的代码放在和base同级的位置则可引用

比如：

```text
- project
|
|- base
|   |- utils
|   |   |- hashTools.py
|   |   |- ...
|   |- pathconfig.py
|   |- ...
|   
|- server.py
|- client.py
|- ...
```

- 引用base中的代码前，先做如下引用以初始化项目路径

```python
from base.pathconfig import Pathconfig
cfg = Pathconfig()
```

# base structure

```text
- base
|
|- utils
|   |- hashTools.py
|   |- keyGenerator.py
|
|- webconnection
|   |- client.py
|   |- server.py
|   |- Protocol.py
|   |- start_server.bash
|
|- GCBChainStructure.py
|- pathconfig.py
|- Transaction.py
|- User.py
|- Miner.py
|- wallet.py
|- readme.md
```

# 项目运行流程

- 广播服务器运行，初始状态添加创世区块，持续运行
- 客户端（挖矿客户端和钱包客户端）运行，首先使用用户名和密码向广播服务器提交登录请求，验证完成后进行交易、查询或者挖矿操作