from fastcdc.fastcdc_py import Chunk


class Segment:
    def __init__(self):
        self.chunks = []
        self.size = 0

    def append(self, chunk: Chunk):
        self.chunks.append(chunk)
        self.size += chunk.length


class Segmenter:
    def __init__(self):
        ...

    def push(self, chunk: Chunk):
        ...

    def flush(self):
        ...


class FixedSizeSegmenter(Segmenter):
    def __init__(self, segment_size):
        super().__init__()
        self.segment_size = segment_size
        self.current_segment = Segment()

    def push(self, chunk: Chunk):
        if self.current_segment.size + chunk.length < self.segment_size:
            self.current_segment.append(chunk)
            return None
        segment = self.current_segment
        self.current_segment = Segment()
        self.current_segment.append(chunk)
        return segment

    def flush(self):
        if self.current_segment.size > 0:
            segment = self.current_segment
            self.current_segment = Segment()
            return segment
        else:
            return None
