class UFVAlertMangler():

    SINGULAR = 'mangler'

    def __init__(self, config, *args, **kwargs):
        self.config = config

    def handle_alert(self, *args, **kwargs):
        raise NotImplementedError(
            'Your custom mangler is missing the handle_alert() method')

