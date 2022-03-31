from src.dd.align.segmenter import Manifest
from src.dd.store.manifest_store import ManifestStore
from src.dd.omega_sparse_index import SparseIndexOmega


class ChampionChooser:
    def __init__(self, max_champions, manifest_store: ManifestStore):
        self.sparse_index = SparseIndexOmega()
        self.manifest_store = manifest_store
        self.max_champions = max_champions
        self.index = {}

    def choose(self, hooks) -> list:
        champions = []


    def add(self, manifest: Manifest, hooks):
        segment_id = self.manifest_store.counter
        for hook in hooks:
            self.sparse_index.add(hook, segment_id)
        self.manifest_store.save(manifest)
