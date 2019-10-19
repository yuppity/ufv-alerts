import json

from urllib.parse import urljoin, urlparse, urlunparse
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

USER_AGENT = 'ufv-alerts/0.0.0'

def simple_get(url, headers={}):
    pass

def simple_post(url, data={}, headers={}, as_json=False):

    post_body = b''
    if as_json or headers.get('Content-Type', '') == 'application/json':
        post_body = json.dumps(data).encode('utf8')

    req = Request(url, data=post_body, headers=headers)
    req.add_header('User-Agent', USER_AGENT)

    try:
        res = urlopen(req)
        if res.getcode() != 200:
            raise HTTPError('HTTP {}'.format(res.getcode()))
        return res.read()
    except (HTTPError, URLError):
        return None

class Session():
    """HTTP Session"""
