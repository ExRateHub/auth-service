import logging.config

import yaml

from core.config import PROJECT_DIR

LOGGING_CONFIG_FILE = PROJECT_DIR / "logging.yaml"


def setup_logging() -> None:
    with open(LOGGING_CONFIG_FILE) as file:
        logging_config = yaml.safe_load(file)
    logging.config.dictConfig(logging_config)


def get_logger(name: str = "root") -> logging.Logger:
    return logging.getLogger(name)
