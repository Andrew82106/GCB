# 基于RSA生成一对公私钥
import rsa


def generate_key_pair():
    (public_key, private_key) = rsa.newkeys(512)
    return public_key, private_key


def encode(content, private_key):
    return rsa.encrypt(content, private_key)


def decode(content, public_key):
    return rsa.decrypt(content, public_key)


if __name__ == '__main__':
    print(generate_key_pair())
    print(generate_key_pair())
    print(generate_key_pair())
    print(generate_key_pair())