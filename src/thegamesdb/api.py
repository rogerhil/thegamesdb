from urllib.parse import urlencode
from urllib.request import build_opener, HTTPHandler, Request
from random import randint
from xmltodict import parse

from .resources import GameResource, PlatformResource


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:23.0) Gecko/20100101 Firefox/23.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20140205 Firefox/24.0 Iceweasel/24.3.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:28.0) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
]


class TheGamesDb(object):

    base_url = 'http://thegamesdb.net/api/'

    def __init__(self):
        self.game = GameResource(self)
        self.platform = PlatformResource(self)
        self.user_agents = USER_AGENTS

    def get_response(self, path, **params):
        """
        """
        url = "%s%s" % (self.base_url, path)
        opener = build_opener(HTTPHandler)
        request = Request(url)
        request.add_header('User-Agent', self.get_random_agent())
        request.get_method = lambda: 'GET'
        if params:
            request.add_data(urlencode(**params))
        response = opener.open(request)
        return response

    def get_data(self, path, **params):
        """
        """
        response = self.get_response(path, **params)
        xml = response.read()
        return parse(xml)

    def get_random_agent(self):
        return self.user_agents[randint(0, len(self.user_agents))]
