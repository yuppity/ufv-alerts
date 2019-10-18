from . import UFVAlertMangler

class DummyMangler(UFVAlertMangler):

    PRIORITY = 0

    def mangle(self, alert):
        return alert
