from fastcdc.fastcdc_py import Chunk


class ChunkStore:
    def __init__(self):
        self.chunks_hashes = set()

    def store(self, chunk_hash):
        if chunk_hash in self.chunks_hashes:
            return 1
        else:
            self.chunks_hashes.add(chunk_hash)
            return 0


