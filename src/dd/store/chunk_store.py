from fastcdc.fastcdc_py import Chunk
import logging


class ChunkStore:
    def __init__(self):
        self.chunks_hashes = set()
        self.total_store_size = 0
        self.total_ineffective_space = 0

    def store(self, chunk: Chunk):
        if chunk.hash in self.chunks_hashes:
            self.total_ineffective_space += chunk.length
            return 1
        else:
            self.chunks_hashes.add(chunk.hash)
            self.total_store_size += chunk.length
            self.total_ineffective_space += chunk.length
            return 0

    def print(self, total_saved_space):
        logging.info("Total store size: " + str(self.total_store_size + total_saved_space))
        logging.info("Total ineffective size: " + str(self.total_ineffective_space + total_saved_space))
        max_dd = (1 - ((self.total_store_size + total_saved_space) / (self.total_ineffective_space + total_saved_space))) * 100
        real_dd = (1 - (self.total_ineffective_space / (self.total_ineffective_space + total_saved_space))) * 100
        logging.info("MaxDD%   " + str(max_dd))
        logging.info("RealDD%   " + str(real_dd))


