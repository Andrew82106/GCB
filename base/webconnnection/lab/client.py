# 编写代码，向127.0.0.1:8000发送一个get请求

import requests
import pickle

response = requests.get('http://127.0.0.1:8000')

print(response.text)
# 使用pickle将response的字节码内容进行读取
response_content = pickle.loads(response.content)
print(response_content)

# 编写代码，向127.0.0.1:8000发送一个post请求，发送一段文本

data = {'text': 'Hello, World!'}
# 将data变成字节码
data_bytes = pickle.dumps(data)
response = requests.post('http://127.0.0.1:8000', data=data_bytes)

print(response.text)
# 使用pickle将response的字节码内容进行读取
response_content = pickle.loads(response.content)
print(response_content)