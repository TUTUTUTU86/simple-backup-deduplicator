class ChunkStore:
    def __init__(self):
        self.chunks = set([])

    def store(self, chunk):
        if chunk in self.chunks:
            return 1
        else:
            self.chunks.add(chunk)
            return 0


