"""Connection functions."""

import yaml

from loguru import logger as log
from atlassian import Confluence


def connect(config: str) -> Confluence:
    """Load the config file and establish a connection to Confluence.

    Parameters
    ----------
    config : str
        The path to a yaml configuration file.

    Returns
    -------
    Confluence
        The confluence connection object.
    """
    with open(config, "r", encoding="utf-8") as conffile:
        conf = yaml.safe_load(conffile)
        log.debug(f"Loaded configuration settings from [{config}].")

    cfc = Confluence(
        url=conf["url"],
        username=conf["username"],
        password=conf["password"],
    )
    log.debug(f"Successfully connected to [{conf['url']}].")

    return cfc
