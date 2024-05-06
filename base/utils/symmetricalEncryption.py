# 实现一个AES加密函数

from AES import AES, generate_key

aes = AES()


def encrypt(key, data):
    aes.add_key(key)
    return aes.encrypt(data)


def decrypt(key, data):
    aes.add_key(key)
    return aes.decrypt(data)


class symEnc:
    """
    Symmetrical Encryption class 用于实现对称加密和解密

    Attributes:
        generateKey: 生成密钥的函数
        encryptFunc: 加密函数
        decryptFunc: 解密函数

    Methods:
        encrypt(data_): 使用密钥和加密函数加密数据
        decrypt(data_): 使用密钥和解密函数解密数据

    """
    def __init__(self):
        self.generateKey = generate_key
        self.encryptFunc = encrypt
        self.decryptFunc = decrypt

    def encrypt(self, data_, key_):
        return self.encryptFunc(key_, data_)

    def decrypt(self, data_, key_):
        return self.decryptFunc(key_, data_)


if __name__ == '__main__':
    key = generate_key()
    data = [b'Hello, World!']
    symEnc = symEnc()
    encrypted = symEnc.encrypt(data, key)
    decrypted = symEnc.decrypt(encrypted, key)

    print(f'Key: {key}')
    print(f'Original Data: {data}')
    print(f'Encrypted Data: {encrypted}')
    print(f'Decrypted Data: {decrypted}')

    assert data == decrypted, "Decrypted data_ does not match original data_"

    print("Encryption and decryption successful!")