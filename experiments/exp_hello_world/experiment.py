"""
To run this script:
poetry run main --config-name config
"""

import logging
from omegaconf import DictConfig

log = logging.getLogger(__name__)


def run(cfg: DictConfig) -> None:
    """Entry point to experiment

    Args:
        cfg (DictConfig): [description]
    """
    log.debug("Hello World")