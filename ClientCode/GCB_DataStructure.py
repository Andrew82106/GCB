class Block:
    def __init__(self, prehash, timestamp, data, nonce, block_hash):
        self.prehash = prehash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.block_hash = block_hash


class Chain(Block):
    def __init__(self):
        super().__init__()
        # 创建一条链的时候应该干啥，这还没想好，先不着急写