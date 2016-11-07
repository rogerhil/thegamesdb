# TheGamesDb API, Python Wrapper
# http://wiki.thegamesdb.net/index.php/Main_Page
# Copyright (C) 2015 Rogerio Hilbert Lima <rogerhil@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

""" This is the main module containing the main class TheGamesDb that provides
the resources and its methods to retrieve games related data through the
Games DB API (http://wiki.thegamesdb.net/index.php/Main_Page).
"""
__author__ = "Rogerio Hilbert Lima"
__copyright__ = "Copyright (C) 2015 Rogerio Hilbert Lima <rogerhil@gmail.com>"
__license__ = "GPL"

import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError
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
    """ The main class for The Games Db API. It provides the following
    resources at the momment:

    >>> api = TheGamesDb()
    >>> api.game
    <GameResource get,list>
    >>> api.platform
    <PlatformResource get,list,games>
    """

    base_url = 'http://thegamesdb.net/api/'
    base_images_url = 'http://thegamesdb.net/banners/'

    def __init__(self, request_attempts=10, seconds_between_attempts=5):
        """ This constructor sets the resources instances and the user
        agents to avoid to being banned by the API server. Every last request
        made by the API saves the last response in the self.last_response.
        If the request fails because a 502 status, it attempts to do it again
        many times defined in the request_attempts argument. And the attempt is
        made after seconds defined in the seconds_between_attempts argument.
        """
        self.game = GameResource(self)
        self.platform = PlatformResource(self)
        self.user_agents = USER_AGENTS
        self.last_response = None
        self.request_attempts = abs(request_attempts)
        self.seconds_between_attempts = abs(seconds_between_attempts)

    def _get_response(self, url, **params):
        """ Giving a service path and optional specific arguments, returns
        the response string.
        """
        data = urlencode(params)
        url = "%s?%s" % (url, data)
        headers = {'User-Agent': self.get_random_agent()}
        request = Request(url, headers=headers, method='GET')

        def open_request(request, attempts, err=None):
            if attempts > self.request_attempts:
                raise err
            attempts += 1
            try:
                with urlopen(request, timeout=30) as response:
                    return response.read()
            except HTTPError as err:
                if err.getcode() != 502:
                    raise err
                print("HTTPError occurred while trying to request the url "
                      "%s. %s. Trying again in %s seconds..." % (url, err,
                                                self.seconds_between_attempts))
                time.sleep(self.seconds_between_attempts)
                return open_request(request, attempts, err)

        attempts = 0
        self.last_response = open_request(request, attempts)
        return self.last_response

    def get_response(self, path, **params):
        """ Giving a service path and optional specific arguments, returns
        the response string.
        """
        url = "%s%s" % (self.base_url, path)
        return self._get_response(url, **params)

    def get_image_data(self, path):
        url = "%s%s" % (self.base_images_url, path)
        return self._get_response(url)

    def get_data(self, path, **params):
        """ Giving a service path and optional specific arguments, returns
        the XML data from the API parsed as a dict structure.
        """
        xml = self.get_response(path, **params)
        try:
            return parse(xml)
        except Exception as err:
            print(path)
            print(params)
            print(err)
            raise err

    def get_random_agent(self):
        """ Randomly returns one of the items in the the user_agents list
        defined.
        """
        return self.user_agents[randint(0, len(self.user_agents) - 1)]
