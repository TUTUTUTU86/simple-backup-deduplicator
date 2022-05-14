import subprocess
from pathlib import Path
from enum import Enum
import logging
import hydra
import omegaconf
from omegaconf import DictConfig
import os
import time

from defaults import CONFIGS_ROOT, RESULTS_ROOT, LINUX_DATA_ROOT
from src.dd.sparse_index import SparseIndex
from src.ff.simple_folder_index import process



class LinuxData(Enum):
    ...


class LinuxDataZip(LinuxData):
    VERSION_5_12 = "linux-5.12.zip"
    VERSION_5_13 = "linux-5.13.zip"
    VERSION_5_14 = "linux-5.14.zip"
    VERSION_5_15 = "linux-5.15.zip"
    VERSION_5_16 = "linux-5.16.zip"
    VERSION_5_17 = "linux-5.17.zip"


class LinuxDataFolder(LinuxData):
    VERSION_5_12 = "linux-5.12"
    VERSION_5_13 = "linux-5.13"
    VERSION_5_14 = "linux-5.14"
    VERSION_5_15 = "linux-5.15"
    VERSION_5_16 = "linux-5.16"
    VERSION_5_17 = "linux-5.17"


class LinuxTest:
    def __init__(self, cfg: DictConfig):
        self.sparse_index = SparseIndex(cfg)
        self.cfg = cfg

    def deduplicate_zips(self, versions: list):
        self.sparse_index.do([(LINUX_DATA_ROOT / data.value) for data in versions])
        self.sparse_index.print()

    def deduplicate_folders(self, versions: list):

        for version in versions:
            all_files = []
            root_dir = LINUX_DATA_ROOT / version.value
            result = []
            for root, dirs, files in os.walk(root_dir):
                result.extend([Path(os.path.join(root, file)) for file in files])
            # print(result)
            all_files.extend(result)
            print(f"total {len(all_files)} files")
            self.sparse_index.do(all_files)
        self.sparse_index.print()

    def test_with_all_linux_versions_folders(self):
        versions = [version for version in LinuxDataFolder]
        logging.info("------------------NEW TEST-------------------")
        logging.info("----TYPE: ALL LINUX FOLDERS----")
        logging.info("-----WITH CONFIG: " + str(self.cfg) + " -----")
        logging.info("WITH LINUX VERSIONS:  " + str(versions))
        start_time = time.perf_counter()
        self.deduplicate_folders(versions)
        logging.info("------TIME: " + str(time.perf_counter() - start_time) + " ------")
        logging.info("------------------NEW TEST-------------------")

    def test_with_all_linux_versions_zips(self):
        versions = [version for version in LinuxDataZip]
        logging.info("------------------NEW TEST-------------------")
        logging.info("----TYPE: ALL LINUX ZIPS----")
        logging.info("-----WITH CONFIG: " + str(self.cfg) + " -----")
        logging.info("WITH LINUX VERSIONS:  " + str(versions))
        start_time = time.perf_counter()
        self.deduplicate_zips(versions)
        logging.info("------TIME: " + str(time.perf_counter() - start_time) + " ------")
        logging.info("------------------NEW TEST-------------------")

    def test_zips(self, versions):
        logging.info("------------------NEW TEST-------------------")
        logging.info("----TYPE: SPECIFIC LINUX ZIPS----")
        logging.info("-----WITH CONFIG: " + str(self.cfg) + " -----")
        logging.info("WITH LINUX VERSIONS:  " + str(versions))
        start_time = time.perf_counter()
        self.deduplicate_zips(versions)
        logging.info("------TIME: " + str(time.perf_counter() - start_time) + " ------")
        logging.info("------------------NEW TEST-------------------")

    def test_folders(self, versions):
        logging.info("------------------NEW TEST-------------------")
        logging.info("----TYPE: ALL LINUX FOLDERS----")
        logging.info("-----WITH CONFIG: " + str(self.cfg) + " -----")
        logging.info("WITH LINUX VERSIONS:  " + str(versions))
        start_time = time.perf_counter()
        self.deduplicate_folders(versions)
        logging.info("------TIME: " + str(time.perf_counter() - start_time) + " ------")
        logging.info("------------------NEW TEST-------------------")


@hydra.main(config_path=CONFIGS_ROOT, config_name="fixed_base")
def main(cfg: DictConfig):
    logging.basicConfig(filename="sample2.log", level=logging.INFO)
    linux_test = LinuxTest(cfg)
    linux_test.test_with_all_linux_versions_folders()
    lunix_test2 = LinuxTest(cfg)
    lunix_test2.test_with_all_linux_versions_zips()


if __name__ == '__main__':
    import sys

    sys.argv.append(f'hydra.run.dir="{RESULTS_ROOT}"')
    main()
