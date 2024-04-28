# socket接口封装

> 可用参考文献：[python cookbook](https://python3-cookbook.readthedocs.io/zh-cn/latest/chapters/p11_network_and_web_program.html)

## 要实现的功能

- 广播服务器：接受多个输入，发送多个输出=接受多个客户端的查询和修改请求，发送最新的链结果
- 挖矿服务器：发送单个输出，接受单个输入=每隔一段时间发送一个查询请求，更新链结果；挖出来块后发送修改请求，请求更新链结果
- 钱包服务器：发送单个输出，接受单个输入=发送查询请求，进行余额查询

> socketLab文件夹中存放部分测试代码