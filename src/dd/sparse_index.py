import numpy as np
import hydra
import logging
from hydra.utils import instantiate
from omegaconf import DictConfig
from collections import Counter

from defaults import CONFIGS_ROOT, DATA_ROOT, RESULTS_ROOT
from src.dd.store.manifest_store import ManifestStore
from src.dd.deduplicator import Deduplicator
from src.dd.champion_chooser import ChampionChooser
from src.dd.align.segmenter import Manifest


class CaptainHook:
    def __init__(self, hook_prefix_len):
        self.hook_len = hook_prefix_len
        self.pref_len = int(4 * np.ceil(hook_prefix_len / 4))

    def is_hook(self, h):
        pref = h[:self.pref_len // 4]
        pref = int(pref, 16)
        return pref < 2 ** (self.pref_len - self.hook_len)


class SparseIndex:
    def __init__(self, cfg: DictConfig):
        self.data_aligner = instantiate(cfg.data_aligner)
        self.captain_hook = instantiate(cfg.captain_hook)
        self.manifest_store = ManifestStore(file_name="manifest.store")
        self.deduplicator = Deduplicator(manifest_store=self.manifest_store)
        self.champion_chooser = ChampionChooser(5, self.manifest_store)
        self.global_counter = Counter()

    def do(self, files):
        for i, segment in enumerate(self.data_aligner.do(files)):
            hooks = []
            self.global_counter[segment.chunks[-1].hash] += 1
            for chunk in segment.chunks:
                if self.captain_hook.is_hook(chunk.hash):
                    hooks.append(chunk.hash)
            # print(hooks)
            champions = self.champion_chooser.choose(hooks)
            # print(champions)
            manifest = self.deduplicator.do(segment, champions)
            self.champion_chooser.add(manifest, hooks)
        self.print()
        self.deduplicator.print()

    def print(self):
        e = 0
        n = sum(self.global_counter.values())
        for c in self.global_counter:
            e -= self.global_counter[c] / n * np.log2(self.global_counter[c] / n)
        print("Total entropy: " + str(e))
        logging.info("Total entropy: " + str(e))


@hydra.main(config_path=CONFIGS_ROOT, config_name="sparse_index")
def main(cfg: DictConfig):
    sparse_index = SparseIndex(cfg)
    sparse_index.do([
        DATA_ROOT / "dd_test" / "data1.zip",
        DATA_ROOT / "dd_test" / "data2.zip"
    ])
    print(cfg)


if __name__ == '__main__':
    import sys
    sys.argv.append(f'hydra.run.dir="{RESULTS_ROOT}"')
    main()
