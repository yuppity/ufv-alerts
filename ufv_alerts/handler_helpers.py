HANDLER_IDENTIFIER = '_ufvalerthandler'

def alert_handler(fn):
    setattr(fn, HANDLER_IDENTIFIER, True)
    return fn

class UFVAlertHandleWrapper():

    def __init__(self, config, base, handler, *args, **kwargs):
        self.handler_fn = handler
        self.config = config
        self.base = base
        self.handler_type = base.__name__

    def handle_alert(self, alert):
        return self.handler_fn(self.config, alert)

def setup_handlers(
        handlers_wanted, package, base,
        matcher=lambda x: False, sort_key=None, config={}):

    from types import ModuleType
    from .logging import get_logger
    import importlib
    import inspect

    handler_collection = []

    package_name = package.__name__ \
        if isinstance(package, ModuleType) else package

    logger = get_logger(package_name)

    for wanted in handlers_wanted:
        handler_module = importlib.import_module(
            '.' + wanted['name'], package_name)
        of_interest = (n for n in dir(handler_module) if n != base.__name__)
        for module_attr in of_interest:
            nothing = True
            obj = getattr(handler_module, module_attr)
            if inspect.isclass(obj) and base in inspect.getmro(obj):
                nothing = handler_collection.append(obj(wanted['config']))
            elif hasattr(obj, '__call__') and hasattr(obj, HANDLER_IDENTIFIER):
                nothing = handler_collection.append(
                    UFVAlertHandleWrapper(wanted['config'], base, obj))
            if not nothing:
                logger.info('Registered {}: {}'.format(
                    base.SINGULAR, obj.__name__))

    if sort_key:
        sorted(handler_collection, key=sort_key)

    return handler_collection
