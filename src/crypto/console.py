import os
import logging
import importlib
from omegaconf import DictConfig
import hydra
from hydra.utils import get_original_cwd

from . import __version__

log = logging.getLogger(__name__)


@hydra.main(config_path="../../configs", config_name="config")
def main(cfg: DictConfig) -> None:
    """Entrypoint"""
    experiment = f"experiments.{cfg.experiment.name}"

    log.info(f"Starting {experiment}")

    # Workaround for hydra
    os.chdir(get_original_cwd())

    module = importlib.import_module(experiment)
    module.run(cfg)