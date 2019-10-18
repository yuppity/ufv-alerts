class UFVAlertOutput():

    SINGULAR = 'output handler'

    def __init__(self, config, *args, **kwargs):
        self.config = config

    def handle_alert(self, output, *args, **kwargs):
        raise NotImplementedError(
            'Your custom output is missing the handle_alert() method')
