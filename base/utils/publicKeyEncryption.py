# 编写一个RSA加密解密函数
import rsa
import pickle


def rsa_encrypt(message, public_key):
    # 加密
    encrypted_message = rsa.encrypt(message, public_key)
    return encrypted_message


def rsa_decrypt(encrypted_message, private_key):
    # 解密
    decrypted_message = rsa.decrypt(encrypted_message, private_key)
    return decrypted_message


def generate_key_pair():
    return rsa.newkeys(512)


class pubEnc:
    """
        Public Key Encryption class用于实现非对称加密和解密数据。
        Attributes:
            encryptFunc: 加密函数
            decryptFunc: 解密函数
            generateKey: 生成密钥对函数

        Methods:
            encrypt(message, public_key): 加密消息
            decrypt(encrypted_message, private_key): 解密消息

        """
    def __init__(self):
        self.encryptFunc = rsa_encrypt
        self.decryptFunc = rsa_decrypt
        self.generateKey = generate_key_pair

    def encrypt(self, message, public_key):
        # 将message对象使用pickle库转化为byte
        message_bytes = pickle.dumps(message)
        return self.encryptFunc(message_bytes, public_key)

    def decrypt(self, encrypted_message, private_key):
        assert isinstance(encrypted_message, bytes), "Encrypted message must be bytes"
        res = self.decryptFunc(encrypted_message, private_key)
        # 将res使用pickle转化
        return pickle.loads(res)


if __name__ == '__main__':
    # 创建加密解密对象
    enc = pubEnc()

    # 生成密钥对
    (pubkey, privkey) = enc.generateKey()

    # 待加密的消息
    message = ['Hello, World!']

    # 加密
    encrypted_message = enc.encrypt(message, pubkey)
    print(f'Encrypted message: {encrypted_message}')

    # 解密
    decrypted_message = enc.decrypt(encrypted_message, privkey)
    print(f'Decrypted message: {decrypted_message}')

    assert decrypted_message == message
    print('Successfully decrypted!')
