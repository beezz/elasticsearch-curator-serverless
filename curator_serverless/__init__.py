"""
Serverless elasticsearch curator handler.
"""

import os
import shutil
import logging
import collections

import requests

from curator.cli import run as run_curator
from requests.exceptions import RequestException

Config = collections.namedtuple('Config', ['CONFIG_FILE', 'ACTION_FILE'])
# Downloaded configuration will reside at those locations
run_config = Config(
    CONFIG_FILE=os.path.join('/tmp', 'config.yml'),
    ACTION_FILE=os.path.join('/tmp', 'action.yml'),
)


logger = logging.getLogger()


class CuratorException(Exception):
    """Base exception class"""


class ConfigMissingError(CuratorException):
    """Raised when configuration is missing"""


class ConfigDownloadError(CuratorException):
    """Raised when configuration download gone awry"""


def configure_from_env():
    """
    Create configuration object from environment variables.
    If any of configuration keys is missing, raises `ConfigMissingError`.
    """
    config_kwargs = {}
    for config_entry in Config._fields:
        if not os.getenv(config_entry):
            raise ConfigMissingError(
                f"Missing configuration env variable {config_entry}")
        config_kwargs[config_entry] = os.getenv(config_entry)
    return Config(**config_kwargs)


def download_file(url, path, timeout=5):
    """
    Downloads file from ``url`` ans saves it at ``path``.
    """
    try:
        file_response = requests.get(url, stream=True, timeout=timeout)
    except RequestException as rexc:
        raise ConfigDownloadError(
            f"Failed to download `{url}`: {rexc}") from None
    if file_response.status_code != requests.codes.ok:
        raise ConfigDownloadError(
            f"Failed to download `{url}`: {file_response.status_code}")
    with open(path, 'wb') as path_file:
        file_response.raw.decode_content = True
        shutil.copyfileobj(file_response.raw, path_file)


def handler(event, context):
    logger.info("Initializing curator's configuration.")
    env_config = configure_from_env()
    logger.info("Getting CONFIG_FILE: `%s`", env_config.CONFIG_FILE)
    download_file(env_config.CONFIG_FILE, run_config.CONFIG_FILE)
    logger.info(
        "CONFIG_FILE: `%s` downloaded and saved.", env_config.CONFIG_FILE)
    logger.info("Getting ACTION_FILE: %s", env_config.ACTION_FILE)
    download_file(env_config.ACTION_FILE, run_config.ACTION_FILE)
    logger.info("ACTION_FILE: `%s` downloaded and saved.", env_config.ACTION_FILE)
    run_curator(run_config.CONFIG_FILE, run_config.ACTION_FILE)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s][%(asctime)s.%(msecs)dZ] %(message)s",
    )
    handler()
