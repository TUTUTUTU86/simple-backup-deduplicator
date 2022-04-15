import os.path
from pathlib import Path

from src.dd.align.chunker import Chunker
from src.dd.align.segmenter import FixedSizeSegmenter, AbstractSegmenter


class DataAligner:
    def __init__(self, chunk_size, segmenter: AbstractSegmenter):
        self.chunker = Chunker(avg_size=chunk_size)
        self.segmenter = segmenter

    def do(self, files: list):
        if len(files) == 0:
            raise Exception("There is no files to work with")
        lcp = Path(files[0]).parent
        for file in files:
            if lcp != Path(file).parent:
                lcp = Path(file).parent
                yield segment
            with open(file, 'rb') as f:
                chunks = self.chunker.do(f)
            for chunk in chunks:
                segment = self.segmenter.push(chunk)
                if segment is not None:
                    yield segment
        segment = self.segmenter.flush()
        if segment is not None:
            yield segment


class PrimitiveDataAligner(DataAligner):
    def __init__(self, chunk_size, segmenter: AbstractSegmenter):
        super(PrimitiveDataAligner, self).__init__(chunk_size, segmenter)

    def do(self, files: list):
        if len(files) == 0:
            raise Exception("There is no files to work with")
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

