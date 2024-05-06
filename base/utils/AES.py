import numpy as np
import pickle


def generate_key():
    # Generate a random 16-byte key_
    return np.random.bytes(16)


class AES:

    def __init__(self):
        self.key = None

    def add_key(self, key):
        self.key = key

    def encrypt(self, data):
        # Serialize the input data_ using pickle
        serialized_data = pickle.dumps(data)

        # Convert serialized data_ to 16-byte blocks
        blocks = [serialized_data[i:i + 16] for i in range(0, len(serialized_data), 16)]
        encrypted_blocks = []

        for block in blocks:
            if len(block) < 16:
                # Pad the last block if necessary
                block += b'\x00' * (16 - len(block))
            encrypted_block = self._encrypt_block(block)
            encrypted_blocks.append(encrypted_block)

        return b''.join(encrypted_blocks)

    def decrypt(self, ciphertext):
        # Convert ciphertext to 16-byte blocks
        blocks = [ciphertext[i:i + 16] for i in range(0, len(ciphertext), 16)]
        decrypted_blocks = []

        for block in blocks:
            decrypted_block = self._decrypt_block(block)
            decrypted_blocks.append(decrypted_block)

        # Concatenate decrypted blocks and deserialize using pickle
        serialized_data = b''.join(decrypted_blocks)
        return pickle.loads(serialized_data)

    def _encrypt_block(self, block):
        # Simple example: XOR block with key_
        encrypted_block = bytes([b ^ k for b, k in zip(block, self.key)])
        return encrypted_block

    def _decrypt_block(self, block):
        # Simple example: XOR block with key_ (as decryption is the same as encryption)
        decrypted_block = bytes([b ^ k for b, k in zip(block, self.key)])
        return decrypted_block


if __name__ == '__main__':

    # Example usage:
    key = generate_key()
    aes = AES()

    # Encrypting and decrypting a dictionary
    data = {'name': 'Alice', 'age': 30}
    encrypted_data = aes.encrypt(data)
    decrypted_data = aes.decrypt(encrypted_data)
    print(decrypted_data)  # Output should be {'name': 'Alice', 'age': 30}
