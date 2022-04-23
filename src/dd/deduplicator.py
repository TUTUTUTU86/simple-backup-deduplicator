from src.dd.store.manifest_store import ManifestStore
from src.dd.align.segmenter import Manifest
from src.dd.store.chunk_store import ChunkStore
import logging


class Deduplicator:

    def __init__(self, manifest_store: ManifestStore):
        self.manifest_store = manifest_store
        self.chunk_store = ChunkStore()
        self.n_new = 0
        self.n_dup = 0
        self.n_dedup = 0

    def do(self, segment, champions) -> Manifest:
        champions_hashes = set()
        for champion in champions:
            champions_hashes.update(self.manifest_store.load(champion).hash_list)

        manifest = Manifest()
        for chunk in segment.chunks:
            if chunk.hash not in champions_hashes:
                result = self.chunk_store.store(chunk.hash)
                if result == 0:
                    self.n_new += 1
                else:
                    self.n_dup += 1
            else:
                self.n_dedup += 1

            manifest.hash_list.append(chunk.hash)

        return manifest

    def print(self):
        print("New: ", self.n_new, "Deduplicated: ", self.n_dedup, "Duplicates: ", self.n_dup)
        logging.info("Deduplication results:")
        logging.info("New: " + str(self.n_new) + " Deduplicated: " + str(self.n_dedup) + " Duplicates: " + str(self.n_dup))
