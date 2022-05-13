from fastcdc.fastcdc_py import Chunk
import logging


class ChunkStore:
    def __init__(self):
        self.chunks_hashes = set()
        self.total_store_size = 0
        self.total_ineffective_size = 0

    def store(self, chunk: Chunk):
        if chunk.hash in self.chunks_hashes:
            self.total_ineffective_size += chunk.length
            return 1
        else:
            self.chunks_hashes.add(chunk.hash)
            self.total_store_size += chunk.length
            self.total_ineffective_size += chunk.length
            return 0

    def print(self):
        logging.info("Total store size: " + str(self.total_store_size))
        logging.info("Total ineffective size: " + str(self.total_ineffective_size))


