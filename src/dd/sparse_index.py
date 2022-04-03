import numpy as np
import hydra
from hydra.utils import instantiate
from omegaconf import DictConfig

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

    def do(self, files):
        for i, segment in enumerate(self.data_aligner.do(files)):
            hooks = []
            for chunk in segment.chunks:
                if self.captain_hook.is_hook(chunk.hash):
                    hooks.append(chunk.hash)
            print(hooks)
            champions = self.champion_chooser.choose(hooks)
            print(champions)
            manifest = self.deduplicator.do(segment, champions)
            self.champion_chooser.add(manifest, hooks)


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
