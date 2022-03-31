import shelve

from segmenter import Manifest


class ManifestStore:
    def __init__(self):
        self.FILE_NAME = "manifests.data"
        self.counter = 0

    def save(self, manifest: Manifest):
        with shelve.open(self.FILE_NAME) as store:
            store[self.counter] = manifest
            self.counter += 1

    def load(self, index):
        with shelve.open(self.FILE_NAME) as store:
            return store[index]
