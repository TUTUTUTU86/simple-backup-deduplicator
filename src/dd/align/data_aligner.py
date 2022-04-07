from src.dd.align.chunker import Chunker
from src.dd.align.segmenter import FixedSizeSegmenter, AbstractSegmenter


class DataAligner:
    def __init__(self, chunk_size, segmenter: AbstractSegmenter):
        self.chunker = Chunker(avg_size=chunk_size)
        self.segmenter = segmenter

    def do(self, files: list):
        for file in files:
            with open(file, 'rb') as f:
                chunks = self.chunker.do(f)
            for chunk in chunks:
                segment = self.segmenter.push(chunk)
                if segment is not None:
                    yield segment
        segment = self.segmenter.flush()
        if segment is not None:
            yield segment


