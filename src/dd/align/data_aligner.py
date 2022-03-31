from src.dd.align.chunker import Chunker
from src.dd.align.segmenter import FixedSizeSegmenter


class DataAligner:
    def __init__(self, chunk_size, segment_size):
        self.chunker = Chunker(avg_size=chunk_size)
        self.segmenter = FixedSizeSegmenter(segment_size=segment_size)

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


