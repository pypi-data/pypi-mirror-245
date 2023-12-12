import tomllib
from collections.abc import Callable
from pathlib import Path
from threading import RLock
from typing import Any


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


_config_lock = RLock()


def _synchronized(func: Callable) -> Callable:
    """
    Synchronizes config file operations

    :param func: function to be synchronized
    :return: None
    """

    def wrapper(*args, **kwargs: Any) -> Any:
        _config_lock.acquire()
        try:
            return func(*args, **kwargs)
        finally:
            _config_lock.release()

    return wrapper


class Configuration:
    config_dir = Path.home() / "Library/Application Support" / "shelloracle"

    def __enter__(self):
        self.config_dir.mkdir(exist_ok=True)
        _config_lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        _config_lock.release()


"""
Let's prototype some of the Configuration usage

Priority:
1. Command line arguments
2. Environment variables
3. Configuration file

# Do I like the config as a context manager? 
with Configuration(in_memory?=True) as config:
    a = config.a
    b = config.b
"""

if __name__ == '__main__':
    with open("../config.toml", "rb") as config_file:
        config = tomllib.load(config_file)
        print(config)
