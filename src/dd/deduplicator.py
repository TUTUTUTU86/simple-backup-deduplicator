from sparse_index import SparseIndex
from manifest_store import ManifestStore


class Deduplicator:

    def __init__(self, sparse_index: SparseIndex, manifest_store: ManifestStore):
        self.sparse_index = sparse_index
        self.manifest_store = manifest_store

    def do(self, segment_hash, champions_hash):
        segment = self.manifest_store.load(segment_hash)
        champions = [];
        for champion_hash in champions_hash:
            champions.append(self.manifest_store.load(champion_hash))


