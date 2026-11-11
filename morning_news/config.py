"""Config block: reads the settings in config.toml."""

import tomllib  # part of Python's standard library, no install needed
from pathlib import Path

# config.toml sits in the project folder, one level above this file's folder.
CONFIG_PATH = Path(__file__).parent.parent / "config.toml"


def load_config() -> dict:
    """Return everything in config.toml as a dictionary."""
    with open(CONFIG_PATH, "rb") as file:
        return tomllib.load(file)
