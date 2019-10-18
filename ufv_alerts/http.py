import json

from urllib.parse import urljoin, urlparse, urlunparse
from urllib.request import urlopen, Request
from urllib.error import HTTPError

def simple_get(url, headers={}):
    pass

def simple_post(url, data={}, headers={}):
    pass

class Session():
    """HTTP Session"""
