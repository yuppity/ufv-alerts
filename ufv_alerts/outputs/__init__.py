from .base import UFVAlertOutput
from ..logging import get_logger
from ..handler_helpers import setup_handlers

def init(output_configs):
    return setup_handlers(output_configs, __name__, UFVAlertOutput)

def dispatch(output, queue):
    while True:
        alert = queue.get()
        output.handle_alert(alert)
