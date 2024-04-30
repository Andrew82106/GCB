from utils.keyGenerator import generate_key_pair, encode, decode


class Wallet:
    """
    Wallet类用于存储用户的钱包信息，包括地址、公钥、私钥和编码/解码函数。

    Attributes:
        address (str): 钱包地址。
        public_key (str): 钱包的公钥。
        _private_key (str): 钱包的私钥。
        encode_func (function): 编码函数。
        decode_func (function): 解码函数。

    Methods:
        __init__(self, address): 初始化钱包对象。
    """
    def __init__(self, address):
        self.address = address
        self.public_key, self._private_key = generate_key_pair()
        self.encode_func = encode
        self.decode_func = decode