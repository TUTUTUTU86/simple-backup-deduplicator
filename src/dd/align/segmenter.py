from fastcdc.fastcdc_py import Chunk


class Segment:
    def __init__(self, chunks=None):
        if chunks is None:
            self.chunks = []
            self.size = 0
        else:
            self.chunks = chunks
            self.size = sum(map(lambda x: x.length, chunks))

    def append(self, chunk: Chunk):
        self.chunks.append(chunk)
        self.size += chunk.length


class Manifest:
    def __init__(self):
        self.hash_list = []


class AbstractSegmenter:

    def __init__(self):
        self.current_segment = Segment()

    def push(self, chunk: Chunk):
        ...

    def flush(self):
        if self.current_segment.size > 0:
            segment = self.current_segment
            self.current_segment = Segment()
            return segment
        else:
            return None


class FixedSizeSegmenter(AbstractSegmenter):

    def __init__(self, segment_size):
        super().__init__()
        self.segment_size = segment_size

    def push(self, chunk: Chunk):
        if self.current_segment.size + chunk.length < self.segment_size:
            self.current_segment.append(chunk)
            return None
        segment = self.current_segment
        self.current_segment = Segment()
        self.current_segment.append(chunk)
        return segment


class VariableSizeSegmenter(AbstractSegmenter):
    def __init__(self, chunk_size, segment_size, rolling_hash):
        super().__init__()
        self.segment_size = segment_size
        self.min_segment_size = 0.7 * segment_size
        self.max_segment_size = 1.3 * segment_size
        self.main_divisor = int(0.6 * segment_size / chunk_size)
        self.backup_divisor = self.main_divisor // 2  # (from paper on TTTD)
        self.backup_break_pos = 0
        self.window = 0
        self.x = rolling_hash.x
        self.q = rolling_hash.q
        self.curr_hash_val = 0
        self.x_pow = 1

    def push(self, chunk: Chunk):
        if self.current_segment.size < self.min_segment_size:
            # not at min size of the chunk
            self.current_segment.append(chunk)
            return None
        self._update_curr_hash()
        if (self.curr_hash_val % self.backup_divisor) == (self.backup_divisor - 1):
            # found possible segment breakpoint
            self.backup_break_pos = len(self.current_segment.chunks)
        if (self.curr_hash_val % self.main_divisor) == (self.main_divisor - 1):
            # found segment breakpoint
            res = self.flush()
            self.current_segment.append(chunk)
            return res
        if self.current_segment.size < self.max_segment_size:
            # not at max size of the chunk
            self.current_segment.append(chunk)
            return None
        # curr_seg_len >= max_threshold
        # if we have backup breakpoint, we yield the part of the segment
        # otherwise, pop last chunk and yield the resulting segment
        if self.backup_break_pos != 0:
            new_seg = Segment(self.current_segment.chunks[self.backup_break_pos:])
            new_seg.append(chunk)
            self.current_segment = Segment(self.current_segment.chunks[:self.backup_break_pos])
            res = self.flush()
            self.current_segment = new_seg
            return res
        else:
            new_seg = Segment(self.current_segment.chunks[-1:])
            new_seg.append(chunk)
            self.current_segment = Segment(self.current_segment.chunks[:-1])
            res = self.flush()
            self.current_segment = new_seg
            return res

    def flush(self):
        self.backup_break_pos = 0
        self.window = 0
        self.curr_hash_val = 0
        self.x_pow = 1
        return super().flush()

    def _update_curr_hash(self):
        sl = len(self.current_segment.chunks)
        self.window = sl if not self.window else self.window
        if not self.curr_hash_val:
            for chunk in self.current_segment.chunks[::-1]:
                self.curr_hash_val = (self.curr_hash_val + int(chunk.hash, 16) * self.x_pow) % self.q
                self.x_pow = (self.x_pow * self.x) % self.q
        else:
            self.curr_hash_val = ((self.curr_hash_val -
                                   int(self.current_segment.chunks[sl - self.window - 1].hash, 16) * self.x_pow) * self.x +
                                  int(self.current_segment.chunks[-1].hash, 16)) % self.q
