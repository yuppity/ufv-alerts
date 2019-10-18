import re
from datetime import datetime
from . import UFVAlertMangler

class DateFromAlertBody(UFVAlertMangler):

    PRIORITY = 0

    def mangle(self, alert):
        body = alert['text_content']
        date_match = re.search(r'Camera.*?detected motion on(.*[AP]M)', body)
        if date_match:
            date_str = date_match.groups()[0].strip()
            alert['alert_datetime'] = datetime.strptime(
                date_str, '%A, %B %d, %Y at %I:%M %p')
        return alert
