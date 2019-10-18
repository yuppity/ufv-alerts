from .base import UFVAlertMangler
from ..logging import get_logger
from ..handler_helpers import setup_handlers

logger = get_logger(__name__)

def init(mangler_configs):

    manglers = setup_handlers(
        mangler_configs, __name__, UFVAlertMangler,
        sort_key=lambda x: x.PRIORITY)

    return manglers

def run_all(output, manglers):

    logger.debug('Running manglers ({})'.format(len(manglers)))

    for mangler in manglers:
        output = mangler.mangle(output)
        if not output:
            return None
    return output
