"""
Serverless elasticsearch curator handler.
"""

import os
import shutil
import logging
import collections

import requests
from requests.exceptions import RequestException

from curator.cli import run as run_curator


Config = collections.namedtuple('Config', ['CONFIG_FILE', 'ACTION_FILE'])


# pylint: disable=invalid-name
logger = logging.getLogger()


class CuratorException(Exception):
    """Base exception class"""


class ConfigMissingError(CuratorException):
    """Raised when configuration is missing"""


class ConfigDownloadError(CuratorException):
    """Raised when configuration download gone awry"""


def resolve_config_entry(config_entry, event, env):
    """
    Resolve configuration field from event or environment.
    """
    return event.get(config_entry, env.get(config_entry))


def is_url(config_file):
    """
    Returns true if 'config_file` starts with `http` which indicates that it's
    an url.
    """
    return config_file.startswith('http')


def download_file(url, path, timeout=5):
    """
    Downloads file from ``url`` ans saves it at ``path``.
    """
    try:
        file_response = requests.get(url, stream=True, timeout=timeout)
    except RequestException as rexc:
        raise ConfigDownloadError(
            f"Failed to download `{url}`: {rexc}") from None
    if file_response.status_code != requests.codes.ok: # pylint: disable=no-member
        raise ConfigDownloadError(
            f"Failed to download `{url}`: {file_response.status_code}")
    with open(path, 'wb') as path_file:
        file_response.raw.decode_content = True
        shutil.copyfileobj(file_response.raw, path_file)


def local_or_remote_file(config_entry, config_value, run_config):
    """
    Use local file or download one from given url

    Returns updated ``run_config``
    """
    if is_url(config_value):
        download_file(
            url=config_value,
            path=getattr(run_config, config_entry)
        )
        logger.info(
            "%s: `%s` downloaded and saved.",
            config_entry, config_value)
    else:
        run_config = run_config._replace(**{config_entry: config_value})
    return run_config


def configure(event, env, run_config=None):
    """
    Create configuration object from environment variables.
    If any of configuration keys is missing, raises `ConfigMissingError`.
    """
    if run_config is None:
        run_config = Config(
            CONFIG_FILE=os.path.join('/tmp', 'config.yml'),
            ACTION_FILE=os.path.join('/tmp', 'action.yml'),
        )
    for config_entry in Config._fields:
        config_value = resolve_config_entry(config_entry, event, env)
        if not config_value:
            raise ConfigMissingError(
                f"Missing configuration env variable {config_entry}")
        run_config = local_or_remote_file(
            config_entry, config_value, run_config)
    return run_config


# pylint: disable=unused-argument
def handler(event, context):
    """
    Curator serverless handler
    """
    logger.info("Initializing curator's configuration.")
    config = configure(event, os.environ)
    run_curator(config.CONFIG_FILE, config.ACTION_FILE)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s][%(asctime)s.%(msecs)dZ] %(message)s",
    )
    handler(None, None)
