import os
import json

from .exceptions import ConfigurationError
from .logging import get_logger

logger = get_logger(__name__)

default_paths = [
    os.path.expanduser('~/.ufv-alerts.rc'),
    '/etc/ufv-alerts.rc',
]

def read(conf_file=None):

    config = None
    logger.warn([conf_file or ''] + default_paths)

    for path in [conf_file or ''] + default_paths:
        with open(path, 'r') as f:
            config = json.load(f)
            break

    if not config:
        raise ConfigurationError
