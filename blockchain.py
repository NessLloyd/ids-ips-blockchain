import datetime
import hashlib

class Source:
    def __init__(self, user_id, transaction_id, cookie):
        self.user_id = user_id
        self.transaction_id = transaction_id
        self.cookie = cookie
        self.timestamp = datetime.datetime.now()

    def __str__(self):
        return f"UserID: {self.user_id}, TransactionID: {self.transaction_id}, Cookie: {self.cookie}, Timestamp: {self.timestamp}"

class Block:
    def __init__(self, blockNo, data, previous_hash='0'*64):
        self.blockNo = blockNo
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.timestamp = datetime.datetime.now()
        self.hash = self.compute_hash()

    def compute_hash(self):
        h = hashlib.sha256()
        h.update(
            str(self.blockNo).encode('utf-8') +
            str(self.data).encode('utf-8') +
            str(self.previous_hash).encode('utf-8') +
            str(self.nonce).encode('utf-8') +
            str(self.timestamp).encode('utf-8')
        )
        return h.hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty
        while not self.compute_hash().startswith(target):
            self.nonce += 1
            self.hash = self.compute_hash()

    def __str__(self):
        return f"BlockNo: {self.blockNo}\nData: {self.data}\nHash: {self.hash}\nPrevHash: {self.previous_hash}\nNonce: {self.nonce}\nTimestamp: {self.timestamp}\n----------------------"

class Blockchain:
    def __init__(self, difficulty=3):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, "Genesis Block", previous_hash='0'*64)
        self.chain.append(genesis_block)

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), data, previous_block.hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        return new_block

    def trace_source(self, identifier):
        traced_blocks = []
        for block in self.chain:
            if isinstance(block.data, Source):
                if (block.data.user_id == identifier or
                    block.data.transaction_id == identifier or
                    block.data.cookie == identifier):
                    traced_blocks.append(block)
        return traced_blocks
