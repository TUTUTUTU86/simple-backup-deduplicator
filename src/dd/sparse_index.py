import hydra
from hydra.utils import instantiate
from omegaconf import DictConfig

from defaults import CONFIGS_ROOT, DATA_ROOT, RESULTS_ROOT


class SparseIndex:
    def __init__(self, cfg: DictConfig):
        self.data_aligner = instantiate(cfg.data_aligner)

    def do(self, files):
        for i, segment in enumerate(self.data_aligner.do(files)):
            print(i)
            hooks = []
            for chunk in segment.chunks:
                if is_hook(chunk.hash):
                    hooks.append(chunk.hash)

            champions = self.champion_chooser.choose(hooks)
            manifest = self.deduplicator.do(segment, champions)
            self.champion_chooser.add(manifest)


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
