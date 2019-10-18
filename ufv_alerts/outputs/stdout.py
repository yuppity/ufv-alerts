"""
Simple output example. Spits alerts to stdout.
"""

# Needed if you write your output handler as class
from .base import UFVAlertOutput

# Needed if you write your output handler as function
from ..handler_helpers import alert_handler

# Optional
import sys
from ..logging import get_logger
logger = get_logger(__name__)

# Example using a class
class StdoutOutput(UFVAlertOutput):

    def handle_alert(self, alert, *args, **kwargs):
        logger.debug('About to handle an alert in {}'.format(self))
        sys.stdout.write('Alert subject: ' + alert['subject'] + '\n')
        sys.stdout.flush()

# Another output handler using function as entry point
@alert_handler
def stdout_output_handler(config, alert, *args, **kwargs):
    logger.debug('About to handle an alert using a function entry point')
    sys.stdout.write('Alert subject: ' + alert['subject'] + '\n')
    sys.stdout.flush()
