import logging
import hydra
from omegaconf import DictConfig

from defaults import CONFIGS_ROOT, RESULTS_ROOT
from testing_system import LinuxTest


@hydra.main(config_path=CONFIGS_ROOT, config_name="fixed_improv")
def main(cfg: DictConfig):
    logging.basicConfig(filename="sample2.log", level=logging.INFO)
    linux_test = LinuxTest(cfg)
    linux_test.current_testing()


if __name__ == '__main__':
    import sys

    sys.argv.append(f'hydra.run.dir="{RESULTS_ROOT}"')
    main()
