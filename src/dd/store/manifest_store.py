import shelve

from src.dd.align.segmenter import Manifest


class ManifestStore:
    def __init__(self, file_name):
        self.file_name = "manifests.data"
        self.counter = 0

    def save(self, manifest: Manifest):
        with shelve.open(self.file_name) as store:
            store[str(self.counter)] = manifest
            self.counter += 1

    def load(self, index) -> Manifest:
        with shelve.open(self.file_name) as store:
            return store[str(index)]
