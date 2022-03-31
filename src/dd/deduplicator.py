from src.dd.store.manifest_store import ManifestStore
from src.dd.align.segmenter import Manifest


class Deduplicator:

    def __init__(self, manifest_store: ManifestStore):
        self.manifest_store = manifest_store
        self.n_new = 0
        self.n_dup = 0
        self.n_dedup = 0

    def do(self, segment, champions) -> Manifest:
        segment = self.manifest_store.load(segment)
        champions_hashes = set()
        for champion in champions:
            champions_hashes.update(self.manifest_store.load(champion))

        manifest = Manifest()
        for chunk in segment.chunks:
            if chunk.hash not in champions_hashes:
                result = self.chunk_store.store(chunk)
                if result == 0:
                    self.n_new += 1
                else:
                    self.n_dup += 1
            else:
                self.n_dedup += 1

            manifest.hash_list.append(chunk.hash)

        return manifest





