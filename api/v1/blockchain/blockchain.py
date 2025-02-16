import json
import time
import hashlib

from api.v1.blockchain.schemas import Block


class Blockchain:
    def __init__(self):
        self.chain: list[Block] = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_data = {'message': 'Genesis Block'}
        timestamp = time.time()
        genesis_hash = self.calculate_hash(0, timestamp, genesis_data, '0')
        genesis_block = Block(
            index=0,
            timestamp=timestamp,
            data=genesis_data,
            previous_hash='0',
            hash=genesis_hash
        )
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, data: dict) -> Block:
        previous_block = self.get_latest_block()
        index = previous_block.index + 1
        timestamp = time.time()
        previous_hash = previous_block.hash
        new_hash = self.calculate_hash(index, timestamp, data, previous_hash)
        new_block = Block(
            index=index,
            timestamp=timestamp,
            data=data,
            previous_hash=previous_hash,
            hash=new_hash
        )
        self.chain.append(new_block)
        return new_block

    def get_chain(self) -> list[Block]:
        return self.chain

    @classmethod
    def calculate_hash(cls, index: int, timestamp: float, data: dict, previous_hash: str) -> str:
        block_str = json.dumps({
            'index': index,
            'timestamp': timestamp,
            'data': data,
            'previous_hash': previous_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_str).hexdigest()