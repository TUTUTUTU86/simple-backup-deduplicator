from fastcdc import fastcdc_py
from xxhash import xxh64


class Chunker:
    def __init__(self, avg_size):
        self.avg_size = avg_size

    def do(self, data):
        chunks = list(fastcdc_py.fastcdc_py(data=data,
                                            avg_size=self.avg_size,
                                            min_size=self.avg_size // 2,
                                            max_size=self.avg_size * 2,
                                            fat=True,
                                            hf=xxh64))
        for chunk in chunks:
            chunk.length = len(chunk.data)
        return chunks
