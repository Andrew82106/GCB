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