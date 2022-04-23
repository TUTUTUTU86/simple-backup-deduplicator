import subprocess
from pathlib import Path
from enum import Enum
import logging
import hydra
from omegaconf import DictConfig

from defaults import CONFIGS_ROOT, RESULTS_ROOT
from src.dd.sparse_index import SparseIndex

LINUX_DATA_ROOT = Path("D:\dev\Research_work\linuxes")


class LinuxData(Enum):
    ...


class LinuxDataZip(LinuxData):
    VERSION_5_12 = "linux-5.12.zip",
    VERSION_5_13 = "linux-5.13.zip",
    VERSION_5_14 = "linux-5.14.zip",
    VERSION_5_15 = "linux-5.15.zip",
    VERSION_5_16 = "linux-5.16.zip",
    VERSION_5_17 = "linux-5.17.zip"


class LunixTest:
    def __init__(self, cfg: DictConfig):
        self.sparse_index = SparseIndex(cfg)

    def deduplicate_zips(self,  versions: list):
        self.sparse_index.do([(LINUX_DATA_ROOT / data.value[0]) for data in versions])


@hydra.main(config_path=CONFIGS_ROOT, config_name="sparse_index")
def main(cfg: DictConfig):
    logging.basicConfig(filename="sample.log", level=logging.INFO)
    linux_test = LunixTest(cfg)
    linux_test.deduplicate_zips([LinuxDataZip.VERSION_5_12, LinuxDataZip.VERSION_5_13])

if __name__ == '__main__':
    import sys
    sys.argv.append(f'hydra.run.dir="{RESULTS_ROOT}"')
    main()
