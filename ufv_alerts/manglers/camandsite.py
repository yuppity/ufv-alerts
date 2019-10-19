import re
from . import UFVAlertMangler

class CamPlusSite(UFVAlertMangler):

    PRIORITY = 0

    def mangle(self, alert):

        body = alert['text_content']
        subject = alert['subject']

        cam_site_match = re.search(r'Motion Detected:\s+(.*)\s+on\s+(\w*)', subject)

        if cam_site_match and len(cam_site_match.groups()) > 1:
            alert['camera'] = cam_site_match.groups()[0]
            alert['site'] = cam_site_match.groups()[1]
        else:
            alert['camera'] = None
            alert['site'] = None

        return alert
