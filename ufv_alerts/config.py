import os
import configparser

from .exceptions import ConfigurationError
from .logging import get_logger

logger = get_logger(__name__)

default_paths = [
    os.path.expanduser('~/.ufv-alerts.rc'),
    '/etc/ufv-alerts.rc',
]

def read(conf_file=None):

    test_ret = {
        'manglers': [{
                'name': 'passthrough',
                'config': {},
            }, {
                'name': 'datefbody',
                'config': {},
            }, {
                'name': 'camandsite',
                'config': {},
            },
        ],
        'outputs': [{
                'name': 'stdout',
                'config': {},
            }, {
                'name': 'slack',
                'config': {
                    'webhook_url': '',
                },
            },
        ],
    }

    config_files = [conf_file or ''] + default_paths
    logger.debug('Reading config from {}'.format(', '.join(config_files)))

    config = configparser.ConfigParser()
    config.read(config_files)

    return test_ret
