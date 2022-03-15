import shelve

from segmenter import Segment

class ManifestStore:
    def __init__(self):
        self.FILE_NAME = "manifests.data"


    def add(self, segment: Segment):
        with shelve.open(self.FILE_NAME) as store:
            store[""]
