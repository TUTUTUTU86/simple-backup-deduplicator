

class Segmenter:
    def __init__(self):
        ...

    def make_segment(self):
        ...


class FixedSizeSegmenter(Segmenter):
    def __init__(self, segment_size):
        Segmenter.__init__()
        self.not_used_chunks = []
        self.segment_size = segment_size

    def make_segment(self, chunks: list):
        if len(chunks) < self.segment_size:
            self.not_used_chunks.extend(chunks)
            return




