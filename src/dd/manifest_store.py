import shelve

from segmenter import Segment


class ManifestStore:
    def __init__(self):
        self.FILE_NAME = "manifests.data"

    def save(self, segment: Segment):
        with shelve.open(self.FILE_NAME) as store:
            store[segment.hash] = segment

    def load(self, hash):
        with shelve.open(self.FILE_NAME) as store:
            return shelve[hash]
