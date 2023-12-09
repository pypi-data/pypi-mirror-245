from pathlib import Path

from .func import *
from .logger import logger


DEFAULT_ANYLEARN_HOST = "https://anylearn.nelbds.cn"


def get_config_path() -> Path:
    config_dir = Path.home() / ".anylearn"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.yaml"


def no_none_filter(data: dict):
    return dict(list(filter(lambda item:item[1] is not None, list(data.items()))))
