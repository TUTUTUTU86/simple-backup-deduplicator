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
        hooks = set(hooks)
        champions = []
        while len(champions) < self.max_champions:
            segments_score = {}
            segments_hooks = {}
            for hook in hooks:
                if hook in self.sparse_index.sparse_index:
                    for segment_id in self.sparse_index.get(hook):
                        if segment_id in segments_score:
                            segments_score[segment_id] += 1
                            segments_hooks[segment_id] = set([hook])
                        else:
                            segments_score[segment_id] = 1
                            segments_hooks[segment_id].update(set([hook]))

            max_score = 0
            for segment in segments_score:
                if segments_score[segment] > max_score:
                    max_score = segments_score[segment]
                    champion = segment
            if max_score != 0:
                hooks -= segments_hooks[champion]
                champions.append(champion)
            else:
                break
        return champions

    def add(self, manifest: Manifest, hooks):
        segment_id = self.manifest_store.counter
        for hook in hooks:
            self.sparse_index.add(hook, segment_id)
        self.manifest_store.save(manifest)
